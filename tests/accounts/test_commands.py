from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from accounts.models import Major, School, Student


class UpdateMajorsTestCase(TestCase):
    def test_update_academics(self):
        call_command("update_academics")

        self.assertTrue(Major.objects.all().count() != 0)
        self.assertTrue(School.objects.all().count() != 0)


class PopulateUsersTestCase(TestCase):
    def test_populate_users(self):
        call_command("populate_users")
        self.assertTrue(len(get_user_model().objects.all()) > 0)
        self.assertTrue(len(Major.objects.all()) > 0)
        self.assertTrue(len(Student.objects.all()) > 0)
