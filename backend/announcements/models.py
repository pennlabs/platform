from django.db import models

class Audience(models.Model):
    """
    Represents a product that an announcement is intended for.
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

    name = models.CharField(choices=AUDIENCE_CHOICES, max_length=20)

    def __str__(self):
        return self.name

class Announcement(models.Model):
    """
    Represents an announcement for any of the Penn Labs services.
    """

    ANNOUNCEMENT_BANNER = 1
    ANNOUNCEMENT_ISSUE = 2
    ANNOUNCEMENT_NOTICE = 3

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
    announcement_type = models.IntegerField(
        choices=ANNOUNCEMENT_CHOICES,
        default=ANNOUNCEMENT_NOTICE,
    )
    audiences = models.ManyToManyField("Audience", related_name="announcements")
    release_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"[{self.get_announcement_type_display()} for {','.join([audience.name for audience in self.audiences.all()])}] starting at {self.release_time.strftime('%m-%d-%Y %H:%M:%S')} {f'''to {self.end_time.strftime('%m-%d-%Y %H:%M:%S')}''' if self.end_time else ''} | {f'{self.title}: ' if self.title else ''} {self.message}"
