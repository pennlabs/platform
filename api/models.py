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
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    bio = models.TextField()
    location = models.CharField(max_length=255)
    teams = models.ManyToManyField(Team)
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


class Update(models.Model):
    product = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    body = models.TextField()


class Event(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    link = models.URLField()
    free_food = models.BooleanField()
