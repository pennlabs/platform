from django.core.management import BaseCommand
from accounts import update_majors
from accounts import update_schools


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        update_majors()
        update_schools()

        self.stdout.write("Updated active schools and major in database.")