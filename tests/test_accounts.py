import datetime
from django.contrib.auth.models import AnonymousUser, User
from django.test import Client, TestCase
from django.test import Client as APIClient
from org.models import Member
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# TODO test login, auth and backends
class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student', password='secret')


class LabsTokenAuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = User.objects.create_user(username='student', password='secret')
        self.member = User.objects.create_user(username='member', password='secret')
        Member.objects.create(student=self.member.student, year_joined=datetime.date.today())
        self.student_token = TokenObtainPairSerializer.get_token(self.student).access_token
        self.member_token = TokenObtainPairSerializer.get_token(self.member).access_token
        self.student_header = "Bearer " + str(self.student_token)
        self.member_header = "Bearer " + str(self.member_token)

    def test_penn_mixin(self):
        request = self.client.get('/accounts/protected/', HTTP_AUTHORIZATION=self.student_header)
        self.assertEquals(request.status_code, 200)
        self.client.logout()

        request = self.client.get('/accounts/protected/', HTTP_AUTHORIZATION=self.member_header)
        self.assertEquals(request.status_code, 200)

        request = self.client.get('/accounts/protected/')
        self.assertEquals(request.status_code, 401)

    def test_labs_mixin(self):
        request = self.client.get('/accounts/labsprotected/', HTTP_AUTHORIZATION=self.student_header)
        self.assertEquals(request.status_code, 401)

        request = self.client.get('/accounts/labsprotected/', HTTP_AUTHORIZATION=self.member_header)
        self.assertEquals(request.status_code, 200)

        request = self.client.get('/accounts/labsprotected/')
        self.assertEquals(request.status_code, 401)
