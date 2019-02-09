from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, generics
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import IsAuthenticated


class PennAuthMixin(generics.GenericAPIView):
    # authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticated,)


class LabsAuthMixin(generics.GenericAPIView):
    # authentication_classes = (LabsTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
