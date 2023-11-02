from django.core.management import BaseCommand

from announcements.models import Audience


class Command(BaseCommand):
    def handle(self, *args, **options):
        for x in [
            "MOBILE",
            "OHQ",
            "CLUBS",
            "COURSE_PLAN",
            "COURSE_REVIEW",
            "COURSE_ALERT",
        ]:
            Audience.objects.get_or_create(name=x)
