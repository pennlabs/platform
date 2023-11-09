from announcements.models import Audience
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for audience_name, _ in Audience.AUDIENCE_CHOICES:
            Audience.objects.get_or_create(name=audience_name)
