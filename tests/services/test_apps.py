from django.test import TestCase
from services.apps import ServicesConfig


class AppsTestCase(TestCase):
    def test_apps(self):
        self.assertEqual(ServicesConfig.name, 'services')
