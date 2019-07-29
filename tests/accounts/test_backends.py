from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.backends import ShibbolethRemoteUserBackend
from accounts.models import PennAffiliation


class BackendTestCase(TestCase):
    def setUp(self):
        self.shibboleth_attributes = {'first_name': '', 'last_name': '', 'email': '', 'affiliation': []}

    def test_search_directory(self):
        backend = ShibbolethRemoteUserBackend()
        self.assertEqual(backend.searchPennDirectory('', ''), '')

    def test_invalid_remote_user(self):
        user = auth.authenticate(remote_user=None, shibboleth_attributes=self.shibboleth_attributes)
        self.assertIsNone(user)

    def test_empty_shibboleth_attributes(self):
        user = auth.authenticate(remote_user='student', shibboleth_attributes=self.shibboleth_attributes)
        self.assertEqual(user.first_name, '')

    def test_create_user(self):
        auth.authenticate(remote_user='test', shibboleth_attributes=self.shibboleth_attributes)
        self.assertEqual(len(get_user_model().objects.all()), 1)
        self.assertEqual(str(get_user_model().objects.all()[0]), 'test')

    def test_create_user_with_attributes(self):
        attributes = {'first_name': 'test', 'last_name': 'user', 'email': 'test@student.edu',
                      'affiliation': ['student', 'member']}
        student_affiliation = PennAffiliation.objects.create(name='student')
        user = auth.authenticate(remote_user='test', shibboleth_attributes=attributes)
        self.assertEqual(user.first_name, 'test')
        self.assertEqual(user.last_name, 'user')
        self.assertEqual(user.email, 'test@student.edu')
        self.assertEqual(user.affiliation.get(name='student'), student_affiliation)
        self.assertEqual(user.affiliation.get(name='member'), PennAffiliation.objects.get(name='member'))
        self.assertEqual(len(user.affiliation.all()), 2)
        self.assertEqual(len(PennAffiliation.objects.all()), 2)

    def test_login_user(self):
        student = get_user_model().objects.create_user(username='student', password='secret')
        user = auth.authenticate(remote_user='student', shibboleth_attributes=self.shibboleth_attributes)
        self.assertEqual(user, student)
