import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import RemoteUserBackend

from accounts.models import PennAffiliation, Student


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
                return ""

            return response[0]["email"]
        except (requests.exceptions.RequestException):
            return ""

    def authenticate(self, request, remote_user, shibboleth_attributes):
        if not remote_user or remote_user == -1:
            return
        User = get_user_model()
        user, created = User.objects.get_or_create(
            pennid=remote_user, defaults={"username": shibboleth_attributes["username"]}
        )

        # Add initial attributes on first log in
        if created:
            user.set_unusable_password()
            user.email = self.get_email(remote_user)
            user.save()
            user = self.configure_user(request, user)

        # Update fields if changed
        for key, value in shibboleth_attributes.items():
            if key != "affiliation" and getattr(user, key) is not value:
                setattr(user, key, value)

        # Update affiliations with every log in
        user.affiliation.clear()
        for affiliation_name in shibboleth_attributes["affiliation"]:
            affiliation, _ = PennAffiliation.objects.get_or_create(name=affiliation_name)
            user.affiliation.add(affiliation)

        # Create a student object if the user is a student
        if "student" in shibboleth_attributes["affiliation"]:
            Student.objects.get_or_create(user=user)

        user.save()

        return user if self.user_can_authenticate(user) else None
