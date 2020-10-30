import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Major(models.Model):
    """
    Represents a school (ex: Engineering, Wharton, etc).
    """

    # add boolean field for active/inactive and if not found through scrape, set it false

    # boolean field for whether major is currently active/inactive
    name = models.TextField(primary_key=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    # implicit username, email, first_name, and last_name fields
    # from AbstractUser that contains the user's PennKey
    pennid = models.IntegerField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    preferred_name = models.CharField(max_length=225, blank=True)

    VERIFICATION_EXPIRATION_MINUTES = 10

    def get_preferred_name(self):
        if self.preferred_name != "":
            return self.preferred_name
        else:
            return self.first_name


class Student(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING)
    # major = models.CharField(max_length=255, blank=True)
    major = models.ManyToManyField(Major)
    school = models.CharField(max_length=255, blank=True)
    graduation_year = models.IntegerField(null=True)

    def __str__(self):
        return self.user.username


class Email(models.Model):
    user = models.ForeignKey(get_user_model(), related_name="emails", on_delete=models.CASCADE)
    email = models.EmailField()
    primary = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_timestamp = models.DateTimeField(blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.email}"


class PhoneNumberModel(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="phone_numbers", on_delete=models.CASCADE
    )
    phone_number = PhoneNumberField(unique=True, blank=True, default=None)
    primary = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_timestamp = models.DateTimeField(blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.phone_number}"
