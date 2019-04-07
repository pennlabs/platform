from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import PennAffiliation, ProductPermissions, Student


class PennAffiliationTestCase(TestCase):
    def setUp(self):
        self.affiliation = PennAffiliation.objects.create(name='student')

    def test_str(self):
        self.assertEqual(str(self.affiliation), self.affiliation.name)


class ProductPermissionsTestCase(TestCase):
    def setUp(self):
        self.product_permission = ProductPermissions.objects.create(id='platform_admin', name='Platform Admin')

    def test_str(self):
        self.assertEqual(str(self.product_permission), self.product_permission.name)


class StudentTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='student', password='secret')
        self.student = Student.objects.create(user=self.user)

    def test_str(self):
        self.assertEqual(str(self.student), self.user.username)
