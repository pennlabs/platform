import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


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
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    preferred_name = models.CharField(max_length=225, blank=True)

    VERIFICATION_EXPIRATION_MINUTES = 10

    def get_preferred_name(self):
        if self.preferred_name != "":
            return self.preferred_name
        else:
            return self.first_name


class Student(models.Model):
    """
    Represents a Student at the University of Pennsylvania.
    """

    user = models.OneToOneField(
        get_user_model(), related_name="student", on_delete=models.DO_NOTHING
    )
    major = models.ManyToManyField(Major, null=True, blank=True)
    school = models.ManyToManyField(School, null=True, blank=True)
    graduation_year = models.PositiveIntegerField(validators=[MinValueValidator(1740)], null=True)

    def __str__(self):
        return self.user.username


class Email(models.Model):
    user = models.ForeignKey(get_user_model(), related_name="emails", on_delete=models.CASCADE)
    value = models.EmailField()
    primary = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_timestamp = models.DateTimeField(blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.value}"


class PhoneNumberModel(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="phone_numbers", on_delete=models.CASCADE
    )
    value = PhoneNumberField(unique=True, blank=True, default=None)
    primary = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_timestamp = models.DateTimeField(blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.value}"
