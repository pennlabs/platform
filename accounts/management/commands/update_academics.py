from django.core.management import BaseCommand

from accounts.update_majors import update_all_majors
from accounts.update_schools import update_all_schools


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        update_all_majors()
        update_all_schools()

        self.stdout.write("Updated active schools and major in database.")
        self.stdout.write("Updated active schools and majors in database.")
