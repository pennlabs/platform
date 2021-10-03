import os
from unittest import skipIf

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.admin import StudentAdmin
from accounts.models import Student, User


class StudentAdminTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            pennid=1, username="user", first_name="First", last_name="Last"
        )
        self.student = self.user.student
        self.student_admin = StudentAdmin(Student, AdminSite())

    def test_username(self):
        self.assertEqual(self.student_admin.username(self.student), self.user.username)

    def test_first_name(self):
        self.assertEqual(
            self.student_admin.first_name(self.student), self.user.first_name
        )

    def test_last_name(self):
        self.assertEqual(
            self.student_admin.last_name(self.student), self.user.last_name
        )


class LabsAdminTestCase(TestCase):
    check = (
        os.environ.get("DJANGO_SETTINGS_MODULE", "") == "Platform.settings.development"
    )

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
