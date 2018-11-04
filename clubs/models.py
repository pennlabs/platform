from django.db import models


class Club(models.Model):
    name = models.CharField(max_length=255)
    route = models.CharField(max_length=255)
    founded = models.DateTimeField()
    verified = models.BooleanField()
    contact = models.EmailField()
    description = models.TextField()


class Event(models.Model):
    name = models.CharField(max_length=255)
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING)
    time = models.DateTimeField()
    location = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField()
