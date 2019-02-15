import datetime
import pytz
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.serializers import StudentSerializer


class SerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student', password='secret', email='student@student.edu',
                                             date_joined=datetime.datetime(2019, 1, 1, tzinfo=pytz.UTC))
        self.user.student.name = 'Student'
        self.user.student.major = 'Major'
        self.user.student.school = 'School'
        self.serializer = StudentSerializer(self.user.student)

    def test_str(self):
        sample_response = {'name': 'Student', 'major': 'Major', 'school': 'School', 'username': 'student',
                           'email': 'student@student.edu', 'date_joined': '2019-01-01T00:00:00Z'}
        self.assertEqual(self.serializer.data, sample_response)
