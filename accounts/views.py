import base64
from sentry_sdk import capture_message
from django.contrib import auth
from django.http import HttpResponseServerError
from django.http.response import HttpResponse
from django.utils.encoding import iri_to_uri
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework_api_key.permissions import HasAPIKey
from accounts.auth import PennView, LabsView


class LoginView(generics.GenericAPIView):
    """
    Log in a user.
    """
    def get(self, request):
        # Validate API Key
        if not HasAPIKey.has_permission(self, request, self):
            return redirect('https://auth.pennlabs.org/login/?next=' + iri_to_uri(request.GET.get('next', '')))

        # API is valid, login user
        pennkey = request.META.get('HTTP_EPPN', '').lower().split('@')[0]
        first_name = request.META.get('HTTP_GIVENNAME', '').lower().capitalize()
        last_name = request.META.get('HTTP_SN', '').lower().capitalize()
        email = request.META.get('HTTP_MAIL', '').lower()
        shibboleth_attributes = {'first_name': first_name, 'last_name': last_name, 'email': email}
        user = auth.authenticate(remote_user=pennkey, shibboleth_attributes=shibboleth_attributes)
        if user:
            auth.login(request, user)
            params = request.get_full_path().split('authorize/')[1]
            return redirect('https://platform.pennlabs.org/accounts/authorize/' + params)
        capture_message("Invalid user returned from shibboleth")
        return HttpResponseServerError()


class ProtectedViewSet(PennView):
    """
    An example api endpoint to test user authentication.
    """
    def get(self, request, format=None):
        return HttpResponse({"secret_information": "this is a login protected route"})


class LabsProtectedViewSet(LabsView):
    """
    An example api endpoint to test Penn Labs authentication.
    """
    def get(self, request, format=None):
        return HttpResponse({"secret_information": "this is a Penn Labs protected route"})
