from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings

from accounts.models import Major, Student


class UpdateMajorsTestCase(TestCase):
    def test_update(self):
        Major.objects.create(name="Test Active Major", is_active=True)
        Major.objects.create(name="Test Inactive Major", is_active=False)

        # populate database with majors scraped from penn's website
        call_command("update_academics")

        # check states of pre-added test majors
        self.assertEqual(Major.objects.get(name="Test Active Major").is_active, False)
        self.assertEqual(Major.objects.get(name="Test Inactive Major").is_active, False)

        Major.objects.create(name="Test Active Major 2", is_active=True)

        # test duplicate run database with majors scraped from penn's website
        call_command("update_academics")

        # check states of pre-added test majors
        self.assertEqual(Major.objects.get(name="Test Active Major").is_active, False)
        self.assertEqual(Major.objects.get(name="Test Active Major 2").is_active, False)
        self.assertEqual(Major.objects.get(name="Test Inactive Major").is_active, False)

class PopulateUsersTestCase(TestCase):

    @override_settings(IS_DEV_LOGIN=False)
    def test_no_effect_in_production(self):
        call_command("populate_users")
        self.assertEqual(len(get_user_model().objects.all()), 0)

    def test_populate_users(self):
        call_command("populate_users")
        self.assertTrue(len(get_user_model().objects.all()) > 0)
        self.assertTrue(len(Major.objects.all()) > 0)
        self.assertTrue(len(Student.objects.all()) > 0)
