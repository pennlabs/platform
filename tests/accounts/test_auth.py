import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser, User
from oauth2_provider.models import Application, AccessToken
from org.models import Member


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(username='student', password='secret')
        self.member = User.objects.create_user(username='member', password='secret')
        Member.objects.create(student=self.member.student, year_joined=datetime.date.today())
        self.application = Application(
            name="Test",
            redirect_uris='http://a.a',
            user=self.student,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE
        )
        self.application.save()
        self.student_token = AccessToken.objects.create(
            user=self.student, token="12345",
            application=self.application,
            expires=timezone.now() + datetime.timedelta(days=1),
            scope="read write"
        )
        self.member_token = AccessToken.objects.create(
            user=self.member, token="123456",
            application=self.application,
            expires=timezone.now() + datetime.timedelta(days=1),
            scope="read write"
        )
        self.student_header = {"HTTP_AUTHORIZATION": "Bearer " + self.student_token.token}
        self.member_header = {"HTTP_AUTHORIZATION": "Bearer " + self.member_token.token}

    def test_penn_view_anonymous(self):
        request = self.client.get(reverse('accounts:protected'))
        self.assertEqual(request.status_code, 403)

    def test_penn_view_student(self):
        request = self.client.get(reverse('accounts:protected'), **self.student_header)
        self.assertEqual(request.status_code, 200)

    def test_penn_view_member(self):
        request = self.client.get(reverse('accounts:protected'), **self.member_header)
        self.assertEqual(request.status_code, 200)

    def test_labs_view_anonymous(self):
        request = self.client.get(reverse('accounts:labsprotected'))
        self.assertEqual(request.status_code, 403)

    def test_labs_view_student(self):
        request = self.client.get(reverse('accounts:labsprotected'), **self.student_header)
        self.assertEqual(request.status_code, 403)

    def test_labs_view_member(self):
        request = self.client.get(reverse('accounts:labsprotected'), **self.member_header)
        self.assertEqual(request.status_code, 200)
