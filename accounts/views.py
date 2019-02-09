from sentry_sdk import capture_message
from django.contrib import auth
from django.http import HttpResponseServerError
from django.http.response import HttpResponse
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework_api_key.permissions import HasAPIKey
from accounts.auth import PennAuthMixin, LabsAuthMixin


class LoginView(generics.GenericAPIView):
    permission_classes = (HasAPIKey,)
    """
    Log in a user.
    """
    def login_redirect(self):
        return redirect('https://auth.pennlabs.org/login/')

    def get(self, request):
        pennkey = request.META.get('HTTP_EPPN', '').lower().split('@')[0]
        first_name = request.META.get('HTTP_GIVENNAME', '').lower().capitalize()
        last_name = request.META.get('HTTP_SN', '').lower().capitalize()
        email = request.META.get('HTTP_MAIL', '').lower()
        shibboleth_attributes = {'first_name': first_name, 'last_name': last_name, 'email': email}
        user = auth.authenticate(remote_user=pennkey, shibboleth_attributes=shibboleth_attributes)
        if user:
            auth.login(request, user)
            return redirect('/accounts/authorize/')
        capture_message("Invalid user returned from shibboleth")
        return HttpResponseServerError()


class ProtectedViewSet(PennAuthMixin, generics.GenericAPIView):
    """
    An example api endpoint to test user authentication.
    """
    def get(self, request, format=None):
        return HttpResponse({"secret_information": "this is a login protected route"})


class LabsProtectedViewSet(LabsAuthMixin, generics.GenericAPIView):
    """
    An example api endpoint to test Penn Labs authentication.
    """
    def get(self, request, format=None):
        return HttpResponse({"secret_information": "this is a Penn Labs protected route"})
