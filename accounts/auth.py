from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, generics
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.views import ProtectedResourceView
from oauth2_provider.views.mixins import ProtectedResourceMixin


class LabsMixin(ProtectedResourceMixin):
    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'student') and hasattr(request.user.student, 'member'):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()


class PennView(ProtectedResourceView):
    pass


class LabsView(LabsMixin, ProtectedResourceView):
    pass
