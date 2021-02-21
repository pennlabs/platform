from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Email, Major, PhoneNumberModel, School, Student


class MajorModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            pennid=1, username="student", first_name="first", last_name="last", password="secret"
        )

        self.major_name = "Test Major"
        self.major = Major.objects.create(name=self.major_name)

    def test_str(self):
        self.assertEqual(str(self.major), f"{self.major_name}")


class SchoolModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            pennid=1, username="student", first_name="first", last_name="last", password="secret"
        )

        self.school_name = "Test School"
        self.school = School.objects.create(name=self.school_name)

    def test_str(self):
        self.assertEqual(str(self.school_name), f"{self.school}")


class StudentTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            pennid=1, username="student", password="secret"
        )
        self.student = Student.objects.create(user=self.user)

    def test_str(self):
        self.assertEqual(str(self.student), self.user.username)


class UserTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            pennid=1, username="student", first_name="first", last_name="last", password="secret"
        )

        self.user2 = get_user_model().objects.create_user(
            pennid=2,
            username="student2",
            password="secret2",
            first_name="first2",
            last_name="last2",
            preferred_name="prefer",
        )

    def test_get_preferred_name_none(self):
        self.assertEqual(self.user.get_preferred_name(), "first")

    def test_get_preferred_name_with_preferred(self):
        self.assertEqual(self.user2.get_preferred_name(), "prefer")


class PhoneNumberModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            pennid=1, username="student", first_name="first", last_name="last", password="secret"
        )

        self.phone_number = "+15550000000"
        self.number = PhoneNumberModel.objects.create(
            user=self.user, phone_number=self.phone_number, primary=True, verified=False
        )

    def test_str(self):
        self.assertEqual(str(self.number), f"{self.user} - {self.phone_number}")


class EmailTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            pennid=1, username="student", first_name="first", last_name="last", password="secret"
        )

        self.email_address = "example@example.com"
        self.email = Email.objects.create(
            user=self.user, email=self.email_address, primary=True, verified=False
        )

    def test_str(self):
        self.assertEqual(str(self.email), f"{self.user} - {self.email_address}")
