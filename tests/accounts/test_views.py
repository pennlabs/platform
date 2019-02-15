from django.test import TestCase, Client
from rest_framework_api_key.models import APIKey


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.secret_key = 'super_secret'
        self.api_key = APIKey.objects.create(secret_key=self.secret_key)

    def test_no_api_key(self):
        response = self.client.get('/accounts/login/')
        self.assertRedirects(response, 'https://auth.pennlabs.org/login/', fetch_redirect_response=False)

    def test_invalid_api_key(self):
        headers = {'HTTP_API_TOKEN': 'invalid_token'}
        response = self.client.get('/accounts/login/', headers)
        self.assertRedirects(response, 'https://auth.pennlabs.org/login/', fetch_redirect_response=False)

    def test_invalid_api_key_secret(self):
        headers = {'HTTP_API_TOKEN': self.api_key.token, 'HTTP_API_SECRET_KEY': 'invalid_secret'}
        response = self.client.get('/accounts/login/', headers)
        self.assertRedirects(response, 'https://auth.pennlabs.org/login/', fetch_redirect_response=False)

    def test_valid_api_key_invalid_shibboleth(self):
        headers = {'HTTP_API_TOKEN': self.api_key.token, 'HTTP_API_SECRET_KEY': self.secret_key}
        response = self.client.get('/accounts/login/', **headers)
        self.assertEqual(response.status_code, 500)

    def test_valid_api_key_valid_shibboleth(self):
        headers = {'HTTP_API_TOKEN': self.api_key.token, 'HTTP_API_SECRET_KEY': self.secret_key, 'HTTP_EPPN': 'test',
                   'HTTP_GIVENNAME': 'test', 'HTTP_SN': 'user', 'HTTP_MAIL': 'test@student.edu'}
        response = self.client.get('/accounts/login/', follow=True, **headers)
        self.assertRedirects(response, '/accounts/authorize/', target_status_code=400)
