import json

from django.test import Client, TestCase
from django.urls import reverse
from shortener.models import Url


class ShortURLViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_url(self):
        response = self.client.post(reverse('org:create_url'), {'long_url': 'http://pennlabs.org'})
        self.assertEqual(response.status_code, 201)
        sample_response = json.loads('{"short_id": "7a28b", "long_url": "http://pennlabs.org"}')
        self.assertEqual(response.data, sample_response)
        self.assertEqual(len(Url.objects.all()), 1)

    def test_invalid_url(self):
        response = self.client.post(reverse('org:create_url'))
        self.assertEqual(response.status_code, 400)
