import os
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


def get_user_image_filepath(instance, fname):
    """
    Returns the provided User's profile picture image path. Maintains the
    file extension of the provided image file if it exists.
    """
    suffix = "." + fname.rsplit(".", 1)[-1] if "." in fname else ""
    return os.path.join("images", f"{instance.username}{suffix}")


class School(models.Model):
    """
    Represents a school at the University of Pennsylvania.
    """

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Major(models.Model):
    """
    Represents a major at the University of Pennsylvania.
    """

    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    DEGREE_BACHELOR = "BACHELORS"
    DEGREE_MASTER = "MASTERS"
    DEGREE_PHD = "PHD"
    DEGREE_PROFESSIONAL = "PROFESSIONAL"
    DEGREE_CHOICES = [
        (DEGREE_BACHELOR, "Bachelor's"),
        (DEGREE_MASTER, "Master's"),
        (DEGREE_PHD, "PhD"),
        (DEGREE_PROFESSIONAL, "Professional"),
    ]
    # fixed choices for degree type
    degree_type = models.CharField(
        max_length=20, choices=DEGREE_CHOICES, default=DEGREE_PROFESSIONAL
    )

    def __str__(self):
        return self.name


class User(AbstractUser):
    # implicit username, email, first_name, and last_name fields
    # from AbstractUser that contains the user's PennKey
    pennid = models.IntegerField(primary_key=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    preferred_name = models.CharField(max_length=225, blank=True)
    profile_pic = models.ImageField(
        upload_to=get_user_image_filepath, blank=True, null=True
    )

    VERIFICATION_EXPIRATION_MINUTES = 10

    def get_preferred_name(self):
        if self.preferred_name != "":
            return self.preferred_name
        else:
            return self.first_name

    def get_email(self):
        email = self.emails.filter(primary=True).first()
        return email.value if email else ""


class Student(models.Model):
    """
    Represents a Student at the University of Pennsylvania.
    """

    user = models.OneToOneField(
        get_user_model(), related_name="student", on_delete=models.DO_NOTHING
    )
    major = models.ManyToManyField(Major, blank=True)
    school = models.ManyToManyField(School, blank=True)
    graduation_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1740)], null=True
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def ensure_student_object(sender, instance, created, **kwargs):
    """
    This post_save hook triggers automatically when a User object is saved, and if no Student
    object exists for that User, it will create one
    """
    Student.objects.get_or_create(user=instance)


class Email(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="emails", on_delete=models.CASCADE
    )
    value = models.EmailField(unique=True)
    primary = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_timestamp = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.value}"


class PhoneNumber(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="phone_numbers", on_delete=models.CASCADE
    )
    value = PhoneNumberField(unique=True, blank=True, default=None)
    primary = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_timestamp = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.value}"
