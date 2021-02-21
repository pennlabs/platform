import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from accounts.models import School


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # scrapes majors from the official penn catalog of all programs
        # source = requests.get("https://catalog.upenn.edu/programs/").text
        source = requests.get("https://catalog.upenn.edu/programs/").text

        soup = BeautifulSoup(source, "lxml")

        # iterate through all list tags with "item" in the class (all programs)
        school_list = soup.find("div", id="cat11list")
        for curr_school in school_list.find_all("div"):
            school_name = curr_school.text
            # create new school entry if it does not already exist
            if School.objects.filter(name=school_name).count() == 0:
                School.objects.create(name=school_name)
