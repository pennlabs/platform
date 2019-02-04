from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, generics
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication, TokenUser
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.settings import api_settings


class LabsTokenAuthentication(JWTTokenUserAuthentication):
    def get_user(self, validated_token):
        if api_settings.USER_ID_CLAIM not in validated_token:
            raise InvalidToken(_('Token contained no recognizable user identification'))
        user = User.objects.filter(id=validated_token[api_settings.USER_ID_CLAIM]).first()
        if (user is None or not hasattr(user.student, 'member')):
            raise InvalidToken(_('Token User is not a Penn Labs member'))
        return TokenUser(validated_token)


class PennAuthMixin(generics.GenericAPIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticated,)


class LabsAuthMixin(generics.GenericAPIView):
    authentication_classes = (LabsTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
