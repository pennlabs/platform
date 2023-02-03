from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class PullsViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_monitor_pulls(self):
        resp = self.client.get(reverse("monitor:pulls"))
        self.assertEqual(resp.status_code, 200, resp.content)
