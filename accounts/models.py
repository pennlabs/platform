import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # implicit username, email, first_name, and last_name fields
    # from AbstractUser that contains the user's PennKey
    pennid = models.IntegerField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)


class Student(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING)
    major = models.CharField(max_length=255, blank=True)
    school = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username
