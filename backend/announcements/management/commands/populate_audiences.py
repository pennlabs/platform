from announcements.models import Audience
from django.core.management import BaseCommand


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
