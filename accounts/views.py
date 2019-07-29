import calendar
import json

from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseServerError
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.models import get_access_token_model
from oauth2_provider.views import IntrospectTokenView
from rest_framework import generics
from sentry_sdk import capture_message

from accounts.auth import LabsView, PennView
from accounts.serializers import UserSerializer


class LoginView(generics.GenericAPIView):
    """
    Log in a user.
    WARNING: You must ensure this page is protected by Shibboleth and Clean Headers
    See https://github.com/nginx-shib/nginx-http-shibboleth
    """

    def get(self, request):
        pennkey = request.META.get('HTTP_EPPN', '').lower().split('@')[0]
        first_name = request.META.get('HTTP_GIVENNAME', '').lower().capitalize()
        last_name = request.META.get('HTTP_SN', '').lower().capitalize()
        email = request.META.get('HTTP_MAIL', '').lower()
        affiliation = request.META.get('HTTP_UNSCOPED_AFFILIATION', '').split(';')
        shibboleth_attributes = {'first_name': first_name, 'last_name': last_name, 'email': email,
                                 'affiliation': affiliation}
        user = auth.authenticate(remote_user=pennkey, shibboleth_attributes=shibboleth_attributes)
        if user:
            auth.login(request, user)
            return redirect(request.GET.get('next', '/'))
        capture_message('Invalid user returned from shibboleth')
        return HttpResponseServerError()


@method_decorator(csrf_exempt, name='dispatch')
class UUIDIntrospectTokenView(IntrospectTokenView):
    @staticmethod
    def get_token_response(token_value=None):
        try:
            token = get_access_token_model().objects.get(token=token_value)
        except ObjectDoesNotExist:
            return HttpResponse(
                content=json.dumps({'active': False}),
                status=401,
                content_type='application/json'
            )
        else:
            if token.is_valid():
                data = {
                    'active': True,
                    'scope': token.scope,
                    'exp': int(calendar.timegm(token.expires.timetuple())),
                }
                if token.application:
                    data['client_id'] = token.application.client_id
                if token.user:
                    data['user'] = UserSerializer(token.user).data
                return HttpResponse(content=json.dumps(data), status=200, content_type='application/json')
            else:
                return HttpResponse(content=json.dumps({
                    'active': False,
                }), status=200, content_type='application/json')


class ProtectedViewSet(PennView):
    """
    An example api endpoint to test user authentication.
    """
    def get(self, request, format=None):
        return HttpResponse({'secret_information': 'this is a login protected route'})


class LabsProtectedViewSet(LabsView):
    """
    An example api endpoint to test Penn Labs authentication.
    """
    def get(self, request, format=None):
        return HttpResponse({'secret_information': 'this is a Penn Labs protected route'})
