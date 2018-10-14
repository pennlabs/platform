from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    date_joined = models.DateTimeField(_('date_joined'), auto_now_add=True)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_superuser = models.BooleanField(_('is_superuser'), default=False)
    name = models.CharField(_('name'), max_length=255, blank=True)
    major = models.CharField(_('major'), max_length=255, blank=True)
    school = models.CharField(_('school'), max_length=255, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_name(self):
        """
        Returns the name for the user.
        """
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to the user.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
