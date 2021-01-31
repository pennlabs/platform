import datetime
import json

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import serializers

from accounts.models import Email, PhoneNumberModel, Student, User, Major, School
from accounts.serializers import (
    EmailSerializer,
    PhoneNumberSerializer,
    StudentSerializer,
    UserSearchSerializer,
    UserSerializer, MajorSerializer, SchoolSerializer, UserSerializer2,
)


class FakeRequest:
    def __init__(self, user):
        self.user = user


class SchoolSerializerTestCase(TestCase):
    def setUp(self):
        self.school = School.objects.create(name="Test School")

        self.serializer = SchoolSerializer(self.school)

    def test_active_major(self):
        sample_response = {
            "name": "Test School"
        }
        self.assertEqual(self.serializer.data, sample_response)


class MajorSerializerTestCase(TestCase):
    def setUp(self):
        self.major_active = Major.objects.create(name="Test Active Major", is_active=True)
        self.major_inactive = Major.objects.create(name="Test Inactive Major", is_active=False)

        self.serializer_active = MajorSerializer(self.major_active)
        self.serializer_inactive = MajorSerializer(self.major_inactive)

    def test_active_major(self):
        sample_response = {
            "name": "Test Active Major"
        }
        self.assertEqual(self.serializer_active.data, sample_response)

    def test_inactive_major(self):
        sample_response = {
            "name": "Test Inactive Major"
        }
        self.assertEqual(self.serializer_inactive.data, sample_response)


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
        Major.objects.create(name="Test Active Major", is_active=True)
        Major.objects.create(name="Test Active Major 2", is_active=True)

        School.objects.create(name="Test School")

        Student.objects.create(user=self.user)
        self.user.student.major.add(Major.objects.get(name="Test Active Major"))
        self.user.student.major.add(Major.objects.get(name="Test Active Major 2"))
        self.user.student.school.add(School.objects.get(name="Test School"))
        self.serializer = StudentSerializer(self.user.student)

    def test_two_majors(self):
        sample_response = {
            "major": ["Test Active Major", "Test Active Major 2"],
            "school": ["Test School"]
        }

        # print(json.dumps(self.serializer.data, indent=4))
        self.assertEqual(self.serializer.data, sample_response)

    def test_remove_major(self):
        sample_response = {
            "major": ["Test Active Major"],
            "school": ["Test School"]
        }

        major_to_remove = Major.objects.get(name="Test Active Major 2");

        self.user.student.major.remove(major_to_remove)
        # print(json.dumps(self.serializer.data, indent=4))

        self.assertEqual(self.serializer.data, sample_response)

    def test_remove_school(self):
        sample_response = {
            "major": ["Test Active Major", "Test Active Major 2"],
            "school": []
        }

        school_to_remove = School.objects.get(name="Test School");

        self.user.student.school.remove(school_to_remove)
        print(json.dumps(self.serializer.data, indent=4))

        self.assertEqual(self.serializer.data, sample_response)

    def test_remove_nonexistent_major(self):
        sample_response = {
            "major": ["Test Active Major", "Test Active Major Non Existent"],
            "school": ["Test School"]
        }

        print(json.dumps(self.serializer.data, indent=4))

        self.assertEqual(self.serializer.data, sample_response)



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

    def test_update_preferred_valid_name(self):
        data = {
            "first_name": "new_preferred",
        }
        serializer = UserSerializer(self.user, data=data)

        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(self.user.preferred_name, "new_preferred")
        self.assertEqual(self.user.first_name, "First")

    def test_preferred_same_as_first(self):
        data = {
            "first_name": "First2",
        }
        serializer = UserSerializer(self.user_preferred_name, data=data)

        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(self.user_preferred_name.preferred_name, "")
        self.assertEqual(self.user_preferred_name.first_name, "First2")


class UserSerializer2TestCase(TestCase):
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
        Major.objects.create(name="Test Active Major", is_active=True)
        School.objects.create(name="Test School")
        self.student = StudentSerializer(Student.objects.create(user=self.user))

        # print(json.dumps(self.student.data, indent=4))

        self.serializer = UserSerializer2(self.user)

        self.user.student.major.add(Major.objects.get(name="Test Active Major"))
        self.user.student.school.add(School.objects.get(name="Test School"))
        self.user.student.graduation_year = 2024

    def test_str_no_preferred_name(self):
        sample_response = {
            "pennid": 1,
            "first_name": "First",
            "last_name": "Last",
            "username": "student",
            "email": "test@test.com",
            "groups": [],
            "student": {
                "major": ["Test Active Major"],
                "school": ["Test School"],
            },
            "user_permissions": [],
            "product_permission": [],  # TODO: remove this after migrating to permissions in DLA
        }

        print(json.dumps(self.serializer.data, indent=4))
        self.assertEqual(self.serializer.data, sample_response)

    def test_update_major(self):
        sample_response = {
            "pennid": 1,
            "first_name": "First",
            "last_name": "Last",
            "username": "student",
            "email": "test@test.com",
            "groups": [],
            "student": {
                "major": ["Test Active Major"],
                "school": ["Test School"],
            },
            "user_permissions": [],
            "product_permission": [],  # TODO: remove this after migrating to permissions in DLA
        }

        print(json.dumps(self.serializer.data, indent=4))
        self.assertEqual(self.serializer.data, sample_response)


class UserSearchSerializerTestCase(TestCase):
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
        self.serializer = UserSearchSerializer(self.user)

        self.user_preferred_name = get_user_model().objects.create_user(
            pennid=2,
            username="student2",
            password="secret2",
            first_name="First2",
            last_name="Last2",
            email="test2@test.com",
            preferred_name="Preferred",
        )
        self.serializer_preferred_name = UserSearchSerializer(self.user_preferred_name)

    def test_str_no_preferred_name(self):
        sample_response = {
            "first_name": "First",
            "last_name": "Last",
            "username": "student",
        }
        self.assertEqual(self.serializer.data, sample_response)

    def test_str_preferred_name_provided(self):
        sample_response = {
            "first_name": "Preferred",
            "last_name": "Last2",
            "username": "student2",
        }
        self.assertEqual(self.serializer_preferred_name.data, sample_response)

# student serializer info / test using nested serializer editing
class StudentSerializerTestCaseOLD(TestCase):
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
        self.serializer = UserSearchSerializer(self.user)

        self.user_preferred_name = get_user_model().objects.create_user(
            pennid=2,
            username="student2",
            password="secret2",
            first_name="First2",
            last_name="Last2",
            email="test2@test.com",
            preferred_name="Preferred",
        )
        self.serializer_preferred_name = UserSearchSerializer(self.user_preferred_name)

    def test_str_no_preferred_name(self):
        sample_response = {
            "first_name": "First",
            "last_name": "Last",
            "username": "student",
        }
        self.assertEqual(self.serializer.data, sample_response)

    def test_str_preferred_name_provided(self):
        sample_response = {
            "first_name": "Preferred",
            "last_name": "Last2",
            "username": "student2",
        }
        self.assertEqual(self.serializer_preferred_name.data, sample_response)

class PhoneNumberSerializerTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            pennid=1,
            username="student",
            first_name="First",
            last_name="Last",
            email="test@example.com",
        )

        self.number1 = PhoneNumberModel.objects.create(
            user=self.user,
            phone_number="+12150001111",
            primary=False,
            verified=False,
            verification_code="123456",
            verification_timestamp=timezone.now(),
        )

        self.number2 = PhoneNumberModel.objects.create(
            user=self.user, phone_number="+12058869999", primary=True,
        )

        self.number3 = PhoneNumberModel.objects.create(
            user=self.user, phone_number="+16170031234", primary=False,
        )

    def test_create(self):
        # If this is your phone number I'm sorry
        data = {
            "phone_number": "+12154729463",
            "primary": True,
            "verified": True,
            "verification_code": "000000",
        }
        serializer = PhoneNumberSerializer(data=data, context={"request": FakeRequest(self.user)})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        phone_number = serializer.save()
        self.assertEqual(phone_number.user, self.user)
        self.assertFalse(phone_number.verified)
        self.assertFalse(phone_number.primary)
        self.assertNotEqual(phone_number.verification_code, "000000")
        # TODO: make sure sendSMSVerification is called

    def test_create_same_phone(self):
        data = {
            "phone_number": "+12150001111",
            "primary": True,
            "verified": True,
            "verification_code": "000000",
        }
        serializer = PhoneNumberSerializer(data=data, context={"request": FakeRequest(self.user)})

        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_update_verified(self):
        data = {
            "verification_code": "123456",
        }
        serializer = PhoneNumberSerializer(
            self.number1, data=data, context={"request": FakeRequest(self.user)}
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertTrue(self.number1.verified)
        self.assertTrue(self.number1.primary)

    def test_update_unverified(self):
        data = {
            "verification_code": "000123",
        }
        serializer = PhoneNumberSerializer(
            self.number1, data=data, context={"request": FakeRequest(self.user)}
        )

        if serializer.is_valid(raise_exception=True):
            with self.assertRaises(serializers.ValidationError):
                serializer.save()

        self.assertFalse(self.number1.verified)
        self.assertFalse(self.number1.primary)

    def test_update_primary(self):
        data = {
            "primary": True,
        }
        serializer = PhoneNumberSerializer(
            self.number3, data=data, context={"request": FakeRequest(self.user)}
        )
        self.assertTrue(serializer.is_valid())
        # print("before save")

        serializer.save()
        self.number2.refresh_from_db()
        self.number3.refresh_from_db()

        self.assertTrue(self.number3.primary)
        self.assertFalse(self.number2.primary)

    def test_verification_timeout(self):
        data = {
            "phone_number": "+12154729463",
            "primary": True,
            "verified": True,
            "verification_code": "000000",
        }
        serializer = PhoneNumberSerializer(data=data, context={"request": FakeRequest(self.user)})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        phone_number = serializer.save()

        phone_number.verification_timestamp = timezone.now() - (
            datetime.timedelta(0, 0, 0, 0, User.VERIFICATION_EXPIRATION_MINUTES + 1)
        )
        phone_number.verification_code = "000000"
        data = {
            "verification_code": "000000",
        }
        serializer = PhoneNumberSerializer(
            phone_number, data=data, context={"request": FakeRequest(self.user)}
        )
        if serializer.is_valid(raise_exception=True):
            with self.assertRaises(serializers.ValidationError):
                serializer.save()
        self.assertFalse(phone_number.verified)


class EmailSerializerTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            pennid=1,
            username="student",
            password="secret",
            first_name="First",
            last_name="Last",
            email="test@test.com",
        )
        self.email1 = Email.objects.create(
            user=self.user,
            email="example@test.com",
            primary=True,
            verification_timestamp=timezone.now(),
        )
        self.email2 = Email.objects.create(
            user=self.user,
            email="example2@test.com",
            primary=False,
            verification_code="123456",
            verification_timestamp=timezone.now(),
        )

    def test_create(self):
        data = {
            "email": "test@example.com",
            "primary": True,
            "verified": True,
            "verification_code": "000000",
        }
        serializer = EmailSerializer(data=data, context={"request": FakeRequest(self.user)})
        self.assertTrue(serializer.is_valid())
        email = serializer.save()
        self.assertEqual(email.user, self.user)
        self.assertFalse(email.verified)
        self.assertFalse(email.primary)
        self.assertNotEqual(email.verification_code, "000000")

    def test_update_verified(self):
        data = {
            "email": "example2@test.com",
            "verification_code": "123456",
        }
        serializer = EmailSerializer(
            self.email2, data=data, context={"request": FakeRequest(self.user)}
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertTrue(self.email2.verified)
        self.assertTrue(self.email2.primary)

    def test_update_unverified(self):
        data = {
            "email": "example2@test.com",
            "verification_code": "000123",
        }
        serializer = EmailSerializer(
            self.email2, data=data, context={"request": FakeRequest(self.user)}
        )

        if serializer.is_valid(raise_exception=True):
            with self.assertRaises(serializers.ValidationError):
                serializer.save()

        self.assertFalse(self.email2.verified)
        self.assertFalse(self.email2.primary)

    def test_update_primary(self):
        data = {
            "email": "example2@test.com",
            "primary": True,
        }
        serializer = EmailSerializer(
            self.email2, data=data, context={"request": FakeRequest(self.user)}
        )
        self.assertTrue(serializer.is_valid())

        serializer.save()

        self.email1.refresh_from_db()
        self.email2.refresh_from_db()

        self.assertTrue(self.email2.primary)
        self.assertFalse(self.email1.primary)

    def test_verification_timeout(self):
        data = {
            "email": "test@example.com",
            "primary": True,
            "verified": True,
            "verification_code": "000000",
        }
        serializer = EmailSerializer(data=data, context={"request": FakeRequest(self.user)})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        email = serializer.save()

        email.verification_timestamp = timezone.now() - (
            datetime.timedelta(0, 0, 0, 0, User.VERIFICATION_EXPIRATION_MINUTES + 1)
        )
        email.verification_code = "000000"
        data = {
            "email": "test@example.com",
            "verification_code": "000000",
        }
        serializer = EmailSerializer(email, data=data, context={"request": FakeRequest(self.user)})
        if serializer.is_valid(raise_exception=True):
            with self.assertRaises(serializers.ValidationError):
                serializer.save()
        self.assertFalse(email.verified)
