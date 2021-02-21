import os
from unittest import skipIf

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.admin import MajorAdmin, SchoolAdmin, StudentAdmin
from accounts.models import Major, School, Student, User


class MajorAdminTestCase(TestCase):
    def setUp(self):
        self.major_active = Major.objects.create(name="Test Active Major", is_active=True)
        self.major_inactive = Major.objects.create(name="Test Inactive Major", is_active=False)

        self.major_admin = MajorAdmin(Major, AdminSite())

    def test_major_active(self):
        self.assertEqual(self.major_admin.name(self.major_active), self.major_active.name)

    def test_major_inactive(self):
        self.assertEqual(self.major_admin.name(self.major_inactive), self.major_inactive.name)


class SchoolAdminTestCase(TestCase):
    def setUp(self):
        self.school1 = School.objects.create(name="Test School")

        self.school_admin = SchoolAdmin(School, AdminSite())

    def test_school(self):
        self.assertEqual(self.school_admin.name(self.school1), self.school1.name)


class StudentAdminTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            pennid=1, username="user", first_name="First", last_name="Last"
        )
        self.student = Student.objects.create(user=self.user)
        self.student_admin = StudentAdmin(Student, AdminSite())

    def test_username(self):
        self.assertEqual(self.student_admin.username(self.student), self.user.username)

    def test_first_name(self):
        self.assertEqual(self.student_admin.first_name(self.student), self.user.first_name)

    def test_last_name(self):
        self.assertEqual(self.student_admin.last_name(self.student), self.user.last_name)


class LabsAdminTestCase(TestCase):
    check = os.environ.get("DJANGO_SETTINGS_MODULE", "") == "Platform.settings.development"

    @skipIf(check, "This test doesn't matter in development")
    def test_admin_not_logged_in(self):
        response = self.client.get(reverse("admin:login") + "?next=/admin/")
        redirect = reverse("accounts:login") + "?next=/admin/"
        self.assertRedirects(response, redirect, fetch_redirect_response=False)

    def test_admin_logged_in(self):
        get_user_model().objects.create_user(
            pennid=1, username="user", password="password", is_staff=True
        )
        self.client.login(username="user", password="password")
        response = self.client.get(reverse("admin:login") + "?next=/admin/")
        redirect = "/admin/"
        self.assertRedirects(response, redirect, fetch_redirect_response=False)
