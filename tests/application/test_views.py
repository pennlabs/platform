from django.test import TestCase, Client


class SplashViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_splash_view(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'splash.html')
