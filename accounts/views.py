from django.shortcuts import redirect
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework_api_key.crypto import hash_token
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.settings import TOKEN_HEADER, SECRET_KEY_HEADER
from accounts.models import Student


class LoginView(generics.GenericAPIView):
    """
    Log in a user. API Key protected.
    """
    def login_redirect(self):
        return redirect('https://auth.pennlabs.org/login')

    def get(self, request):
        # Validate API Key or redirect to Shibboleth
        token = request.META.get(TOKEN_HEADER, '')
        secret_key = request.META.get(SECRET_KEY_HEADER, '')
        if not token or not secret_key:
            return self.login_redirect()
        api_key = APIKey.objects.filter(token=token, revoked=False).first()
        if api_key is None:
            return self.login_redirect()
        hashed_token = hash_token(token, secret_key)
        if hashed_token != api_key.hashed_token:
            return self.login_redirect()

        return Response({"Test": "okay"})
