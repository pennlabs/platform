import json
import random

from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from accounts.models import Email, Major, PhoneNumber, School, User


with open("accounts/data/users.json") as f:
    users = json.load(f)["users"]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Forces repopulation")

    def handle(self, *args, **options):
        for x in ["alum", "employee", "faculty", "member", "staff", "student"]:
            Group.objects.get_or_create(name=x)
        for i, user in enumerate(users):
            username = (
                user["first_name"].strip().lower() + user["last_name"].strip().lower()
            )
            school = (
                user["student"]["school"][0].lower() + "." if "student" in user else ""
            )
            first_name = user["first_name"]
            last_name = user["last_name"]
            pennid = i + 1000
            email_address = f"{username}@{school}upenn.edu"
            password = f"password{pennid}"

            user_obj, created = User.objects.get_or_create(
                pennid=pennid,
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )

            if created:
                if "preferred_name" in user:
                    user_obj.preferred_name = user["preferred_name"]
                    user_obj.save()
                member_group = Group.objects.get(name="member")
                user_obj.groups.add(member_group)
                for group in user["group"]:
                    group_obj = Group.objects.filter(name=group).first()
                    if group_obj is not None:
                        user_obj.groups.add(group_obj)

                if "student" in user:
                    student_details = user["student"]
                    student = user_obj.student
                    student.graduation_year = student_details["graduation_year"]
                    student.save()
                    for major_name in student_details["major"]:
                        major = Major.objects.filter(name=major_name).first()
                        if major is not None:
                            student.major.add(major)
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
                        user=user_obj,
                        value=email_address,
                        primary=True,
                        verified=email_details["verified"],
                    )
                    email.save()
                    if "multiple" in email_details:
                        school = (
                            user["student"]["school"][0].lower() + "."
                            if "student" in user
                            else ""
                        )
                        email2 = Email(
                            user=User.objects.all().get(username=username),
                            value=f"{user['last_name'].strip().lower()}@{school}upenn.edu",
                            primary=False,
                        )
                        email2.save()
                if "phone" in user:
                    if user["phone"].get("invalid") is not None:
                        number = "555"
                        for _ in range(7):
                            number += str(random.randint(0, 9))
                    else:
                        number = ""
                        for _ in range(10):
                            number += str(random.randint(0, 9))

                    phone = PhoneNumber(
                        user=User.objects.all().get(username=username),
                        value=number,
                        primary=True,
                        verified=user["phone"]["verified"],
                    )
                    phone.save()
                user_obj.save()

        self.stdout.write("Users populated")
