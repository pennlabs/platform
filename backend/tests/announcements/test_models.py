from announcements.models import Announcement, Audience
from django.test import TestCase
from django.utils import timezone


class AudienceTestCase(TestCase):
    def setUp(self):
        self.audience_name = "CLUBS"
        self.audience = Audience.objects.create(name=Audience.AUDIENCE_CLUBS)

    def test_str(self):
        self.assertEqual(str(self.audience), self.audience_name)


class AnnouncementTestCase(TestCase):
    def setUp(self):
        self.audience_name = "CLUBS"
        self.title = "Test Announcement"
        self.message = "This is a test"
        self.announcement_type = "Issue"
        self.release_time = timezone.datetime(
            year=3000, month=12, day=31, tzinfo=timezone.get_current_timezone()
        )
        self.end_time = timezone.datetime(
            year=3001, month=1, day=1, tzinfo=timezone.get_current_timezone()
        )
        self.audience = Audience.objects.create(name=Audience.AUDIENCE_CLUBS)
        self.announcement = Announcement.objects.create(
            title=self.title,
            message=self.message,
            announcement_type=Announcement.ANNOUNCEMENT_ISSUE,
            release_time=self.release_time,
            end_time=self.end_time,
        )
        self.announcement.audiences.add(self.audience)

    def test_str(self):
        self.assertEqual(
            str(self.announcement),
            f"[{self.announcement_type} for {self.audience_name}] \
starting at {self.release_time.strftime('%m-%d-%Y %H:%M:%S')} to \
{self.end_time.strftime('%m-%d-%Y %H:%M:%S')} | {self.title}: {self.message}",
        )
