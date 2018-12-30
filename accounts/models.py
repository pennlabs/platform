from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    major = models.CharField(max_length=255, blank=True)
    school = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.student.save()


class Application(models.Model):
    redirect_uri = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    maintainer = models.CharField(max_length=255)
    revoked = models.BooleanField(default=False)

    def __str__(self):
        return self.name
