from django.db import models


class Club(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    verified = models.BooleanField()
    founded = models.DateField(null=True)
    email = models.EmailField()
    facebook = models.URLField(null=True)

    def __str__(self):
        return self.name


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
