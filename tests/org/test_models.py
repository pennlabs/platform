import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Student
from org.models import Member, Role, Team


class TeamTestCase(TestCase):
    def setUp(self):
        Team.objects.create(name='Directors', description='Important people',
                            order=1)
        Team.objects.create(name='Platform', description='Important stuff',
                            order=2)
        Team.objects.create(name='Android', description='Important information',
                            order=3)

    def test_str(self):
        self.assertEqual(str(Team.objects.all()[0]), 'Directors')

    def test_order(self):
        directors = Team.objects.get(name='Directors')
        platform = Team.objects.get(name='Platform')
        android = Team.objects.get(name='Android')
        first = Team.objects.all()[0]
        second = Team.objects.all()[1]
        third = Team.objects.all()[2]
        self.assertEqual(directors, first)
        self.assertEqual(platform, second)
        self.assertEqual(android, third)


class RoleTestCase(TestCase):
    def setUp(self):
        Role.objects.create(name='Co-Director', description='Important people', order=1)
        Role.objects.create(name='Backend Engineer', description='Important stuff', order=2)
        Role.objects.create(name='Frontend Engineer', description='Important stuff', order=3)

    def test_str(self):
        self.assertEqual(str(Role.objects.all()[0]), 'Co-Director')

    def test_order(self):
        """
        Test custom ordering
        """
        director = Role.objects.get(name='Co-Director')
        be_engineer = Role.objects.get(name='Backend Engineer')
        fe_engineer = Role.objects.get(name='Frontend Engineer')
        first = Role.objects.all()[0]
        second = Role.objects.all()[1]
        third = Role.objects.all()[2]
        self.assertEqual(director, first)
        self.assertEqual(be_engineer, second)
        self.assertEqual(fe_engineer, third)


class MemberTestCase(TestCase):
    def setUp(self):
        self.member = get_user_model().objects.create_user(username='member', password='secret')
        Student.objects.create(user=self.member)
        Member.objects.create(student=self.member.student, year_joined=datetime.date.today())

    def test_str(self):
        self.assertEqual(str(self.member.student.member), 'member')
