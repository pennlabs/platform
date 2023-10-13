from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.shortcuts import redirect
from django.urls import reverse

from announcements.models import (
    Audience,
    Announcement
)

admin.site.register(Audience)
admin.site.register(Announcement)
