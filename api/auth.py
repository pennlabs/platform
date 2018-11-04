from knox.auth import TokenAuthentication
from rest_framework import exceptions
from .models import Member
from rest_framework.authentication import get_authorization_header
from django.utils.translation import ugettext_lazy as _


class LabsTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        prefix = "Token".encode()
        if not auth or auth[0].lower() != prefix.lower():
            return None
        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. '
                    'Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)
        (user, auth_token) = super().authenticate(request)
        if Member.objects.filter(user=user).exists():
            return (user, auth_token)
        else:
            raise exceptions.AuthenticationFailed(
                _('Authentication Failed. User is not a Penn Labs member'))
