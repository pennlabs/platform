import json
import random

from django.contrib.auth.models import Group
from django.core.management import BaseCommand, call_command

from announcements.models import Audience


with open("accounts/data/users.json") as f:
    users = json.load(f)["users"]


class Command(BaseCommand):

    def handle(self, *args, **options):
        for x in ["MOBILE", "OHQ", "CLUBS", "COURSE_PLAN", "COURSE_REVIEW", "COURSE_ALERT"]:
            Audience.objects.get_or_create(name=x)