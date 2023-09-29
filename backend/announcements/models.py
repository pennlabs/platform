from django.db import models
from django.contrib.postgres.fields import ArrayField


class Announcement(models.Model):
    """
    Represents an announcement in any of labs services.
    """

    AUDIENCE_MOBILE = "MOBILE"
    AUDIENCE_OHQ = "OHQ"
    AUDIENCE_CLUBS = "CLUBS"
    AUDIENCE_COURSE_PLAN = "COURSE_PLAN"
    AUDIENCE_COURSE_REVIEW = "COURSE_REVIEW"
    AUDIENCE_COURSE_ALERT = "COURSE_ALERT"

    AUDIENCE_CHOICES = [
        (AUDIENCE_MOBILE, "Penn Mobile"),
        (AUDIENCE_OHQ, "OHQ"),
        (AUDIENCE_CLUBS, "Penn Clubs"),
        (AUDIENCE_COURSE_PLAN, "Penn Course Plan"),
        (AUDIENCE_COURSE_REVIEW, "Penn Course Review"),
        (AUDIENCE_COURSE_ALERT, "Penn Course Alert"),
    ]

    ANNOUNCEMENT_BANNER = "BANNER"
    ANNOUNCEMENT_ISSUE = "ISSUE"
    ANNOUNCEMENT_NOTICE = "NOTICE"

    ANNOUNCEMENT_CHOICES = [
        (ANNOUNCEMENT_BANNER, "Banner"),
        (ANNOUNCEMENT_ISSUE, "Issue"),
        (ANNOUNCEMENT_NOTICE, "Notice"),
    ]

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    message = models.TextField()
    announcement_type = models.CharField(
        max_length=20,
        choices=ANNOUNCEMENT_CHOICES,
        default=ANNOUNCEMENT_NOTICE,
    )
    audience = ArrayField(
        models.CharField(max_length=20, choices=AUDIENCE_CHOICES), blank=True
    )
    schedule = ArrayField(
        ArrayField(
            models.DateTimeField(),
            size=2,
        ),
    )

    def __str__(self):
        return f"[{self.announcement_type}: {self.audience}] @ {self.schedule} {self.title} - {self.message}"
