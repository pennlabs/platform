from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    major = models.CharField(max_length=255, blank=True)
    school = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=DjangoUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User.objects.create(user=instance)


@receiver(post_save, sender=DjangoUser)
def save_user_profile(sender, instance, **kwargs):
    instance.user.save()
