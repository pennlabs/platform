from django.contrib.auth import get_user_model
from django.contrib.auth.backends import RemoteUserBackend


class ShibbolethRemoteUserBackend(RemoteUserBackend):
    def authenticate(self, request, remote_user, shibboleth_attributes):
        if not remote_user:
            return
        User = get_user_model()
        username = self.clean_username(remote_user)
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_unusable_password()
            for key, value in shibboleth_attributes.items():
                if value:
                    setattr(user, key, value)
                else:
                    # TODO Poll Penn Directory to get missing information
                    # User: first/last name and email
                    # Student: major, school, display name
                    setattr(user, key, searchPennDirectory())

            user.save()
            user = self.configure_user(user)

        return user if self.user_can_authenticate(user) else None

    def searchPennDirectory(self, username, wanted):
        pass
