import datetime

import pytz
from django.contrib.auth.models import User
from django.test import TestCase

from accounts.serializers import StudentSerializer


class SerializerTestCase(TestCase):
    def setUp(self):
        self.date = pytz.timezone('America/New_York').localize(datetime.datetime(2019, 1, 1))
        self.user = User.objects.create_user(username='student', password='secret', email='student@student.edu',
                                             date_joined=self.date)
        self.user.student.name = 'Student'
        self.user.student.major = 'Major'
        self.user.student.school = 'School'
        self.serializer = StudentSerializer(self.user.student)

    def test_str(self):
        sample_response = {'name': 'Student', 'major': 'Major', 'school': 'School', 'username': 'student',
                           'email': 'student@student.edu', 'date_joined': '2019-01-01T00:00:00-05:00'}
        self.assertEqual(self.serializer.data, sample_response)
