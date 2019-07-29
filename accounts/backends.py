from collections import Mapping

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
        if not remote_user:
            return
        User = get_user_model()
        username = self.clean_username(remote_user)
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_unusable_password()
            if isinstance(shibboleth_attributes, Mapping):
                for key, value in shibboleth_attributes.items():
                    if key != 'affiliation':
                        if value:
                            setattr(user, key, value)
                        else:
                            setattr(user, key, self.searchPennDirectory(username, key))

            user.save()
            user = self.configure_user(request, user)

        if shibboleth_attributes is not None and 'affiliation' in shibboleth_attributes:
            for affiliation_name in shibboleth_attributes['affiliation']:
                affiliation = PennAffiliation.objects.get_or_create(name=affiliation_name)[0]
                user.affiliation.add(affiliation)
            user.save()

        return user if self.user_can_authenticate(user) else None
