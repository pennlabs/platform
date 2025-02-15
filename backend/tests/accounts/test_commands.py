from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from accounts.models import Major, School, Student


class UpdateMajorsTestCase(TestCase):
    def test_update_academics(self):
        call_command("update_academics")
        self.assertNotEqual(0, Major.objects.all().count())
        self.assertNotEqual(0, School.objects.all().count())


class PopulateUsersTestCase(TestCase):
    def test_populate_users(self):
        call_command("populate_users")
        self.assertTrue(get_user_model().objects.all().count() > 0)
        self.assertTrue(Major.objects.all().count() > 0)
        self.assertTrue(Student.objects.all().count() > 0)

    def test_populate_twice(self):
        call_command("populate_users")
        call_command("populate_users")
        self.assertEqual(get_user_model().objects.all().count(), 10)
