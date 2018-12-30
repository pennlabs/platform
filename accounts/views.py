from django.contrib import auth
from django.http import HttpResponseServerError
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_api_key.crypto import hash_token
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.settings import TOKEN_HEADER, SECRET_KEY_HEADER
from rest_framework_jwt.settings import api_settings
from accounts.models import Application

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginView(generics.GenericAPIView):
    """
    Log in a user. API Key protected.
    """
    def login_redirect(self, redirect_uri):
        return redirect('https://auth.pennlabs.org/login?redirect_uri=' + redirect_uri)

    def get(self, request):
        # Validate API Key or redirect to Shibboleth
        redirect_uri = request.GET.get('redirect_uri', '')
        application = Application.objects.filter(redirect_uri=redirect_uri, revoked=False).first()
        if application is None:
            raise ValidationError({"redirect_uri": "Invalid redirect_uri"})
        token = request.META.get(TOKEN_HEADER, '')
        secret_key = request.META.get(SECRET_KEY_HEADER, '')
        if not token or not secret_key:
            return self.login_redirect(redirect_uri)
        api_key = APIKey.objects.filter(token=token, revoked=False).first()
        if api_key is None:
            return self.login_redirect(redirect_uri)
        hashed_token = hash_token(token, secret_key)
        if hashed_token != api_key.hashed_token:
            return self.login_redirect(redirect_uri)

        # Use provided headers to login user
        pennkey = request.META.get('HTTP_EPPN', '').lower().split('@')[0]
        first_name = request.META.get('HTTP_GIVENNAME', '').lower().capitalize()
        last_name = request.META.get('HTTP_SN', '').lower().capitalize()
        email = request.META.get('HTTP_MAIL', '').lower()
        shibboleth_attributes = {'first_name': first_name, 'last_name': last_name, 'email': email}
        user = auth.authenticate(remote_user=pennkey, shibboleth_attributes=shibboleth_attributes)
        if user:
            request.user = user
            auth.login(request, user)
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            response = redirect(redirect_uri + "?token=" + token)
            return response
        return HttpResponseServerError()
