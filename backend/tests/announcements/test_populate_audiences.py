from announcements.models import Audience
from django.core.management import call_command
from django.test import TestCase


class PopulateAudiencesTestCase(TestCase):
    def test_populate_audiences(self):
        call_command("populate_audiences")
        self.assertTrue(Audience.objects.all().count() > 0)

    def test_populate_twice(self):
        call_command("populate_audiences")
        count = Audience.objects.all().count()
        call_command("populate_audiences")
        self.assertEqual(Audience.objects.all().count(), count)
