import calendar
import datetime
import json
import os
import sys
from importlib import reload
from unittest.mock import MagicMock, patch
from urllib.parse import quote

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.test import Client, TestCase, override_settings
from django.urls import clear_url_caches, reverse
from django.utils import timezone
from oauth2_provider.models import get_access_token_model, get_application_model
from rest_framework.test import APIClient
from rest_framework_api_key.models import APIKey

from accounts.models import (
    Email,
    Major,
    PhoneNumber,
    PrivacyResource,
    PrivacySetting,
    School,
    User,
)
from accounts.serializers import (
    EmailSerializer,
    MajorSerializer,
    PhoneNumberSerializer,
    PrivacySettingSerializer,
    SchoolSerializer,
    StudentSerializer,
    UserSearchSerializer,
    UserSerializer,
)


def reload_urlconf():
    """
    reloads the urlconfs after settings variables are updated
    """
    urlconf = settings.ROOT_URLCONF
    acc_urls = "accounts.urls"
    if urlconf in sys.modules and acc_urls in sys.modules:
        clear_url_caches()
        reload(sys.modules[urlconf])
        reload(sys.modules[acc_urls])


@override_settings(IS_DEV_LOGIN=False)
class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        reload_urlconf()

    def test_invalid_shibboleth_response(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 500)

    @patch("accounts.backends.requests.post")
    @patch("accounts.backends.requests.get")
    def test_valid_shibboleth(self, mock_get, mock_post):
        mock_response_get = MagicMock()
        mock_response_get.status_code = 200
        mock_response_get.json.return_value = {"result_data": []}
        mock_get.return_value = mock_response_get

        mock_response_post = MagicMock()
        mock_response_post.status_code = 200
        mock_response_post.json.return_value = {"access_token": "my-access-token"}
        mock_post.return_value = mock_response_post

        headers = {
            "HTTP_EMPLOYEENUMBER": "1",
            "HTTP_EPPN": "test",
            "HTTP_GIVENNAME": "test",
            "HTTP_SN": "user-hyphenated",
            "HTTP_MAIL": "test@student.edu",
        }
        params = (
            reverse("accounts:authorize")
            + "?client_id=abc123&response_type=code&state=abc"
        )
        response = self.client.get(
            reverse("accounts:login") + "?next=" + quote(params), **headers
        )
        base_url = "/accounts/authorize/"
        sample_response = base_url + "?client_id=abc123&response_type=code&state=abc"
        self.assertRedirects(response, sample_response, fetch_redirect_response=False)
        user = get_user_model().objects.get(username="test")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User-Hyphenated")


@override_settings(IS_DEV_LOGIN=False)
class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        reload_urlconf()

    def test_logged_in_user(self):
        get_user_model().objects.create_user(
            pennid=1, username="user", password="secret"
        )
        self.client.login(username="user", password="secret")
        response = self.client.get(reverse("accounts:logout"))
        self.assertNotIn("_auth_user_id", self.client.session)
        sample_response = (
            "/Shibboleth.sso/Logout?return=https://idp.pennkey.upenn.edu/logout"
        )
        self.assertRedirects(response, sample_response, fetch_redirect_response=False)

    def test_guest_user(self):
        response = self.client.get(reverse("accounts:logout"))
        sample_response = (
            "/Shibboleth.sso/Logout?return=https://idp.pennkey.upenn.edu/logout"
        )
        self.assertRedirects(response, sample_response, fetch_redirect_response=False)


@override_settings(IS_DEV_LOGIN=True)
class DevLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        reload_urlconf()
        call_command("populate_users")

    def test_get_login_page(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)

    @patch("accounts.backends.requests.post")
    @patch("accounts.backends.requests.get")
    def test_login_valid_choice(self, mock_get, mock_post):
        mock_response_get = MagicMock()
        mock_response_get.status_code = 200
        mock_response_get.json.return_value = {"result_data": []}
        mock_get.return_value = mock_response_get

        mock_response_post = MagicMock()
        mock_response_post.status_code = 200
        mock_response_post.json.return_value = {"access_token": "my-access-token"}
        mock_post.return_value = mock_response_post

        self.client.post(reverse("accounts:login"), data={"userChoice": 1})
        # sample_response = reverse("application:homepage")
        expected_user_pennid = 1
        actual_user_pennid = int(self.client.session["_auth_user_id"])
        self.assertTrue(expected_user_pennid, actual_user_pennid)
        # self.assertRedirects(response, sample_response, fetch_redirect_response=False)

    @patch("accounts.backends.requests.post")
    @patch("accounts.backends.requests.get")
    def test_login_invalid_choice(self, mock_get, mock_post):
        mock_response_get = MagicMock()
        mock_response_get.status_code = 200
        mock_response_get.json.return_value = {"result_data": []}
        mock_get.return_value = mock_response_get

        mock_response_post = MagicMock()
        mock_response_post.status_code = 200
        mock_response_post.json.return_value = {"access_token": "my-access-token"}
        mock_post.return_value = mock_response_post

        self.client.post(reverse("accounts:login"), data={"userChoice": 24})
        self.assertTrue("_auth_user_id" in self.client.session)


@override_settings(IS_DEV_LOGIN=True)
class DevLogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        reload_urlconf()

    def test_logout_user(self):
        get_user_model().objects.create_user(
            pennid=1, username="user", password="secret"
        )
        self.client.login(username="user", password="secret")
        response = self.client.get(reverse("accounts:logout"))
        self.assertNotIn("_auth_user_id", self.client.session)
        sample_response = reverse("accounts:login")
        self.assertRedirects(response, sample_response, fetch_redirect_response=False)

    def test_guest_user(self):
        response = self.client.get(reverse("accounts:logout"))
        sample_response = reverse("accounts:login")
        self.assertRedirects(response, sample_response, fetch_redirect_response=False)


@override_settings(IS_DEV_LOGIN=False)
class UUIDIntrospectTokenViewTestCase(TestCase):
    """
    Not exhaustive since most testing is done in django-oauth-toolkit itself. Code borrowed from
    https://github.com/jazzband/django-oauth-toolkit/blob/master/tests/test_introspection_view.py
    """

    def setUp(self):
        reload_urlconf()
        self.Application = get_application_model()
        self.AccessToken = get_access_token_model()
        self.UserModel = get_user_model()
        self.resource_server_user = self.UserModel.objects.create_user(
            pennid=1, username="resource_server"
        )
        self.test_user = self.UserModel.objects.create_user(
            pennid=2, username="bar_user"
        )

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
        auth_headers = {
            "HTTP_AUTHORIZATION": "Bearer " + self.resource_server_token.token
        }
        response = self.client.post(
            reverse("accounts:introspect"),
            {"token": self.valid_token.token},
            **auth_headers,
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
        auth_headers = {
            "HTTP_AUTHORIZATION": "Bearer " + self.resource_server_token.token
        }
        response = self.client.post(
            reverse("accounts:introspect"),
            {"token": self.invalid_token.token},
            **auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertIsInstance(content, dict)
        self.assertDictEqual(content, {"active": False})

    def test_view_post_notexisting_token(self):
        auth_headers = {
            "HTTP_AUTHORIZATION": "Bearer " + self.resource_server_token.token
        }
        response = self.client.post(
            reverse("accounts:introspect"), {"token": "kaudawelsch"}, **auth_headers
        )

        self.assertEqual(response.status_code, 401)
        content = response.json()
        self.assertIsInstance(content, dict)
        self.assertDictEqual(content, {"active": False})


@override_settings(IS_DEV_LOGIN=False)
class UserSearchTestCase(TestCase):
    def setUp(self):
        reload_urlconf()
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
        response = self.client.get(
            reverse("accounts:search") + "?q=t", **self.auth_headers
        )
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
        response = self.client.get(
            reverse("accounts:search") + "?q=test1", **self.auth_headers
        )
        self.assertIn(UserSearchSerializer(self.user1).data, response.json())
        self.assertNotIn(UserSearchSerializer(self.user2).data, response.json())

    def test_exact_pennkey_user2(self):
        response = self.client.get(
            reverse("accounts:search") + "?q=test2", **self.auth_headers
        )
        self.assertNotIn(UserSearchSerializer(self.user1).data, response.json())
        self.assertIn(UserSearchSerializer(self.user2).data, response.json())

    def test_first_name(self):
        response = self.client.get(
            reverse("accounts:search") + "?q=tes", **self.auth_headers
        )
        self.assertIn(UserSearchSerializer(self.user1).data, response.json())
        self.assertIn(UserSearchSerializer(self.user2).data, response.json())


class UserViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            pennid=1,
            username="student",
            password="secret",
            first_name="First",
            last_name="Last",
            email="test@test.com",
        )

        Major.objects.create(
            name="Test Active Major", is_active=True, degree_type="BACHELORS"
        )
        Major.objects.create(
            name="Test Active Major 2", degree_type="PHD", is_active=True
        )
        Major.objects.create(
            name="Test Active Major 3", degree_type="PROFESSIONAL", is_active=True
        )

        School.objects.create(name="Test School")
        School.objects.create(name="Test School 2")

        self.user.student.major.add(Major.objects.get(name="Test Active Major"))
        self.user.student.major.add(Major.objects.get(name="Test Active Major 2"))
        self.user.student.school.add(School.objects.get(name="Test School"))
        self.user.student.graduation_year = 2024
        self.serializer = StudentSerializer(self.user.student)

        self.client = APIClient()
        self.serializer = UserSerializer(self.user)

    def test_get_object(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("accounts:me"))
        self.assertEqual(json.loads(response.content), self.serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_update_major(self):
        self.client.force_authenticate(user=self.user)
        update_data = {"student": {"school": [{"name": "Test School"}]}}

        response = self.client.patch(reverse("accounts:me"), update_data, format="json")

        self.assertEqual(json.loads(response.content), self.serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_update_school(self):
        self.client.force_authenticate(user=self.user)
        update_data = {
            "student": {"school": [{"name": "Test School"}, {"name": "Test School 2"}]}
        }

        response = self.client.patch(reverse("accounts:me"), update_data, format="json")

        self.assertEqual(json.loads(response.content), self.serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_update_all_student_fields(self):
        self.client.force_authenticate(user=self.user)
        update_data = {
            "student": {
                "major": [
                    {"name": "Test Active Major 2", "degree_type": "PHD"},
                    {"name": "Test Active Major", "degree_type": "BACHELORS"},
                ],
                "school": [{"name": "Test School 2"}],
                "graduation_year": 2030,
            }
        }

        response = self.client.patch(reverse("accounts:me"), update_data, format="json")

        self.assertEqual(json.loads(response.content), self.serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_update_invalid_graduation_year(self):
        self.client.force_authenticate(user=self.user)
        update_data = {"student": {"graduation_year": 1600}}

        response = self.client.patch(reverse("accounts:me"), update_data, format="json")

        self.assertEqual(response.status_code, 400)

    # add same major
    def test_update_same_major_twice(self):
        self.client.force_authenticate(user=self.user)
        update_data = {
            "student": {
                "major": [
                    {"name": "Test Active Major 2", "degree_type": "PHD"},
                    {"name": "Test Active Major 2", "degree_type": "PHD"},
                ],
                "school": [{"name": "Test School 2"}],
                "graduation_year": 2030,
            }
        }

        response = self.client.patch(reverse("accounts:me"), update_data, format="json")

        self.assertEqual(response.status_code, 200)


class FindUserViewTestCase(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            pennid=1,
            username="student",
            password="secret",
            first_name="First",
            last_name="Last",
            email="test@test.com",
        )

        self.user2 = get_user_model().objects.create_user(
            pennid=2,
            username="student2",
            password="secret2",
            first_name="First2",
            last_name="Last2",
            email="test2@test.com",
        )

        self.client = APIClient()
        self.serializer = UserSerializer(self.user1)

    def test_find_user(self):
        self.client.force_authenticate(user=self.user1)
        resp = self.client.get(
            reverse("accounts:user", kwargs={"username": "student2"})
        )
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(2, resp.json()["pennid"])

    def test_find_user_not_found(self):
        self.client.force_authenticate(user=self.user1)
        resp = self.client.get(
            reverse("accounts:user", kwargs={"username": "doesnt_exist"})
        )
        self.assertEqual(resp.status_code, 404, resp.content)


class ProfilePicViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            pennid=1,
            username="student",
            password="secret",
            first_name="First",
            last_name="Last",
            email="test@test.com",
        )

        self.client = APIClient()
        self.serializer = UserSerializer(self.user)

    def test_profile_pic_upload_success(self):
        # successful image upload
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(
            reverse("accounts:me-pfp-upload"),
            {
                "profile_pic": open(
                    os.path.join(os.getcwd(), "tests", "accounts", "test_pfp.jpg"),
                    "rb",
                )
            },
        )
        self.assertEqual(resp.status_code, 200, resp.content)

        # ensure image url is set
        resp = self.client.get(reverse("accounts:me"))
        self.assertEqual(resp.status_code, 200, resp.content)
        data = json.loads(resp.content.decode("utf-8"))
        self.assertTrue(data["profile_pic"])

    def test_profile_pic_upload_empty(self):
        # empty image throws an error
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(reverse("accounts:me-pfp-upload"))
        self.assertEqual(resp.status_code, 400, resp.content)

    def test_profile_pic_upload_non_image(self):
        # non-image upload should fail
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(
            reverse("accounts:me-pfp-upload"),
            {
                "profile_pic": open(
                    os.path.join(os.getcwd(), "README.md"),
                    "rb",
                )
            },
        )
        self.assertEqual(resp.status_code, 400, resp.content)

        # ensure image url is NOT set
        resp = self.client.get(reverse("accounts:me"))
        self.assertEqual(resp.status_code, 200, resp.content)
        data = json.loads(resp.content.decode("utf-8"))
        self.assertFalse(data["profile_pic"])

    def test_profile_pic_upload_too_large(self):
        # images larger than 500 KB should fail
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(
            reverse("accounts:me-pfp-upload"),
            {
                "profile_pic": open(
                    os.path.join(
                        os.getcwd(), "tests", "accounts", "test_pfp_large.png"
                    ),
                    "rb",
                )
            },
        )
        self.assertEqual(resp.status_code, 400, resp.content)

        # ensure image url is NOT set
        resp = self.client.get(reverse("accounts:me"))
        self.assertEqual(resp.status_code, 200, resp.content)
        data = json.loads(resp.content.decode("utf-8"))
        self.assertFalse(data["profile_pic"])

    def test_profile_pic_upload_no_auth(self):
        # not authenticated user should fail with 403
        resp = self.client.post(
            reverse("accounts:me-pfp-upload"),
            {
                "profile_pic": open(
                    os.path.join(os.getcwd(), "tests", "accounts", "test_pfp.jpg"),
                    "rb",
                )
            },
        )
        self.assertEqual(resp.status_code, 403, resp.content)

        # ensure image url is NOT set
        self.client.force_authenticate(user=self.user)
        resp = self.client.get(reverse("accounts:me"))
        self.assertEqual(resp.status_code, 200, resp.content)
        data = json.loads(resp.content.decode("utf-8"))
        self.assertFalse(data["profile_pic"])

    def test_profile_pic_upload_no_user(self):
        # uploading without a user should fail with 403
        self.client.force_authenticate()
        resp = self.client.post(
            reverse("accounts:me-pfp-upload"),
            {
                "profile_pic": open(
                    os.path.join(os.getcwd(), "tests", "accounts", "test_pfp.jpg"),
                    "rb",
                )
            },
        )
        self.assertEqual(resp.status_code, 403, resp.content)


class MajorViewTestCase(TestCase):
    def setUp(self):
        self.major_active_1 = Major.objects.create(
            name="Test Active Major", is_active=True
        )
        self.major_active_2 = Major.objects.create(
            name="Test Active Major 2", is_active=True
        )

        self.major_inactive_1 = Major.objects.create(
            name="Test Inactive Major", is_active=False
        )
        self.major_inactive_2 = Major.objects.create(
            name="Test Inactive Major 2", is_active=False
        )

        self.client = APIClient()
        self.serializer_active_1 = MajorSerializer(self.major_active_1)
        self.serializer_active_2 = MajorSerializer(self.major_active_2)

    def test_get_queryset(self):
        response = self.client.get(reverse("accounts:majors-list"))
        self.assertEqual(
            json.loads(response.content),
            [self.serializer_active_1.data, self.serializer_active_2.data],
        )


class SchoolViewTestCase(TestCase):
    def setUp(self):
        self.school_1 = School.objects.create(name="Test School")
        self.school_2 = School.objects.create(name="Test School 2")

        self.client = APIClient()
        self.serializer_1 = SchoolSerializer(self.school_1)
        self.serializer_2 = SchoolSerializer(self.school_2)

    def test_get_queryset(self):
        response = self.client.get(reverse("accounts:schools-list"))
        self.assertEqual(
            json.loads(response.content),
            [self.serializer_1.data, self.serializer_2.data],
        )


class PhoneNumberViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            pennid=1, username="test1", first_name="first1", last_name="last1"
        )

        self.number1 = PhoneNumber.objects.create(
            user=self.user, value="+12150001111", primary=False, verified=False
        )
        self.number2 = PhoneNumber.objects.create(
            user=self.user, value="+12058869999", primary=True, verified=True
        )
        self.number3 = PhoneNumber.objects.create(
            user=self.user, value="+16170031234", primary=False, verified=True
        )

        self.user2 = User.objects.create(
            pennid=2, username="test2", first_name="first2", last_name="last2"
        )
        self.number4 = PhoneNumber.objects.create(
            user=self.user2, value="+12158989000", primary=True, verified=True
        )

        self.client = APIClient()
        self.serializer1 = PhoneNumberSerializer(self.number1)
        self.serializer2 = PhoneNumberSerializer(self.number2)
        self.serializer3 = PhoneNumberSerializer(self.number3)
        self.expected_response = {"detail": "Phone number successfully deleted"}

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
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user.phone_numbers.filter(value="+12150001111").exists())

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
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user.phone_numbers.filter(value="+12058869999").exists())

    def test_destroy_only_number(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(
            reverse("accounts:me-phonenumber-detail", args=[self.number4.id])
        )
        self.assertEqual(json.loads(response.content), self.expected_response)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(self.user2.phone_numbers.all()), 0)

    def test_resend_verification_fail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse(
                "accounts:me-phonenumber-resend-verification", args=[self.number1.id]
            )
        )
        self.assertEqual(400, response.status_code)

    def test_resend_verification_success(self):
        # Mark verification code as expired
        self.number1.verification_timestamp = timezone.now() - datetime.timedelta(
            days=1
        )
        self.number1.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse(
                "accounts:me-phonenumber-resend-verification", args=[self.number1.id]
            )
        )
        self.assertEqual(200, response.status_code)


class EmailViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            pennid=1, username="test1", first_name="first1", last_name="last1"
        )
        self.email1 = Email.objects.create(
            user=self.user, value="example@test.com", primary=True, verified=True
        )
        self.email2 = Email.objects.create(
            user=self.user, value="example2@test.com", primary=False, verified=False
        )
        self.email3 = Email.objects.create(
            user=self.user, value="example3@test.com", primary=False, verified=True
        )
        self.user2 = User.objects.create(
            pennid=2, username="test2", first_name="first2", last_name="last2"
        )
        self.email4 = Email.objects.create(
            user=self.user2, value="example4@test.com", primary=True, verified=True
        )
        self.email5 = Email.objects.create(
            user=self.user2, value="example5@test.com", primary=False, verified=False
        )
        self.client = APIClient()
        self.serializer1 = EmailSerializer(self.email1)
        self.serializer2 = EmailSerializer(self.email2)
        self.serializer3 = EmailSerializer(self.email3)
        self.success_response = {"detail": "Email successfully deleted"}
        self.failure_response = {"detail": "You can't delete the only verified email"}

    def test_get_queryset(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("accounts:me-email-list"))
        self.assertEqual(
            json.loads(response.content),
            [self.serializer1.data, self.serializer2.data, self.serializer3.data],
        )

    def test_destroy_nonprimary(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse("accounts:me-email-detail", args=[self.email2.id])
        )
        self.email1.refresh_from_db()
        self.email3.refresh_from_db()
        self.assertTrue(self.email1.primary)
        self.assertFalse(self.email3.primary)
        self.assertEqual(json.loads(response.content), self.success_response)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user.emails.filter(value="example2@test.com").exists())

    def test_destroy_primary(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse("accounts:me-email-detail", args=[self.email1.id])
        )
        self.email2.refresh_from_db()
        self.email3.refresh_from_db()
        self.assertFalse(self.email2.primary)
        self.assertTrue(self.email3.primary)
        self.assertEqual(json.loads(response.content), self.success_response)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user.emails.filter(value="example@test.com").exists())

    def test_destroy_only_verified_email(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(
            reverse("accounts:me-email-detail", args=[self.email4.id])
        )
        self.email4.refresh_from_db()
        self.email5.refresh_from_db()
        self.assertTrue(self.email4.primary)
        self.assertFalse(self.email5.primary)
        self.assertEqual(json.loads(response.content), self.failure_response)
        self.assertEqual(response.status_code, 405)
        self.assertTrue(self.user2.emails.filter(value="example4@test.com").exists())

    def test_resend_verification_fail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("accounts:me-email-resend-verification", args=[self.email2.id])
        )
        self.assertEqual(400, response.status_code)

    def test_resend_verification_success(self):
        # Mark verification code as expired
        self.email2.verification_timestamp = timezone.now() - datetime.timedelta(days=1)
        self.email2.save()

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("accounts:me-email-resend-verification", args=[self.email2.id])
        )
        self.assertEqual(200, response.status_code)


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
        self.user.is_superuser = False
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


class PrivacySettingViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = User.objects.create(
            pennid=1, username="test1", first_name="first1", last_name="last1"
        )
        self.user_2 = User.objects.create(
            pennid=2, username="test2", first_name="first2", last_name="last2"
        )

        self.resource_1 = PrivacyResource.objects.create(name="ACADEMIC_IDENTITY")
        self.resource_2 = PrivacyResource.objects.create(name="COLLEGE_HOUSE")

        self.serializer = PrivacySettingSerializer

    def test_resource_postsave_settings_created(self):
        # Assert that the post save hook created settings for the 2 resources
        self.assertEqual(4, PrivacySetting.objects.all().count())
        self.assertEqual(2, self.user_1.privacy_setting.count())
        self.assertEqual(2, self.user_2.privacy_setting.count())

    def test_user_postsave_settings_created(self):
        # Assert that after user creation, new settings are made for the user
        user = User.objects.create(
            pennid=3, username="test3", first_name="first3", last_name="last3"
        )
        self.assertEqual(2, PrivacySetting.objects.filter(user=user).count())
        # Assert that saving on a pre-created user does not create new settings
        user.save()
        self.assertEqual(2, PrivacySetting.objects.filter(user=user).count())

    def test_authenticated(self):
        response = self.client.get(reverse("accounts:privacy"))
        self.assertEqual(403, response.status_code)

    def test_list_settings(self):
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(reverse("accounts:privacy"))
        # Assert the list is exactly all of user_1's settings with correct fields
        self.assertEqual(
            json.loads(response.content),
            self.serializer(
                PrivacySetting.objects.filter(user=self.user_1), many=True
            ).data,
        )
        # Assert the list is exactly all of user_2's settings with correct fields
        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(reverse("accounts:privacy"))
        self.assertEqual(
            json.loads(response.content),
            self.serializer(
                PrivacySetting.objects.filter(user=self.user_2), many=True
            ).data,
        )

    def test_update_settings(self):
        # Assert after updating, setting changes to false
        self.client.force_authenticate(user=self.user_1)
        update_data_1 = {"enabled": False}
        test_id_1 = self.user_1.privacy_setting.first().id
        response = self.client.patch(
            reverse("accounts:privacy", args=[test_id_1]),
            data=update_data_1,
            format="json",
        )
        test_setting_1 = PrivacySetting.objects.get(id=test_id_1)
        self.assertEqual(
            json.loads(response.content), self.serializer(test_setting_1).data
        )
        self.assertFalse(test_setting_1.enabled)

        # Assert after updating, setting remains to true (settings default to true)
        self.client.force_authenticate(user=self.user_2)
        update_data_2 = {"enabled": True}
        test_id_2 = self.user_2.privacy_setting.first().id
        response = self.client.patch(
            reverse("accounts:privacy", args=[test_id_2]),
            data=update_data_2,
            format="json",
        )
        test_setting_2 = PrivacySetting.objects.get(id=test_id_2)
        self.assertEqual(
            json.loads(response.content), self.serializer(test_setting_2).data
        )
        self.assertTrue(test_setting_2.enabled)
