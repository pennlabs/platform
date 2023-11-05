from announcements.models import Announcement, Audience
from announcements.serializers import AnnouncementSerializer, AudienceSerializer
from django.test import TestCase
from django.utils import timezone


class AudienceSerializerTestCase(TestCase):
    def setUp(self):
        self.audience = Audience.objects.create(name=Audience.AUDIENCE_CLUBS)
        self.serializer = AudienceSerializer(self.audience)

    def test_serializer(self):
        data = {"name": self.audience.name}
        self.assertEqual(self.serializer.data, data)


class AnnouncementSerializerTestCase(TestCase):
    def setUp(self):
        self.audience_clubs = Audience.objects.create(name=Audience.AUDIENCE_CLUBS)
        self.audience_ohq = Audience.objects.create(name=Audience.AUDIENCE_OHQ)
        self.announcement = Announcement.objects.create(
            title="Test message",
            message="This is a test",
            announcement_type=Announcement.ANNOUNCEMENT_NOTICE,
            release_time=timezone.datetime(
                year=3000, month=12, day=31, tzinfo=timezone.get_current_timezone()
            ),
        )
        self.announcement.audiences.add(self.audience_clubs)
        self.announcement.audiences.add(self.audience_ohq)
        self.serializer = AnnouncementSerializer(self.announcement)

    def test_serializer(self):
        data = {
            "id": self.announcement.id,
            "title": self.announcement.title,
            "message": self.announcement.message,
            "announcement_type": self.announcement.announcement_type,
            "release_time": self.announcement.release_time.isoformat(),
            "end_time": None,
            "audiences": [Audience.AUDIENCE_CLUBS, Audience.AUDIENCE_OHQ],
        }
        self.assertEqual(self.serializer.data, data)
