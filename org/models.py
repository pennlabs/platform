from django.db import models
from rest_framework import serializers
from accounts.models import User


class Team(models.Model):
    name = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    bio = models.TextField()
    location = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, null=True, blank=True)
    roles = models.ManyToManyField(Role)
    url = models.SlugField(unique=True, null=True)
    photo = models.URLField()
    linkedin = models.URLField()
    website = models.URLField()
    github = models.URLField()
    year_joined = models.DateField()
    alumnus = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
