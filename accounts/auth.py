import jwt
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, generics
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from org.models import Member

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class LabsTokenAuthentication(JSONWebTokenAuthentication):
    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        (user, payload) = super().authenticate(request)
        if hasattr(user.student, 'member'):
            return (user, payload)
        else:
            raise exceptions.AuthenticationFailed(
                _('Authentication Failed. User is not a Penn Labs member'))


class PennAuthMixin(generics.GenericAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class LabsAuthMixin(generics.GenericAPIView):
    authentication_classes = (LabsTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
