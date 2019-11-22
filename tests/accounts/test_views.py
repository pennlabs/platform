import calendar
import datetime

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.six.moves.urllib.parse import quote
from oauth2_provider.models import get_access_token_model, get_application_model

from accounts.serializers import UserSerializer


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
            "HTTP_SN": "user",
            "HTTP_MAIL": "test@student.edu",
        }
        params = reverse("accounts:authorize") + "?client_id=abc123&response_type=code&state=abc"
        response = self.client.get(reverse("accounts:login") + "?next=" + quote(params), **headers)
        base_url = "/accounts/authorize/"
        sample_response = base_url + "?client_id=abc123&response_type=code&state=abc"
        self.assertRedirects(response, sample_response, fetch_redirect_response=False)


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
