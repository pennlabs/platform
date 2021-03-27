import calendar
import datetime
from urllib.parse import quote

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from oauth2_provider.models import get_access_token_model, get_application_model
from rest_framework_api_key.models import APIKey

from accounts.models import User
from accounts.serializers import UserSearchSerializer, UserSerializer


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_invalid_shibboleth_response(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 500)

    def test_valid_shibboleth(self):
        headers = {
            "HTTP_EMPLOYEENUMBER": "1",
            "HTTP_EPPN": "test",
            "HTTP_GIVENNAME": "test",
            "HTTP_SN": "user-hyphenated",
            "HTTP_MAIL": "test@student.edu",
        }
        params = reverse("accounts:authorize") + "?client_id=abc123&response_type=code&state=abc"
        response = self.client.get(reverse("accounts:login") + "?next=" + quote(params), **headers)
        base_url = "/accounts/authorize/"
        sample_response = base_url + "?client_id=abc123&response_type=code&state=abc"
        self.assertRedirects(response, sample_response, fetch_redirect_response=False)
        user = get_user_model().objects.get(username="test")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User-Hyphenated")


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_logged_in_user(self):
        get_user_model().objects.create_user(pennid=1, username="user", password="secret")
        self.client.login(username="user", password="secret")
        response = self.client.get(reverse("accounts:logout"))
        self.assertNotIn("_auth_user_id", self.client.session)
        sample_response = "/Shibboleth.sso/Logout?return=https://idp.pennkey.upenn.edu/logout"
        self.assertRedirects(response, sample_response, fetch_redirect_response=False)

    def test_guest_user(self):
        response = self.client.get(reverse("accounts:logout"))
        sample_response = "/Shibboleth.sso/Logout?return=https://idp.pennkey.upenn.edu/logout"
        self.assertRedirects(response, sample_response, fetch_redirect_response=False)


class UUIDIntrospectTokenViewTestCase(TestCase):
    """
    Not exhaustive since most testing is done in django-oauth-toolkit itself. Code borrowed from
    https://github.com/jazzband/django-oauth-toolkit/blob/master/tests/test_introspection_view.py
    """

    def setUp(self):
        self.Application = get_application_model()
        self.AccessToken = get_access_token_model()
        self.UserModel = get_user_model()
        self.resource_server_user = self.UserModel.objects.create_user(
            pennid=1, username="resource_server"
        )
        self.test_user = self.UserModel.objects.create_user(pennid=2, username="bar_user")

        self.application = self.Application(
            name="Test Application",
            redirect_uris="http://localhost http://example.com http://example.org",
            user=self.test_user,
            client_type=self.Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=self.Application.GRANT_AUTHORIZATION_CODE,
        )
        self.application.save()

        self.resource_server_token = self.AccessToken.objects.create(
            user=self.resource_server_user,
            token="12345678900",
            application=self.application,
            expires=timezone.now() + datetime.timedelta(days=1),
            scope="introspection",
        )

        self.valid_token = self.AccessToken.objects.create(
            user=self.test_user,
            token="12345678901",
            application=self.application,
            expires=timezone.now() + datetime.timedelta(days=1),
            scope="read write dolphin",
        )

        self.invalid_token = self.AccessToken.objects.create(
            user=self.test_user,
            token="12345678902",
            application=self.application,
            expires=timezone.now() + datetime.timedelta(days=-1),
            scope="read write dolphin",
        )

    def test_view_post_valid_token(self):

        auth_headers = {"HTTP_AUTHORIZATION": "Bearer " + self.resource_server_token.token}
        response = self.client.post(
            reverse("accounts:introspect"), {"token": self.valid_token.token}, **auth_headers
        )

        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertIsInstance(content, dict)
        self.assertDictEqual(
            content,
            {
                "active": True,
                "scope": self.valid_token.scope,
                "client_id": self.valid_token.application.client_id,
                "user": UserSerializer(self.valid_token.user).data,
                "exp": int(calendar.timegm(self.valid_token.expires.timetuple())),
            },
        )

    def test_view_post_invalid_token(self):
        auth_headers = {"HTTP_AUTHORIZATION": "Bearer " + self.resource_server_token.token}
        response = self.client.post(
            reverse("accounts:introspect"), {"token": self.invalid_token.token}, **auth_headers
        )

        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertIsInstance(content, dict)
        self.assertDictEqual(content, {"active": False})

    def test_view_post_notexisting_token(self):
        auth_headers = {"HTTP_AUTHORIZATION": "Bearer " + self.resource_server_token.token}
        response = self.client.post(
            reverse("accounts:introspect"), {"token": "kaudawelsch"}, **auth_headers
        )

        self.assertEqual(response.status_code, 401)
        content = response.json()
        self.assertIsInstance(content, dict)
        self.assertDictEqual(content, {"active": False})


class UserSearchTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            pennid=1, username="test1", first_name="Test", last_name="Userabc"
        )
        self.user2 = User.objects.create(
            pennid=2, username="test2", first_name="Testing", last_name="User"
        )
        self.token = "abc123"
        self.AccessToken = get_access_token_model()
        self.AccessToken.objects.create(
            user=self.user1,
            token=self.token,
            expires=timezone.now() + datetime.timedelta(days=1),
            scope="read",
        )
        self.client = Client()
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Bearer {self.token}"}

    def test_short_query(self):
        response = self.client.get(reverse("accounts:search") + "?q=t", **self.auth_headers)
        self.assertFalse(response.json())
        self.assertNotIn(UserSearchSerializer(self.user1).data, response.json())
        self.assertNotIn(UserSearchSerializer(self.user2).data, response.json())

    def test_full_name(self):
        response = self.client.get(
            reverse("accounts:search") + "?q=test%20user", **self.auth_headers
        )
        self.assertIn(UserSearchSerializer(self.user1).data, response.json())
        self.assertIn(UserSearchSerializer(self.user2).data, response.json())

    def test_exact_pennkey_user1(self):
        response = self.client.get(reverse("accounts:search") + "?q=test1", **self.auth_headers)
        self.assertIn(UserSearchSerializer(self.user1).data, response.json())
        self.assertNotIn(UserSearchSerializer(self.user2).data, response.json())

    def test_exact_pennkey_user2(self):
        response = self.client.get(reverse("accounts:search") + "?q=test2", **self.auth_headers)
        self.assertNotIn(UserSearchSerializer(self.user1).data, response.json())
        self.assertIn(UserSearchSerializer(self.user2).data, response.json())

    def test_first_name(self):
        response = self.client.get(reverse("accounts:search") + "?q=tes", **self.auth_headers)
        self.assertIn(UserSearchSerializer(self.user1).data, response.json())
        self.assertIn(UserSearchSerializer(self.user2).data, response.json())


class ProductAdminViewTestCase(TestCase):
    def setUp(self):
        _, self.key = APIKey.objects.create_key(name="my-remote-service")
        self.authorization = f"Api-Key {self.key}"
        self.user = User.objects.create(username="test", pennid=123)

    def test_invalid_key(self):
        authorization = "Api-Key abc"
        response = self.client.post(
            reverse("accounts:productadmin"), HTTP_AUTHORIZATION=authorization
        )
        self.assertEqual(403, response.status_code)

    def test_invalid_body(self):
        response = self.client.post(
            reverse("accounts:productadmin"), HTTP_AUTHORIZATION=self.authorization
        )
        self.assertEqual(400, response.status_code)

    def test_remove_product_admin(self):
        content_type = ContentType.objects.get(app_label="accounts", model="user")
        perm = Permission.objects.create(
            content_type=content_type, codename="example_admin", name="Example Admin"
        )
        self.user.user_permissions.add(perm)
        self.assertEqual(1, self.user.user_permissions.count())
        response = self.client.post(
            reverse("accounts:productadmin"),
            {"user2": []},
            content_type="application/json",
            HTTP_AUTHORIZATION=self.authorization,
        )
        self.assertEqual(200, response.status_code)
        self.user.refresh_from_db()
        self.assertEqual(0, self.user.user_permissions.count())

    def test_remove_platform_admin(self):
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        response = self.client.post(
            reverse("accounts:productadmin"),
            {"user2": []},
            content_type="application/json",
            HTTP_AUTHORIZATION=self.authorization,
        )
        self.assertEqual(200, response.status_code)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_add_product_admin(self):
        response = self.client.post(
            reverse("accounts:productadmin"),
            {"test": ["example_product_admin"]},
            content_type="application/json",
            HTTP_AUTHORIZATION=self.authorization,
        )
        self.assertEqual(200, response.status_code)
        self.user.refresh_from_db()
        self.assertEqual(1, self.user.user_permissions.count())
        perm = self.user.user_permissions.first()
        self.assertEqual("example_product_admin", perm.codename)
        self.assertEqual("Example Product Admin", perm.name)

    def test_add_platform_admin(self):
        response = self.client.post(
            reverse("accounts:productadmin"),
            {"test": ["platform_admin"]},
            content_type="application/json",
            HTTP_AUTHORIZATION=self.authorization,
        )
        self.assertEqual(200, response.status_code)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)
