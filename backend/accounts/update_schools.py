import requests
from bs4 import BeautifulSoup

from accounts.models import School


# the catalog sits behind a bot challenge that blocks the default python-requests user agent
CATALOG_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    )
}


def update_all_schools():
    # scrapes schools from the official penn catalog of all programs
    source = requests.get(
        "https://catalog.upenn.edu/programs/", headers=CATALOG_HEADERS
    ).text

    soup = BeautifulSoup(source, "lxml")

    # iterate through all list tags with "item" in the class (all programs)
    school_list = soup.find("div", id="cat11list")
    if school_list is None:
        raise RuntimeError(
            "cat11list not found: catalog page changed or request was blocked"
        )
    for curr_school in school_list.find_all("div"):
        school_name = curr_school.text
        # create new school entry if it does not already exist
        School.objects.update_or_create(name=school_name)
