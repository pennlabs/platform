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
    preferred_name = models.CharField(max_length=100, blank=True)

class Student(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING)
    major = models.CharField(max_length=255, blank=True)
    school = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

class Email(models.Model):
    # optional additional user emails 
    email = models.EmailField()
    user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING, through='EmailVerification')

class EmailVerification(models.Model):
    # through model to keep track of whether email was verified
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)

class PhoneNumber(models.Model):
    # optional user phone numbers
    phone_number = PhoneNumberField()
    user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING, through='PhoneNumberVerification')

class PhoneNumberVerification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    email = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)