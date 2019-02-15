import json
from django.test import TestCase, Client
from shortener.models import Url


class ShortURLViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_url(self):
        response = self.client.post('/org/urls/create/', {'url': 'http://pennlabs.org'})
        self.assertEqual(response.status_code, 200)
        sample_response = json.loads('{"short": "7a28b", "long": "http://pennlabs.org"}')
        self.assertEqual(response.data, sample_response)
        self.assertEqual(len(Url.objects.all()), 1)

    def test_invalid_url(self):
        response = self.client.post('/org/urls/create/')
        self.assertEqual(response.status_code, 400)
