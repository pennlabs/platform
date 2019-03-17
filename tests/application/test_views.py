from django.test import TestCase, Client
from django.urls import reverse


class SplashViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_splash_view(self):
        response = self.client.get(reverse('application:homepage'))
        self.assertTemplateUsed(response, 'splash.html')
