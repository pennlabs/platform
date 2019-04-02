from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase

from accounts.backends import ShibbolethRemoteUserBackend


class BackendTestCase(TestCase):
    def test_search_directory(self):
        backend = ShibbolethRemoteUserBackend()
        self.assertEqual(backend.searchPennDirectory('', ''), '')

    def test_invalid_remote_user(self):
        user = auth.authenticate(remote_user=None, shibboleth_attributes={})
        self.assertIsNone(user)

    def test_invalid_shibboleth_attributes(self):
        user = auth.authenticate(remote_user='student', shibboleth_attributes=None)
        self.assertIsNotNone(user)

    def test_partial_shibboleth_attributes(self):
        user = auth.authenticate(remote_user='student', shibboleth_attributes={'first_name': ''})
        self.assertEqual(user.first_name, '')

    def test_create_user(self):
        auth.authenticate(remote_user='test', shibboleth_attributes={})
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(str(User.objects.all()[0]), 'test')

    def test_create_user_with_attributes(self):
        attributes = {'first_name': 'test', 'last_name': 'user', 'email': 'test@student.edu'}
        user = auth.authenticate(remote_user='test', shibboleth_attributes=attributes)
        self.assertEqual(user.first_name, 'test')
        self.assertEqual(user.last_name, 'user')
        self.assertEqual(user.email, 'test@student.edu')

    def test_login_user(self):
        student = User.objects.create_user(username='student', password='secret')
        user = auth.authenticate(remote_user='student', shibboleth_attributes={})
        self.assertEqual(user, student)
