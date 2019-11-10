import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Student
from accounts.serializers import StudentSerializer, UserSerializer


class StudentSerializerTestCase(TestCase):
    def setUp(self):
        self.date = pytz.timezone('America/New_York').localize(datetime.datetime(2019, 1, 1))
        self.user = get_user_model().objects.create_user(
            pennid=1,
            username='student',
            password='secret',
            first_name='First',
            last_name='Last',
            email='test@test.com',
        )
        Student.objects.create(user=self.user)
        self.user.student.name = 'Student'
        self.user.student.major = 'Major'
        self.user.student.school = 'School'
        self.serializer = StudentSerializer(self.user.student)

    def test_str(self):
        sample_response = {
            'major': 'Major',
            'school': 'School',
            'first_name': 'First',
            'last_name': 'Last',
            'username': 'student',
            'email': 'test@test.com',
            'affiliation': [],
            'product_permission': []
        }
        self.assertEqual(self.serializer.data, sample_response)


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.date = pytz.timezone('America/New_York').localize(datetime.datetime(2019, 1, 1))
        self.user = get_user_model().objects.create_user(
            pennid=1,
            username='student',
            password='secret',
            first_name='First',
            last_name='Last',
            email='test@test.com',
        )
        self.serializer = UserSerializer(self.user)

    def test_str(self):
        sample_response = {
            'pennid': 1,
            'first_name': 'First',
            'last_name': 'Last',
            'username': 'student',
            'email': 'test@test.com',
            'affiliation': [],
            'product_permission': []
        }
        self.assertEqual(self.serializer.data, sample_response)
