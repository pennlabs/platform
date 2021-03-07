import requests
from bs4 import BeautifulSoup
from accounts.models import Major


def contains_filters(listed_filters, desired_filters=set(), excluded_filters=set()):
    # ensure no excluded filters appear
    for curr_filter in excluded_filters:
        if curr_filter in listed_filters:
            return False

    # ensure at least one desired filter appears
    for curr_filter in desired_filters:
        if curr_filter in listed_filters:
            return True

    return False


def update_majors():
    # scrapes majors from the official penn catalog of all programs
    source = requests.get("https://catalog.upenn.edu/programs/").text

    soup = BeautifulSoup(source, "lxml")

    bachelor_filter = "filter_6"
    master_filter = "filter_25"
    phd_filter = "filter_7"
    professional_filter = "filter_10"
    minor_filter = "filter_26"
    desired_filters = {bachelor_filter, master_filter, phd_filter, professional_filter}
    excluded_filters = {minor_filter}

    listed_majors = set()
    # iterate through all list tags with "item" in the class (all programs)
    for program in soup.find_all(
            "li", class_=lambda value: value and value.startswith("item ")
    ):
        curr_filter_list = program.attrs["class"]
        # check if entry meets relevant desired and excluded filter criteria
        if not contains_filters(
                curr_filter_list, desired_filters=desired_filters, excluded_filters=excluded_filters
        ):
            continue

        # grab the major name
        major_name = program.find("span", class_="title").text

        # create new major entry if it does not already exist
        if Major.objects.filter(name=major_name).count() == 0:
            # identify degree type
            if bachelor_filter in curr_filter_list:
                curr_degree_type = Major.DEGREE_BACHELOR
            elif master_filter in curr_filter_list:
                curr_degree_type = Major.DEGREE_MASTER
            elif phd_filter in curr_filter_list:
                curr_degree_type = Major.DEGREE_PHD
            else:
                curr_degree_type = Major.DEGREE_PROFESSIONAL

            Major.objects.create(name=major_name, is_active=True, degree_type=curr_degree_type)

        # keep track of found majors
        listed_majors.add(major_name)

    # iterate through existing majors and set active/inactive status
    for existing_major in Major.objects.all():
        existing_major.is_active = existing_major.name in listed_majors
        existing_major.save()
