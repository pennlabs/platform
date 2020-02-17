import requests
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Student


class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField(unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]


class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField(unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]


class Member(models.Model):
    student = models.OneToOneField(Student, on_delete=models.DO_NOTHING, null=True, blank=True)
    bio = models.TextField()
    job = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255)
    team = models.ForeignKey(
        Team, related_name="members", on_delete=models.DO_NOTHING, null=True, blank=True
    )
    roles = models.ManyToManyField(Role)
    url = models.SlugField(unique=True)
    photo = models.URLField()
    linkedin = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    year_joined = models.DateField()
    alumnus = models.BooleanField(default=False)

    def __str__(self):
        return self.student.user.username

    class Meta:
        ordering = ["student__user__first_name"]


@receiver(post_save, sender=Member, dispatch_uid="rebuild_website")
def rebuild_website(sender, instance, **kwargs):
    if settings.REBUILD_WEBHOOK_URL is not None:
        requests.post(settings.REBUILD_WEBHOOK_URL)
    else:
        print("Site rebuild triggered.")
