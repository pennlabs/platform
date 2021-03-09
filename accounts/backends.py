import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.models import Group

from accounts.models import Student


class ShibbolethRemoteUserBackend(RemoteUserBackend):
    """
    Authenticate users from Shibboleth headers.
    Code based on https://github.com/Brown-University-Library/django-shibboleth-remoteuser
    """

    def get_email(self, pennid):
        try:
            response = requests.get(
                settings.EMAIL_WEB_SERVICE_URL + str(pennid),
                auth=(settings.EMAIL_WEB_SERVICE_USERNAME, settings.EMAIL_WEB_SERVICE_PASSWORD),
            )
            response = response.json()
            response = response["result_data"]

            # Check if Penn ID doesn't exist somehow
            if len(response) == 0:
                return None

            return response[0]["email"]
        except (requests.exceptions.RequestException):
            return None

    def authenticate(self, request, remote_user, shibboleth_attributes):
        if not remote_user or remote_user == -1:
            return
        User = get_user_model()
        user, created = User.objects.get_or_create(
            pennid=remote_user, defaults={"username": shibboleth_attributes["username"]}
        )

        # Add initial attributes on first log in
        if created:
            email = self.get_email(remote_user)
            if email is None:
                email = f"{shibboleth_attributes['username']}@upenn.edu"
            user.set_unusable_password()
            user.email = email
            user.save()
            user = self.configure_user(request, user)

        # Update fields if changed
        for key, value in shibboleth_attributes.items():
            if key != "affiliation" and getattr(user, key) is not value:
                setattr(user, key, value)

        # Update groups with every log in
        user.groups.clear()
        for affiliation_name in shibboleth_attributes["affiliation"]:
            if affiliation_name:  # Some users don't have any affiliation somehow ¯\_(ツ)_/¯
                group, _ = Group.objects.get_or_create(name=affiliation_name)
                user.groups.add(group)

        # Create a student object if the user is a student
        if "student" in shibboleth_attributes["affiliation"]:
            Student.objects.get_or_create(user=user)

        user.save()

        return user if self.user_can_authenticate(user) else None
