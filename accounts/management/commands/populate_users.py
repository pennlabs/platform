import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from accounts.models import User, Student, Major, Email, PhoneNumberModel

users = [
    {
        'role': ['student'],
        'first_name': 'Armaan',
        'last_name': 'Tobaccowalla',
        'student': {
            'degree': 'B',
            'major': ['Finance', 'Computer Science'],
            'school': ['Wharton', 'SEAS'],
            'graduation_year': 2022
        },
        'email': {
            'verified': True
        },
        'phone': {
            'verified': True
        }
    },
    {
        'group': ['student'],
        'first_name': 'Jay',
        'last_name': 'Vishwarupe',
        'student': {
            'degree': 'B',
            'major': ['Computer Science'],
            'school': ['SEAS'],
            'graduation_year': 2024
        },
        'email': {
            'verified': True
        },
        'phone': {
            'verified': True
        }
    },
    {
        'group': ['student'],
        'first_name': 'Rafa',
        'last_name': 'Marques',
        'student': {
            'degree': 'M',
            'major': ['Electrical Engineering'],
            'school': ['SEAS'],
            'graduation_year': 2023
        },
        'email': {
            'verified': False
        },
        'phone': {
            'verified': True
        }
    },
    {
        'group': ['student', 'employee'],
        'first_name': 'Peyton',
        'last_name': 'Walters',
        'student': {
            'degree': 'PhD',
            'major': ['Accounting'],
            'school': ['Wharton'],
            'graduation_year': 2025,
        },
        'email': {
            'verified': False
        },
        'phone': {
            'verified': False
        }
    },
    {
        'group': ['student'],
        'first_name': 'William',
        'last_name': 'Goeller',
        'preferred_name': 'Goeller',
        'student': {
            'degree': 'Submat',
            'major': ['Mathematics'],
            'school': ['College'],
            'graduation_year': 2021
        },
        'email': {
            'verified': False,
            'multiple': True
        },
        'phone': {
            'verified': True
        }
    },
    {
        'group': ['student', 'employee'],
        'first_name': 'Brandon',
        'last_name': 'Wang',
        'student': {
            'degree': 'B',
            'major': ['Nursing'],
            'school': ['Nursing'],
            'graduation_year': 2022
        },
        'email': {
            'verified': False
        },
        'phone': {
            'verified': False
        }
    },
    {
        'group': ['faculty', 'alumni'],
        'first_name': 'Amy',
        'last_name': 'Gutman',
        'email': {
            'verified': True
        },
        'phone': {
            'verified': True
        }
    },
    {
        'group': ['faculty', 'staff', 'alumni'],
        'first_name': 'Nakia',
        'last_name': 'Rimmer',
        'email': {
            'verified': False
        },
        'phone': {
            'verified': True
        }
    },
    {
        'group': ['faculty', 'staff'],
        'first_name': 'Rajiv',
        'last_name': 'Gandhi',
        'email': {
            'verified': True
        },
        'phone': {
            'verified': True
        }
    },
    {
        'group': ['student'],
        'first_name': 'Marcus',
        'last_name': 'Goldman',
        'preferred_name': 'Samuel Sachs',
        'student': {
            'degree': 'P',
            'major': ['Finance'],
            'school': ['Wharton'],
            'graduation_year': 2023
        },
        'email': {
            'verified': True,
            'multiple': True
        },
        'phone': {
            'verified': True
        }
    }
]

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for i, user in enumerate(users):
            if not settings.IS_DEV_LOGIN:
                break
            # User.objects.all().delete()
            username = (user['first_name'].strip() + user['last_name'].strip()).lower()
            school = user['student']['school'][0].lower() + "." if 'student' in user else ""
            email_address = f"{user['first_name'].strip().lower()}@{school}upenn.edu"
            first_name = user['first_name']
            last_name = user['last_name']
            pennid = i + 1
            password = f"password{pennid}"

            user_obj = get_user_model().objects.create(
                username=username,
                first_name = first_name,
                last_name = last_name,
                password=password
            )
            if 'preferred_name' in user:
                user_obj.preferred_name = user['preferred_name']
            user_obj.save()
            if 'student' in user:
                student_details = user['student']
                student = Student.objects.create(
                    user=user_obj,
                    graduation_year=student_details['graduation_year']
                )
                for major_name in student_details['major']:
                    major = Major.objects.get(name=major_name)
                    if major != None:
                        student.major.add(major)
                    else:
                        major = Major.objects.create(name=major_name)
                        if student_details['degree'] == 'B' or student_details['degree'] == 'Submat':
                            major.degree_type = major.DEGREE_BACHELOR
                        elif student_details['degree'] == 'P':
                            major.degree_type = major.DEGREE_PROFESSIONAL
                        elif student_details['degree'] == 'PhD':
                            major.degree_type = major.DEGREE_PHD
                        elif student_details['degree'] == 'M':
                            major.degree_type = major.DEGREE_MASTER
                        major.save()
                        student.major.add(major)
                        if student_details['degree'] == 'Submat':
                            major2 = Major.objects.create(name=major_name)
                            major2.degree_type = major.DEGREE_MASTER
                            major2.save()
                            student.major.add(major2)
                student.save()
            if 'email' in user:
                email_details = user['email']
                email = Email.objects.create(
                    user=user_obj,
                    email = email_address,
                    primary=True,
                    verified=email_details['verified']
                )
                email.save()
                if 'multiple' in email_details:
                    email2 =  Email.objects.create(
                        user=user_obj,
                        email=f"{user['last_name'].strip().lower()}@{school}upenn.edu",
                        primary=False
                    )
                    if email.details['verified']:
                        email2.verified = True
                    email2.save()

            if 'phone' in user:
                phone = PhoneNumberModel.objects.create(
                    user=user_obj,
                    phone_number= random.sample(range(10), 10),
                    verified=user['phone']['verified']
                )
                phone.save()

        self.stdout.write("Updated active schools and major in database.")