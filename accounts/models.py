import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    affiliation = models.ManyToManyField('PennAffiliation')
    product_permission = models.ManyToManyField('ProductPermission')


class Student(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.DO_NOTHING)
    major = models.CharField(max_length=255, blank=True)
    school = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


class PennAffiliation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductPermission(models.Model):
    id = models.SlugField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
