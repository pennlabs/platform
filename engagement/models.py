from django.db import models
from accounts.models import User


class Club(models.Model):
    id = models.SlugField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    verified = models.BooleanField()
    founded = models.DateField(null=True)
    fact = models.CharField(max_length=255)
    size = models.IntegerField()
    email = models.EmailField()
    facebook = models.URLField(null=True)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Event(models.Model):
    name = models.CharField(max_length=255)
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    url = models.URLField()
    image_url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.name
