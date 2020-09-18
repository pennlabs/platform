import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase
from phonenumber_field.phonenumber import PhoneNumber

from accounts.models import Email, PhoneNumberModel, Student
from accounts.serializers import (
    EmailSerializer,
    PhoneNumberSerializer,
    StudentSerializer,
    UserSerializer,
)


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
        self.serializer_preferred_name = UserSerializer(self.user_preferred_name)

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


class FakeRequest:
    def __init__(self, user):
        self.user = user


class PhoneNumberSerializerTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            pennid=1,
            username="student",
            first_name="First",
            last_name="Last",
            email="test@example.com",
        )
        self.primary_number = PhoneNumberModel.objects.create(
            user=self.user, phone_number="+15550000000", primary=True, verified=True
        )
        self.non_primary_number = PhoneNumberModel.objects.create(
            user=self.user, phone_number="+15550000001"
        )

        self.serializer_primary = PhoneNumberSerializer(self.primary_number)
        self.serializer_non_primary = PhoneNumberSerializer(self.non_primary_number)

    def test_create(self):
        # If this is your phone number I'm sorry
        data = {
            "phone_number": "+12154729463",
            "primary": True,
            "verified": True,
            "verification_code": "000000",
        }
        serializer = PhoneNumberSerializer(data=data, context={"request": FakeRequest(self.user)})
        self.assertTrue(serializer.is_valid())
        phone_number = serializer.save()
        self.assertEqual(phone_number.user, self.user)
        self.assertFalse(phone_number.verified)
        self.assertFalse(phone_number.primary)
        self.assertNotEqual(phone_number.verification_code, "000000")
        # TODO: make sure sendSMSVerification is called

    # def test_primary_number(self):
    #     sample_response = {
    #         "phone_number": PhoneNumber.from_string(phone_number="+41524204242").as_e164,
    #         "primary_number": True,
    #         "verified": True,
    #     }
    #     self.assertEqual(self.serializer_primary.data, sample_response)

    # def test_non_primary_number(self):
    #     sample_response = {
    #         "phone_number": PhoneNumber.from_string(phone_number="+12150000000").as_e164,
    #         "primary_number": False,
    #         "verified": False,
    #     }
    #     self.assertEqual(self.serializer_non_primary.data, sample_response)


# class EmailSerializerTestCase(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             pennid=1,
#             username="student",
#             password="secret",
#             first_name="First",
#             last_name="Last",
#             email="test@test.com",
#         )
#         self.email_primary = Email.objects.create(
#             user=self.user, email="primary@test.com", primary_email=True
#         )
#         self.email_non_primary = Email.objects.create(
#             user=self.user, email="nonprimary@test.com", verified=True
#         )

#         self.serializer_primary = EmailSerializer(self.email_primary)
#         self.serializer_non_primary = EmailSerializer(self.email_non_primary)

#     def test_email_primary(self):
#         sample_response = {"email": "primary@test.com", "primary_email": True, "verified": False}
#         self.assertEqual(self.serializer_primary.data, sample_response)

#     def test_email_non_primary(self):
#         sample_response = {"email": "nonprimary@test.com", "primary_email": False, "verified": True}
#         self.assertEqual(self.serializer_non_primary.data, sample_response)
