from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Student


class StudentTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            pennid=1, username="student", password="secret"
        )
        self.student = Student.objects.create(user=self.user)

    def test_str(self):
        self.assertEqual(str(self.student), self.user.username)
