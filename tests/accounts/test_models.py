from django.contrib.auth.models import User
from django.test import TestCase


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student', password='secret')

    def test_str(self):
        self.assertEqual(str(self.user.student), self.user.username)

    def test_uuid(self):
        self.assertEquals(self.user.student.get_uuid(), str(self.user.student.uuid))
