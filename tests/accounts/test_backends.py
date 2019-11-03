from unittest.mock import patch

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.backends import ShibbolethRemoteUserBackend
from accounts.models import PennAffiliation


class BackendTestCase(TestCase):
    def setUp(self):
        self.shibboleth_attributes = {'first_name': '', 'last_name': '', 'email': '', 'affiliation': []}

    def test_invalid_remote_user(self):
        user = auth.authenticate(remote_user=-1, shibboleth_attributes=self.shibboleth_attributes)
        self.assertIsNone(user)

    def test_empty_shibboleth_attributes(self):
        user = auth.authenticate(remote_user=1, shibboleth_attributes=self.shibboleth_attributes)
        self.assertEqual(user.pennid, 1)
        self.assertEqual(user.first_name, '')

    def test_create_user(self):
        auth.authenticate(remote_user=1, shibboleth_attributes=self.shibboleth_attributes)
        self.assertEqual(len(get_user_model().objects.all()), 1)
        self.assertEqual(get_user_model().objects.all()[0].pennid, 1)

    def test_create_user_with_attributes(self):
        attributes = {'username': 'user', 'first_name': 'test', 'last_name': 'user',
                      'affiliation': ['student', 'member']}
        student_affiliation = PennAffiliation.objects.create(name='student')
        user = auth.authenticate(remote_user=1, shibboleth_attributes=attributes)
        self.assertEqual(user.first_name, 'test')
        self.assertEqual(user.last_name, 'user')
        self.assertEqual(user.affiliation.get(name='student'), student_affiliation)
        self.assertEqual(user.affiliation.get(name='member'), PennAffiliation.objects.get(name='member'))
        self.assertEqual(len(user.affiliation.all()), 2)
        self.assertEqual(len(PennAffiliation.objects.all()), 2)

    def test_update_user_with_attributes(self):
        attributes = {'username': 'user', 'first_name': 'test', 'last_name': 'user',
                      'affiliation': []}
        user = auth.authenticate(remote_user=1, shibboleth_attributes=attributes)
        self.assertEqual(user.username, 'user')
        attributes['username'] = 'changed_user'
        user = auth.authenticate(remote_user=1, shibboleth_attributes=attributes)
        self.assertEqual(user.username, 'changed_user')

    def test_login_user(self):
        student = get_user_model().objects.create_user(pennid=1, username='student', password='secret')
        user = auth.authenticate(remote_user=1, shibboleth_attributes=self.shibboleth_attributes)
        self.assertEqual(user, student)

    @patch('accounts.backends.requests.get')
    def test_get_email_exists(self, mock_response):
        mock_response.return_value.json.return_value = {
            'result_data': [
                {
                    'email': 'test@example.com'
                }
            ]
        }
        backend = ShibbolethRemoteUserBackend()
        self.assertEqual(backend.get_email(1), 'test@example.com')

    @patch('accounts.backends.requests.get')
    def test_get_email_no_exists(self, mock_response):
        mock_response.return_value.json.return_value = {
            'result_data': []
        }
        backend = ShibbolethRemoteUserBackend()
        self.assertEqual(backend.get_email(1), '')
