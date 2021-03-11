from django.core.management import BaseCommand

from accounts.update_majors import update_majors
from accounts.update_schools import update_schools


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        update_majors()
        update_schools()

        self.stdout.write("Updated active schools and major in database.")
