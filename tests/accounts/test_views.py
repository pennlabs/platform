from django.test import Client, TestCase
from django.urls import reverse
from rest_framework_api_key.models import APIKey


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.secret_key = 'super_secret'
        self.api_key = APIKey.objects.create(secret_key=self.secret_key)

    def test_next_variable(self):
        url = reverse('accounts:login') + '?next=/accounts/authorize/%3Fclient_id%3Done%26state%3Dabc'
        response = self.client.get(url)
        sample_response = 'https://auth.pennlabs.org/login/?next=/accounts/authorize/?client_id=one&state=abc'
        self.assertRedirects(response, sample_response, fetch_redirect_response=False)

    def test_no_api_key(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertRedirects(response, 'https://auth.pennlabs.org/login/?next=', fetch_redirect_response=False)

    def test_invalid_api_key(self):
        headers = {'HTTP_API_TOKEN': 'invalid_token'}
        response = self.client.get(reverse('accounts:login'), headers)
        self.assertRedirects(response, 'https://auth.pennlabs.org/login/?next=', fetch_redirect_response=False)

    def test_invalid_api_key_secret(self):
        headers = {'HTTP_API_TOKEN': self.api_key.token, 'HTTP_API_SECRET_KEY': 'invalid_secret'}
        response = self.client.get(reverse('accounts:login'), headers)
        self.assertRedirects(response, 'https://auth.pennlabs.org/login/?next=', fetch_redirect_response=False)

    def test_valid_api_key_invalid_shibboleth(self):
        headers = {'HTTP_API_TOKEN': self.api_key.token, 'HTTP_API_SECRET_KEY': self.secret_key}
        response = self.client.get(reverse('accounts:login'), **headers)
        self.assertEqual(response.status_code, 500)

    def test_valid_api_key_valid_shibboleth(self):
        headers = {'HTTP_API_TOKEN': self.api_key.token, 'HTTP_API_SECRET_KEY': self.secret_key, 'HTTP_EPPN': 'test',
                   'HTTP_GIVENNAME': 'test', 'HTTP_SN': 'user', 'HTTP_MAIL': 'test@student.edu'}
        params = reverse('accounts:authorize') + '?client_id=abc123&response_type=code&state=abc'
        response = self.client.get(reverse('accounts:login') + '?next=' + params, **headers)
        base_url = 'https://platform.pennlabs.org/accounts/authorize/'
        sample_response = base_url + '?client_id=abc123&response_type=code&state=abc'
        self.assertRedirects(response, sample_response, fetch_redirect_response=False)
