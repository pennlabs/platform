import datetime

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from oauth2_provider.models import AccessToken, Application

from accounts.models import Student


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = get_user_model().objects.create_user(
            pennid=1, username="student", password="secret"
        )
        Student.objects.create(user=self.student)
        self.application = Application(
            name="Test",
            redirect_uris="http://a.a",
            user=self.student,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.application.save()
        self.student_token = AccessToken.objects.create(
            user=self.student,
            token="12345",
            application=self.application,
            expires=timezone.now() + datetime.timedelta(days=1),
            scope="read write",
        )
        self.student_header = {"HTTP_AUTHORIZATION": "Bearer " + self.student_token.token}

    def test_penn_view_anonymous(self):
        request = self.client.get(reverse("accounts:protected"))
        self.assertEqual(request.status_code, 403)

    def test_penn_view_student(self):
        request = self.client.get(reverse("accounts:protected"), **self.student_header)
        self.assertEqual(request.status_code, 200)

    def test_labs_view_anonymous(self):
        request = self.client.get(reverse("accounts:labsprotected"))
        self.assertEqual(request.status_code, 403)

    def test_labs_view_student(self):
        request = self.client.get(reverse("accounts:labsprotected"), **self.student_header)
        self.assertEqual(request.status_code, 403)
