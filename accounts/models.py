import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    # implicit username, email, first_name, and last_name fields
    # from AbstractUser that contains the user's PennKey
    pennid = models.IntegerField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    preferred_name = models.CharField(max_length=225, blank=True)


class Student(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING)
    major = models.CharField(max_length=255, blank=True)
    school = models.CharField(max_length=255, blank=True)
    graduation_year = models.IntegerField(null=True)

    def __str__(self):
        return self.user.username


class Email(models.Model):
    user = models.ForeignKey(get_user_model(), related_name="emails", on_delete=models.CASCADE)
    email = models.EmailField()
    # whether this email is the primary email
    primary_email = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)


class PhoneNumber(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    phone_number = PhoneNumberField()
    primary_number = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
