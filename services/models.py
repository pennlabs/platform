from django.db import models
from api.models import Team


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.URLField()
    icon = models.URLField()
    notes = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    routes = models.ManyToManyField('Endpoint')

    def __str__(self):
        return self.name


class Endpoint(models.Model):
    url = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.url


class Update(models.Model):
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.title
