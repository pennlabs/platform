import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Student
from accounts.serializers import StudentSerializer, UserSerializer


class StudentSerializerTestCase(TestCase):
    def setUp(self):
        self.date = pytz.timezone("America/New_York").localize(datetime.datetime(2019, 1, 1))
        self.user = get_user_model().objects.create_user(
            pennid=1,
            username="student",
            password="secret",
            first_name="First",
            last_name="Last",
            email="test@test.com",
        )
        Student.objects.create(user=self.user)
        self.user.student.name = "Student"
        self.user.student.major = "Major"
        self.user.student.school = "School"
        self.serializer = StudentSerializer(self.user.student)

        self.user_preferred_name = get_user_model().objects.create_user(
            pennid=2,
            username="student2",
            password="secret2",
            first_name="First2",
            last_name="Last2",
            email="test2@test.com",
            preferred_name="Preferred",
        )
        Student.objects.create(user=self.user_preferred_name)
        self.user_preferred_name.student.name = "Student"
        self.user_preferred_name.student.major = "Major"
        self.user_preferred_name.student.school = "School"
        self.serializer_preferred_name = StudentSerializer(self.user_preferred_name.student)

    def test_str_no_preferred_name(self):
        sample_response = {
            "major": "Major",
            "school": "School",
            "first_name": "First",
            "last_name": "Last",
            "username": "student",
            "email": "test@test.com",
            "groups": [],
            "user_permissions": [],
            "product_permission": [],  # TODO: remove this after migrating to permissions in DLA
        }
        self.assertEqual(self.serializer.data, sample_response)

    def test_str_preferred_name_provided(self):
        sample_response = {
            "major": "Major",
            "school": "School",
            "first_name": "Preferred",
            "last_name": "Last2",
            "username": "student2",
            "email": "test2@test.com",
            "groups": [],
            "user_permissions": [],
            "product_permission": [],  # TODO: remove this after migrating to permissions in DLA
        }
        self.assertEqual(self.serializer_preferred_name.data, sample_response)


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.date = pytz.timezone("America/New_York").localize(datetime.datetime(2019, 1, 1))
        self.user = get_user_model().objects.create_user(
            pennid=1,
            username="student",
            password="secret",
            first_name="First",
            last_name="Last",
            email="test@test.com",
        )
        self.serializer = UserSerializer(self.user)

        self.user_preferred_name = get_user_model().objects.create_user(
            pennid=2,
            username="student2",
            password="secret2",
            first_name="First2",
            last_name="Last2",
            email="test2@test.com",
            preferred_name="Preferred",
        )
        self.serializer_preferred_name = UserSerializer(self.user)

    def test_str_no_preferred_name(self):
        sample_response = {
            "pennid": 1,
            "first_name": "First",
            "last_name": "Last",
            "username": "student",
            "email": "test@test.com",
            "groups": [],
            "user_permissions": [],
            "product_permission": [],  # TODO: remove this after migrating to permissions in DLA
        }
        self.assertEqual(self.serializer.data, sample_response)
        
    def test_str_preferred_name_provided(self):
        sample_response = {
            "pennid": 2,
            "first_name": "Preferred",
            "last_name": "Last2",
            "username": "student2",
            "email": "test2@test.com",
            "groups": [],
            "user_permissions": [],
            "product_permission": [],  # TODO: remove this after migrating to permissions in DLA
        }
        self.assertEqual(self.serializer_preferred_name.data, sample_response)
