from django.test import TestCase

from org.models import Team
from services.models import Endpoint, Service, Update


class ServiceTestCase(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Directors", description="Important people", order=1)
        self.service = Service.objects.create(name="Service", team=self.team)

    def test_str(self):
        self.assertEqual(str(self.service), self.service.name)


class EndpointTestCase(TestCase):
    def setUp(self):
        self.endpoint = Endpoint.objects.create(url="platform")

    def test_str(self):
        self.assertEqual(str(self.endpoint), self.endpoint.url)


class UpdateTestCase(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Directors", description="Important people", order=1)
        self.service = Service.objects.create(name="Service", team=self.team)
        self.update = Update.objects.create(service=self.service)

    def test_str(self):
        self.assertEqual(str(self.update), self.update.title)
