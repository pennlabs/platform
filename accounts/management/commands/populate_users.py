import random
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from accounts.models import Email, Major, PhoneNumberModel, School, Student, User


users = [
    {
        "group": ["student"],
        "first_name": "Armaan",
        "last_name": "Tobaccowalla",
        "student": {
            "degree": "B",
            "major": ["Finance", "Computer Science"],
            "school": ["Wharton", "SEAS"],
            "graduation_year": 2022,
        },
        "email": {"verified": True},
        "phone": {"verified": True},
    },
    {
        "group": ["student"],
        "first_name": "Jay",
        "last_name": "Vishwarupe",
        "student": {
            "degree": "B",
            "major": ["Computer Science"],
            "school": ["SEAS"],
            "graduation_year": 2024,
        },
        "email": {"verified": True},
        "phone": {"verified": True},
    },
    {
        "group": ["student"],
        "first_name": "Rafa",
        "last_name": "Marques",
        "student": {
            "degree": "M",
            "major": ["Electrical Engineering"],
            "school": ["SEAS"],
            "graduation_year": 2023,
        },
        "email": {"verified": False},
        "phone": {"verified": True},
    },
    {
        "group": ["student", "employee"],
        "first_name": "Peyton",
        "last_name": "Walters",
        "student": {
            "degree": "PhD",
            "major": ["Accounting"],
            "school": ["Wharton"],
            "graduation_year": 2025,
        },
        "email": {"verified": False},
        "phone": {"verified": False},
    },
    {
        "group": ["student"],
        "first_name": "William",
        "last_name": "Goeller",
        "preferred_name": "Goeller",
        "student": {
            "degree": "Submat",
            "major": ["Mathematics"],
            "school": ["College"],
            "graduation_year": 2021,
        },
        "email": {"verified": False, "multiple": True},
        "phone": {"verified": True},
    },
    {
        "group": ["student", "employee"],
        "first_name": "Brandon",
        "last_name": "Wang",
        "student": {
            "degree": "B",
            "major": ["Nursing"],
            "school": ["Nursing"],
            "graduation_year": 2022,
        },
        "email": {"verified": False},
        "phone": {"verified": False},
    },
    {
        "group": ["student"],
        "first_name": "Marcus",
        "last_name": "Goldman",
        "preferred_name": "Samuel",
        "student": {
            "degree": "P",
            "major": ["Finance"],
            "school": ["Wharton"],
            "graduation_year": 2023,
        },
        "email": {"verified": True, "multiple": True},
        "phone": {"verified": True},
    },
    {
        "group": ["faculty", "alum"],
        "first_name": "Amy",
        "last_name": "Gutman",
        "email": {"verified": True},
        "phone": {"verified": True},
    },
    {
        "group": ["faculty", "staff", "alum"],
        "first_name": "Nakia",
        "last_name": "Rimmer",
        "email": {"verified": False},
        "phone": {"verified": True},
    },
    {
        "group": ["faculty", "staff"],
        "first_name": "Rajiv",
        "last_name": "Gandhi",
        "email": {"verified": True},
        "phone": {"verified": True},
    },
]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Forces repopulation")

    def handle(self, *args, **options):

        # check if already filled
        all_users = get_user_model().objects.all()
        if (
            len(all_users) == 10
            and len(all_users.filter(username="rajivgandhi")) > 0
            and (not options["force"])
        ):
            self.stdout.write("Users already populated")
            return

        # Main Command
        Student.objects.all().delete()
        Group.objects.all().delete()
        get_user_model().objects.all().delete()
        for x in ["alum", "employee", "faculty", "member", "staff", "student"]:
            Group.objects.get_or_create(name=x)

        for i, user in enumerate(users):
            username = (user["first_name"].strip() + user["last_name"].strip()).lower()
            school = user["student"]["school"][0].lower() + "." if "student" in user else ""
            email_address = f"{user['first_name'].strip().lower()}@{school}upenn.edu"
            first_name = user["first_name"]
            last_name = user["last_name"]
            pennid = i + 1
            password = f"password{pennid}"

            user_obj = User(
                pennid=pennid,
                username=username,
                uuid=uuid.uuid5(namespace=uuid.NAMESPACE_DNS, name=user["last_name"]),
                first_name=first_name,
                last_name=last_name,
                email=email_address,
                password=password,
            )

            if "preferred_name" in user:
                user_obj.preferred_name = user["preferred_name"]
            user_obj.save()
            user_obj = get_user_model().objects.all().get(username=username)
            member_group = Group.objects.get(name="member")
            user_obj.groups.add(member_group)
            for group in user["group"]:
                group_obj = Group.objects.get(name=group)
                user_obj.groups.add(group_obj)

            if "student" in user:
                student_details = user["student"]
                student = Student(
                    user=User.objects.all().get(username=username),
                    graduation_year=student_details["graduation_year"],
                )
                student.save()
                for major_name in student_details["major"]:
                    majors = Major.objects.filter(name=major_name)
                    if len(majors) != 0:
                        student.major.add(majors[0])
                    else:
                        major1 = Major(name=major_name)
                        if (
                            student_details["degree"] == "B"
                            or student_details["degree"] == "Submat"
                        ):
                            major1.degree_type = major1.DEGREE_BACHELOR
                        elif student_details["degree"] == "P":
                            major1.degree_type = major1.DEGREE_PROFESSIONAL
                        elif student_details["degree"] == "PhD":
                            major1.degree_type = major1.DEGREE_PHD
                        elif student_details["degree"] == "M":
                            major1.degree_type = major1.DEGREE_MASTER
                        major1.save()
                        student.major.add(major1)
                    if student_details["degree"] == "Submat":
                        major2 = Major(name="Physics")
                        major2.degree_type = major2.DEGREE_MASTER
                        major2.save()
                        student.major.add(major2)
                    for school_name in student_details["school"]:
                        schools = School.objects.filter(name=school_name)
                        if len(schools) != 0:
                            student.school.add(schools[0])
                        else:
                            school = School(name=school_name)
                            school.save()
                            student.school.add(school)
                student.save()
            if "email" in user:
                email_details = user["email"]
                email = Email(
                    user=User.objects.all().get(username=username),
                    value=email_address,
                    primary=True,
                    verified=email_details["verified"],
                )
                email.save()
                if "multiple" in email_details:
                    email2 = Email(
                        user=User.objects.all().get(username=username),
                        value=f"{user['last_name'].strip().lower()}@{school}upenn.edu",
                        primary=False,
                    )
                    email2.save()
            if "phone" in user:
                number = ""
                for _ in range(10):
                    number += str(random.randint(0, 9))
                phone = PhoneNumberModel(
                    user=User.objects.all().get(username=username),
                    value=number,
                    primary=True,
                    verified=user["phone"]["verified"],
                )
                phone.save()
            user_obj.save()

        self.stdout.write("Users populated")
