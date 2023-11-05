from announcements.models import Announcement, Audience
from announcements.serializers import AnnouncementSerializer
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.utils import timezone


class AnnouncementsFilterTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.audience_clubs = Audience.objects.create(name=Audience.AUDIENCE_CLUBS)
        self.audience_ohq = Audience.objects.create(name=Audience.AUDIENCE_OHQ)
        self.announcement1 = Announcement.objects.create(
            title="Test message",
            message="This is a test",
            announcement_type=Announcement.ANNOUNCEMENT_NOTICE,
            release_time=timezone.datetime(
                year=1000, month=12, day=31, tzinfo=timezone.get_current_timezone()
            ),
            end_time=timezone.datetime(
                year=1001, month=12, day=31, tzinfo=timezone.get_current_timezone()
            ),
        )
        self.announcement2 = Announcement.objects.create(
            title="Test message 2",
            message="This is also a test",
            announcement_type=Announcement.ANNOUNCEMENT_NOTICE,
            end_time=timezone.datetime(
                year=3000, month=12, day=31, tzinfo=timezone.get_current_timezone()
            ),
        )
        self.announcement1.audiences.add(self.audience_clubs)
        self.announcement2.audiences.add(self.audience_ohq)

    def test_get_no_filter(self):
        response = self.client.get("/announcements/")
        self.assertIn(AnnouncementSerializer(self.announcement1).data, response.json())
        self.assertIn(AnnouncementSerializer(self.announcement2).data, response.json())

    def test_filter_active(self):
        response = self.client.get("/announcements/?active=true")
        self.assertNotIn(
            AnnouncementSerializer(self.announcement1).data, response.json()
        )
        self.assertIn(AnnouncementSerializer(self.announcement2).data, response.json())

    def test_filter_audience(self):
        response = self.client.get("/announcements/?audience=clubs")
        self.assertIn(AnnouncementSerializer(self.announcement1).data, response.json())
        self.assertNotIn(
            AnnouncementSerializer(self.announcement2).data, response.json()
        )


class AnnouncementsPermissionTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_invalid_permission(self):
        response = self.client.post(
            "/announcements/",
            {
                "title": "Maintenance Alert",
                "message": "We apologize for any inconvenience caused.",
                "audiences": [
                    "CLUBS",
                    "COURSE_PLAN",
                    "COURSE_ALERT"
                ],
            },
        )
        self.assertEqual(response.status_code, 403)


class AnnouncementsModifyTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        for x in [
            "MOBILE",
            "OHQ",
            "CLUBS",
            "COURSE_PLAN",
            "COURSE_REVIEW",
            "COURSE_ALERT",
        ]:
            Audience.objects.get_or_create(name=x)
        self.announcement = Announcement.objects.create(
            title="Test message",
            message="This is a test",
            announcement_type=Announcement.ANNOUNCEMENT_NOTICE,
            release_time=timezone.datetime(
                year=1000, month=12, day=31, tzinfo=timezone.get_current_timezone()
            ),
            end_time=timezone.datetime(
                year=1001, month=12, day=31, tzinfo=timezone.get_current_timezone()
            ),
        )
        self.user = get_user_model().objects.create(
            pennid=1,
            username="student",
            password="secret",
            first_name="First",
            last_name="Last",
            email="test@test.com",
            is_superuser=1,
        )
        self.client.force_login(self.user)

    def test_create_announcement(self):
        response = self.client.post(
            "/announcements/",
            {
                "title": "Maintenance Alert",
                "message": "We apologize for any inconvenience caused.",
                "audiences": ["CLUBS", "COURSE_PLAN", "COURSE_ALERT"],
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Announcement.objects.filter(title="Maintenance Alert").exists())

    def test_update_announcement(self):
        response = self.client.patch(
            f"/announcements/{self.announcement.id}/",
            {"title": "Wow!"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Announcement.objects.filter(title="Wow!").exists())
        self.assertFalse(Announcement.objects.filter(title="Test message").exists())

    def test_delete_announcement(self):
        response = self.client.delete(f"/announcements/{self.announcement.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Announcement.objects.filter(title="Test message").exists())
