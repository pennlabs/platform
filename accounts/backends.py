from django.contrib.auth import get_user_model
from django.contrib.auth.backends import RemoteUserBackend

from accounts.models import PennAffiliation


class ShibbolethRemoteUserBackend(RemoteUserBackend):
    """
    Authenticate users from Shibboleth headers.
    Code based on https://github.com/Brown-University-Library/django-shibboleth-remoteuser
    """
    def searchPennDirectory(self, username, key):
        # TODO Poll Penn Directory to get missing information
        # User: first/last name and email
        # Student: major, school, display name
        return ''
        # bearer = ""
        # token = ""
        # headers = {
        #     "Authorization-Bearer": bearer,
        #     "Authorization-Token": token,
        # }
        # params = {
        #     "email": username,
        #     "affiliation": "STU"
        # }
        # response = get("https://esb.isc-seo.upenn.edu/8091/open_data/directory",
        #                params=params, headers=headers, timeout=30)
        # if response.status_code == 200:
        #     response = response.json()

    def authenticate(self, request, remote_user, shibboleth_attributes):
        if not remote_user or remote_user == -1:
            return
        User = get_user_model()
        user, created = User.objects.get_or_create(pennid=remote_user)

        # Add initial attributes on first log in
        if created:
            user.set_unusable_password()
            for key, value in shibboleth_attributes.items():
                if key != 'affiliation':
                    setattr(user, key, value)
            user.save()
            user = self.configure_user(request, user)

        # Update affiliations with every log in
        user.affiliation.clear()
        for affiliation_name in shibboleth_attributes['affiliation']:
            affiliation, _ = PennAffiliation.objects.get_or_create(name=affiliation_name)
            user.affiliation.add(affiliation)
        user.save()

        return user if self.user_can_authenticate(user) else None
