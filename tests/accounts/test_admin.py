from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from accounts.admin import StudentAdmin
from accounts.models import Student, User


class StudentAdminTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(pennid=1, username='user', first_name='First', last_name='Last')
        self.student = Student.objects.create(user=self.user)
        self.sa = StudentAdmin(Student, AdminSite())

    def test_username(self):
        self.assertEqual(self.sa.username(self.student), self.user.username)

    def test_first_name(self):
        self.assertEqual(self.sa.first_name(self.student), self.user.first_name)

    def test_last_name(self):
        self.assertEqual(self.sa.last_name(self.student), self.user.last_name)
