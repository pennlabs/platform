from sentry_sdk import capture_message
from django.contrib import auth
from django.http import HttpResponseServerError
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework_api_key.crypto import hash_token
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.settings import TOKEN_HEADER, SECRET_KEY_HEADER
from rest_framework_simplejwt.views import TokenViewBase, TokenObtainPairView
from accounts.models import Application
from accounts.serializers import PlatformTokenObtainPairSerializer, PlatformTokenVerifySerializer
from accounts.utils import hash_client_secret


class PlatformTokenVerifyView(TokenViewBase):
    serializer_class = PlatformTokenVerifySerializer


class LoginView(generics.GenericAPIView):
    """
    Log in a user.
    """
    def login_redirect(self, redirect_uri):
        return redirect('https://auth.pennlabs.org/login?redirect_uri=' + redirect_uri)

    def get(self, request):
        # Get body and header variables
        redirect_uri = request.GET.get('redirect_uri', '')
        client_id = request.GET.get('client_id', '')
        client_secret = request.GET.get('client_secret', '')
        token = request.META.get(TOKEN_HEADER, '')
        secret_key = request.META.get(SECRET_KEY_HEADER, '')

        # Validate redirect_uri or invalidate request
        application = Application.objects.filter(redirect_uri=redirect_uri, revoked=False).first()
        if application is None:
            capture_message("Invalid login redirect_uri", level="error")
            return HttpResponseBadRequest("Invalid redirect_uri.")

        # Validate Application client id and secret and redirect to auth (Product initiating request)
        hased_client_secret = hash_client_secret(client_id, client_secret)
        if hased_client_secret == application.hashed_secret:
            return self.login_redirect(redirect_uri)

        # Validate API token and secret or invalidate request (Auth initiating request)
        api_key = APIKey.objects.filter(token=token, revoked=False).first()
        hashed_token = hash_token(token, secret_key)
        if api_key is None or hashed_token != api_key.hashed_token:
            capture_message("Invalid login request", level="error")
            return HttpResponseBadRequest("Invalid request.")

        # Request is from auth. Use provided headers to login user
        pennkey = request.META.get('HTTP_EPPN', '').lower().split('@')[0]
        first_name = request.META.get('HTTP_GIVENNAME', '').lower().capitalize()
        last_name = request.META.get('HTTP_SN', '').lower().capitalize()
        email = request.META.get('HTTP_MAIL', '').lower()
        shibboleth_attributes = {'first_name': first_name, 'last_name': last_name, 'email': email}
        user = auth.authenticate(remote_user=pennkey, shibboleth_attributes=shibboleth_attributes)
        if user:
            request.user = user
            auth.login(request, user)
            token = PlatformTokenObtainPairSerializer.get_token(user)
            response = redirect(redirect_uri + "?token=" + token)
            return response
        return HttpResponseServerError()
