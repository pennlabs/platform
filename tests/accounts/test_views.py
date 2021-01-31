import calendar
import datetime
import json
from urllib.parse import quote

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from oauth2_provider.models import get_access_token_model, get_application_model
from rest_framework.test import APIClient

from accounts.models import Email, PhoneNumberModel, User
from accounts.serializers import (
    EmailSerializer,
    PhoneNumberSerializer,
    UserSearchSerializer,
    UserSerializer,
)


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


class UserViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            pennid=1, username="test1", first_name="first1", last_name="last1"
        )
        self.client = APIClient()
        self.serializer = UserSerializer(self.user)

    def test_get_object(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("accounts:me"))
        self.assertEqual(json.loads(response.content), self.serializer.data)


class PhoneNumberViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            pennid=1, username="test1", first_name="first1", last_name="last1"
        )

        self.number1 = PhoneNumberModel.objects.create(
            user=self.user, phone_number="+12150001111", primary=False, verified=False,
        )
        self.number2 = PhoneNumberModel.objects.create(
            user=self.user, phone_number="+12058869999", primary=True, verified=True,
        )
        self.number3 = PhoneNumberModel.objects.create(
            user=self.user, phone_number="+16170031234", primary=False, verified=True,
        )

        self.user2 = User.objects.create(
            pennid=2, username="test2", first_name="first2", last_name="last2",
        )
        self.number4 = PhoneNumberModel.objects.create(
            user=self.user2, phone_number="+12158989000", primary=True, verified=True,
        )

        self.client = APIClient()
        self.serializer1 = PhoneNumberSerializer(self.number1)
        self.serializer2 = PhoneNumberSerializer(self.number2)
        self.serializer3 = PhoneNumberSerializer(self.number3)
        self.expected_response = {"message": "Phone number successfully deleted", "status": 200}

    def test_get_queryset(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("accounts:me-phonenumber-list"))
        self.assertEqual(
            json.loads(response.content),
            [self.serializer1.data, self.serializer2.data, self.serializer3.data],
        )

    def test_destroy_nonprimary(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse("accounts:me-phonenumber-detail", args=[self.number1.id])
        )
        self.number2.refresh_from_db()
        self.number3.refresh_from_db()
        self.assertTrue(self.number2.primary)
        self.assertFalse(self.number3.primary)
        self.assertEqual(json.loads(response.content), self.expected_response)
        self.assertFalse(self.user.phone_numbers.filter(phone_number="+12150001111").exists())

    def test_destroy_primary(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse("accounts:me-phonenumber-detail", args=[self.number2.id])
        )
        self.number1.refresh_from_db()
        self.number3.refresh_from_db()
        self.assertTrue(self.number3.primary)
        self.assertFalse(self.number1.primary)
        self.assertEqual(json.loads(response.content), self.expected_response)
        self.assertFalse(self.user.phone_numbers.filter(phone_number="+12058869999").exists())

    def test_destroy_only_number(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(
            reverse("accounts:me-phonenumber-detail", args=[self.number4.id])
        )
        self.assertEqual(json.loads(response.content), self.expected_response)
        self.assertEquals(len(self.user2.phone_numbers.all()), 0)


class EmailViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            pennid=1, username="test1", first_name="first1", last_name="last1"
        )
        self.email1 = Email.objects.create(
            user=self.user, email="example@test.com", primary=True, verified=True,
        )
        self.email2 = Email.objects.create(
            user=self.user, email="example2@test.com", primary=False, verified=False,
        )
        self.email3 = Email.objects.create(
            user=self.user, email="example3@test.com", primary=False, verified=True,
        )
        self.user2 = User.objects.create(
            pennid=2, username="test2", first_name="first2", last_name="last2"
        )
        self.email4 = Email.objects.create(
            user=self.user2, email="example4@test.com", primary=True, verified=True
        )
        self.email5 = Email.objects.create(
            user=self.user2, email="example5@test.com", primary=False, verified=False
        )
        self.client = APIClient()
        self.serializer1 = EmailSerializer(self.email1)
        self.serializer2 = EmailSerializer(self.email2)
        self.serializer3 = EmailSerializer(self.email3)
        self.success_response = {"message": "Email successfully deleted", "status": 200}
        self.failure_response = {
            "message": "You can't delete the only verified email",
            "status": 405,
        }

    def test_get_queryset(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("accounts:me-email-list"))
        self.assertEqual(
            json.loads(response.content),
            [self.serializer1.data, self.serializer2.data, self.serializer3.data],
        )

    def test_destroy_nonprimary(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("accounts:me-email-detail", args=[self.email2.id]))
        self.email1.refresh_from_db()
        self.email3.refresh_from_db()
        self.assertTrue(self.email1.primary)
        self.assertFalse(self.email3.primary)
        self.assertEqual(json.loads(response.content), self.success_response)
        self.assertFalse(self.user.emails.filter(email="example2@test.com").exists())

    def test_destroy_primary(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("accounts:me-email-detail", args=[self.email1.id]))
        self.email2.refresh_from_db()
        self.email3.refresh_from_db()
        self.assertFalse(self.email2.primary)
        self.assertTrue(self.email3.primary)
        self.assertEqual(json.loads(response.content), self.success_response)
        self.assertFalse(self.user.emails.filter(email="example@test.com").exists())

    def test_destroy_only_verified_email(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(reverse("accounts:me-email-detail", args=[self.email4.id]))
        self.email4.refresh_from_db()
        self.email5.refresh_from_db()
        self.assertTrue(self.email4.primary)
        self.assertFalse(self.email5.primary)
        self.assertEqual(json.loads(response.content), self.failure_response)
        self.assertTrue(self.user2.emails.filter(email="example4@test.com").exists())
