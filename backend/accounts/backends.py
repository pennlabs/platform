import os

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.models import Group
from requests.auth import HTTPBasicAuth

from accounts.models import Email


SETTINGS_MODULE = os.getenv("DJANGO_SETTINGS_MODULE", None)


class ShibbolethRemoteUserBackend(RemoteUserBackend):
    """
    Authenticate users from Shibboleth headers.
    Code based on https://github.com/Brown-University-Library/django-shibboleth-remoteuser
    """

    def get_email(self, pennid):
        # Skip if in debug mode or staging
        if settings.DEBUG or SETTINGS_MODULE == "Platform.settings.staging":
            return None
        """
        Use Penn Directory API with OAuth2 to get the email of a user given their Penn ID.
        This is necessary to ensure that we have the correct domain (@seas vs. @wharton, etc.)
        for various services like Clubs emails.
        """
        auth = HTTPBasicAuth(
            settings.EMAIL_OAUTH_CLIENT_ID, settings.EMAIL_OAUTH_CLIENT_SECRET
        )
        token_response = requests.post(
            settings.EMAIL_OAUTH_TOKEN_URL,
            auth=auth,
            data={"grant_type": "client_credentials"},
        )

        if token_response.status_code != 200:
            return None

        tokens = token_response.json()
        access_token = tokens["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        api_url = settings.EMAIL_OAUTH_API_URL_BASE + str(pennid)
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()["result_data"]
            if not data:
                return None
            return data[0]["email"]
        else:
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
            user.set_unusable_password()
            user.save()
            user = self.configure_user(request, user)

        # Always update email

        email = self.get_email(remote_user)
        if email is None or email == "":
            email = f"{shibboleth_attributes['username']}@upenn.edu"

        old_email = Email.objects.filter(user=user, primary=True).first()

        if old_email and old_email.value != email:
            old_email.value = email
            old_email.save()
        elif not old_email:
            Email.objects.create(user=user, value=email, primary=True, verified=True)

        # Update fields if changed
        for key, value in shibboleth_attributes.items():
            if key != "affiliation" and getattr(user, key) is not value:
                setattr(user, key, value)

        # Update groups with every log in
        user.groups.clear()
        for affiliation_name in shibboleth_attributes["affiliation"]:
            if (
                affiliation_name
            ):  # Some users don't have any affiliation somehow ¯\_(ツ)_/¯
                group, _ = Group.objects.get_or_create(name=affiliation_name)
                user.groups.add(group)

        user.save()

        return user if self.user_can_authenticate(user) else None
