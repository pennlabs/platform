from django.core.management import call_command
from django.test import TestCase

from accounts.models import Major, School


class UpdateMajorsTestCase(TestCase):
    def test_update_academics(self):
        call_command("update_academics")

        self.assertTrue(Major.objects.all().count() != 0)
        self.assertTrue(School.objects.all().count() != 0)
