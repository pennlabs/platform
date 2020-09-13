from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import PhoneNumberModel, Student


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

        self.number = PhoneNumberModel.objects.create(
            user=self.user, phone_number="+12150000000", primary_number=True, verified=False
        )

    def test_str(self):
        self.assertEqual(str(self.number), "+12150000000")
