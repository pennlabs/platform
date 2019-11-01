import datetime
import json

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Student
from org.models import Member, Role, Team
from org.serializers import TeamSerializer


class TeamSerializerTestCase(TestCase):
    def setUp(self):
        self.date = pytz.timezone('America/New_York').localize(datetime.datetime(2019, 1, 1))
        self.team = Team.objects.create(name='Platform', description='Important',
                                        order=2)
        self.director_role = Role.objects.create(name='Z-Director', description='Important people', order=1)
        self.backend_role = Role.objects.create(name='Backend Engineer', description='Important stuff', order=2)
        self.director = get_user_model().objects.create_user(pennid=1, username='z-director', password='secret',
                                                             date_joined=self.date)
        Student.objects.create(user=self.director)
        self.backend = get_user_model().objects.create_user(pennid=2, username='backend', password='secret',
                                                            date_joined=self.date)
        Student.objects.create(user=self.backend)
        self.director_member = Member.objects.create(student=self.director.student, year_joined=self.date,
                                                     team=self.team, url='director')
        self.director_member.roles.add(self.director_role)
        self.backend_member = Member.objects.create(student=self.backend.student, year_joined=self.date,
                                                    team=self.team, url='backend')
        self.backend_member.roles.add(self.backend_role)
        self.serializer = TeamSerializer(self.team)

    def test_get_members(self):
        with open('tests/org/team.json', 'r') as f:
            sample_response = json.load(f)
        self.assertEqual(self.serializer.data, sample_response)
