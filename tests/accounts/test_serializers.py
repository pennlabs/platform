import datetime

import pytz
from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from phonenumber_field.phonenumber import PhoneNumber

from accounts.models import Email, PhoneNumberModel, Student, User
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

