import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import serializers

from accounts.models import Email, Major, PhoneNumber, School, User
from accounts.serializers import (
    EmailSerializer,
    MajorSerializer,
    PhoneNumberSerializer,
    SchoolSerializer,
    StudentSerializer,
    UserSearchSerializer,
    UserSerializer,
)


class FakeRequest:
    def __init__(self, user):
        self.user = user


class SchoolSerializerTestCase(TestCase):
    def setUp(self):
        self.school = School.objects.create(name="Test School")

        self.serializer = SchoolSerializer(self.school)

    def test_active_major(self):
        sample_response = {"id": self.school.id, "name": self.school.name}
        self.assertEqual(self.serializer.data, sample_response)


class MajorSerializerTestCase(TestCase):
    def setUp(self):
        self.major_active = Major.objects.create(name="Test Active Major", is_active=True)
        self.major_inactive = Major.objects.create(
            name="Test Inactive Major", degree_type="PHD", is_active=False
        )

        self.serializer_active = MajorSerializer(self.major_active)
        self.serializer_inactive = MajorSerializer(self.major_inactive)

    def test_active_major(self):
        sample_response = {
            "id": self.major_active.id,
            "name": self.major_active.name,
            "degree_type": self.major_active.degree_type,
        }
        self.assertEqual(self.serializer_active.data, sample_response)

    def test_inactive_major(self):
        sample_response = {
            "id": self.major_inactive.id,
            "name": self.major_inactive.name,
            "degree_type": self.major_inactive.degree_type,
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
        self.active_major_1 = Major.objects.create(name="Test Active Major", is_active=True)
        self.active_major_2 = Major.objects.create(
            name="Test Active Major 2", degree_type="PHD", is_active=True
        )

        self.school = School.objects.create(name="Test School")

        self.user.student.major.add(Major.objects.get(name="Test Active Major"))
        self.user.student.major.add(Major.objects.get(name="Test Active Major 2"))
        self.user.student.school.add(School.objects.get(name="Test School"))
        self.serializer = StudentSerializer(self.user.student)

    def test_two_majors(self):
        sample_response = {
            "major": [
                {
                    "id": self.active_major_1.id,
                    "name": self.active_major_1.name,
                    "degree_type": self.active_major_1.degree_type,
                },
                {
                    "id": self.active_major_2.id,
                    "name": self.active_major_2.name,
                    "degree_type": self.active_major_2.degree_type,
                },
            ],
            "school": [{"id": self.school.id, "name": self.school.name}],
        }

        self.assertEqual(self.serializer.data["major"], sample_response["major"])
        self.assertEqual(self.serializer.data["school"], sample_response["school"])

    def test_remove_major(self):
        sample_response = {
            "major": [
                {
                    "id": self.active_major_1.id,
                    "name": self.active_major_1.name,
                    "degree_type": self.active_major_1.degree_type,
                }
            ],
            "school": [{"id": self.school.id, "name": self.school.name}],
        }

        self.user.student.major.remove(self.active_major_2)

        self.assertEqual(self.serializer.data["major"], sample_response["major"])
        self.assertEqual(self.serializer.data["school"], sample_response["school"])

    def test_remove_school(self):
        sample_response = {
            "major": [
                {
                    "id": self.active_major_1.id,
                    "name": self.active_major_1.name,
                    "degree_type": self.active_major_1.degree_type,
                },
                {
                    "id": self.active_major_2.id,
                    "name": self.active_major_2.name,
                    "degree_type": self.active_major_2.degree_type,
                },
            ],
            "school": [],
        }

        school_to_remove = School.objects.get(name="Test School")

        self.user.student.school.remove(school_to_remove)

        self.assertEqual(self.serializer.data["major"], sample_response["major"])
        self.assertEqual(self.serializer.data["school"], sample_response["school"])


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
        self.assertEqual(self.serializer.data["first_name"], "First")
        self.assertEqual(self.serializer.data["last_name"], "Last")

    def test_str_preferred_name_provided(self):
        self.assertEqual(self.serializer_preferred_name.data["first_name"], "Preferred")
        self.assertEqual(self.serializer_preferred_name.data["last_name"], "Last2")

    def test_update_preferred_valid_name(self):
        data = {
            "first_name": "new_preferred",
        }
        serializer = UserSerializer(self.user, data=data, partial=True)

        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(self.user.preferred_name, "new_preferred")
        self.assertEqual(self.user.first_name, "First")

    def test_preferred_same_as_first(self):
        data = {
            "first_name": "First2",
        }
        serializer = UserSerializer(self.user_preferred_name, data=data, partial=True)

        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(self.user_preferred_name.preferred_name, "")
        self.assertEqual(self.user_preferred_name.first_name, "First2")


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

        self.number1 = PhoneNumber.objects.create(
            user=self.user,
            value="+12150001111",
            primary=False,
            verified=False,
            verification_code="123456",
            verification_timestamp=timezone.now(),
        )

        self.number2 = PhoneNumber.objects.create(
            user=self.user,
            value="+12058869999",
            primary=True,
        )

        self.number3 = PhoneNumber.objects.create(
            user=self.user,
            value="+16170031234",
            primary=False,
        )

    def test_create(self):
        # If this is your phone number I'm sorry
        data = {
            "value": "+12154729463",
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
            "value": "+12150001111",
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
        self.number3.verified = True
        self.number3.save()

        data = {
            "primary": True,
        }
        serializer = PhoneNumberSerializer(
            self.number3, data=data, context={"request": FakeRequest(self.user)}
        )
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.number2.refresh_from_db()
        self.number3.refresh_from_db()

        self.assertTrue(self.number3.primary)
        self.assertFalse(self.number2.primary)

    def test_attempt_unverified_make_primary(self):
        data = {
            "primary": True,
        }
        serializer = PhoneNumberSerializer(
            self.number3, data=data, context={"request": FakeRequest(self.user)}
        )

        if serializer.is_valid(raise_exception=True):
            with self.assertRaises(serializers.ValidationError):
                serializer.save()

    def test_verification_timeout(self):
        data = {
            "value": "+12154729463",
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
            value="example@test.com",
            primary=True,
            verification_timestamp=timezone.now(),
        )
        self.email2 = Email.objects.create(
            user=self.user,
            value="example2@test.com",
            primary=False,
            verification_code="123456",
            verification_timestamp=timezone.now(),
        )

    def test_create(self):
        data = {
            "value": "test@example.com",
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
            "value": "example2@test.com",
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
            "value": "example2@test.com",
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
        self.email2.verified = True
        self.email2.save()

        data = {
            "value": "example2@test.com",
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

    def test_attempt_unverified_make_primary(self):
        data = {
            "value": "example2@test.com",
            "primary": True,
        }
        serializer = EmailSerializer(
            self.email2, data=data, context={"request": FakeRequest(self.user)}
        )

        if serializer.is_valid(raise_exception=True):
            with self.assertRaises(serializers.ValidationError):
                serializer.save()

    def test_verification_timeout(self):
        data = {
            "value": "test@example.com",
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
            "value": "test@example.com",
            "verification_code": "000000",
        }
        serializer = EmailSerializer(email, data=data, context={"request": FakeRequest(self.user)})
        if serializer.is_valid(raise_exception=True):
            with self.assertRaises(serializers.ValidationError):
                serializer.save()
        self.assertFalse(email.verified)
