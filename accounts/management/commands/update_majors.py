from abc import ABC

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from accounts.models import Major
import requests


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # scrapes majors from the official penn catalog of all programs
        source = requests.get("https://catalog.upenn.edu/programs/").text

        soup = BeautifulSoup(source, "lxml")

        # iterate through all list tags with "item" in the class (all programs)
        for program in soup.find_all("li", class_=lambda value: value and value.startswith("item")):
            # grab the href path
            major_url = program.find("a", href=True)
            # grab the major name
            major_name = program.find("span", class_="title").text

            # filter for undergraduate programs
            if "undergraduate" in major_url["href"]:
                # create new major entry if it does not already exist
                if Major.objects.filter(name=major_name).count() == 0:
                    # print(major_name)
                    Major.objects.create(name=major_name)