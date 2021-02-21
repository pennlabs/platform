from django.core.management import call_command
from django.test import TestCase

from accounts.models import Major


class UpdateMajorsTestCase(TestCase):
    def test_update(self):
        Major.objects.create(name="Test Active Major", is_active=True)
        Major.objects.create(name="Test Inactive Major", is_active=False)

        # populate database with majors scraped from penn's website
        call_command("update_majors")

        # check states of pre-added test majors
        self.assertEqual(Major.objects.get(name="Test Active Major").is_active, False)
        self.assertEqual(Major.objects.get(name="Test Inactive Major").is_active, False)

        Major.objects.create(name="Test Active Major 2", is_active=True)

        # test duplicate run database with majors scraped from penn's website
        call_command("update_majors")

        # check states of pre-added test majors
        self.assertEqual(Major.objects.get(name="Test Active Major").is_active, False)
        self.assertEqual(Major.objects.get(name="Test Active Major 2").is_active, False)
        self.assertEqual(Major.objects.get(name="Test Inactive Major").is_active, False)
