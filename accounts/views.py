import calendar
import json

from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Case, IntegerField, Q, Value, When
from django.http import HttpResponseServerError
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from oauth2_provider.models import get_access_token_model
from oauth2_provider.views import IntrospectTokenView
from rest_framework import generics
from sentry_sdk import capture_message

from accounts.auth import LabsView, PennView
from accounts.models import User
from accounts.serializers import UserSearchSerializer, UserSerializer


class LoginView(View):
    """
    Log in a user.
    WARNING: You must ensure this page is protected by Shibboleth and Clean Headers
    See https://github.com/nginx-shib/nginx-http-shibboleth
    """

    def get(self, request):
        pennid = int(request.META.get("HTTP_EMPLOYEENUMBER", "-1"))
        pennkey = request.META.get("HTTP_EPPN", "").lower().split("@")[0]
        first_name = request.META.get("HTTP_GIVENNAME", "").title()
        last_name = request.META.get("HTTP_SN", "").lower().title()
        affiliation = request.META.get("HTTP_UNSCOPED_AFFILIATION", "").split(";")
        shibboleth_attributes = {
            "username": pennkey,
            "first_name": first_name,
            "last_name": last_name,
            "affiliation": affiliation,
        }
        user = auth.authenticate(remote_user=pennid, shibboleth_attributes=shibboleth_attributes)
        if user:
            auth.login(request, user)
            return redirect(request.GET.get("next", "/"))
        capture_message("Invalid user returned from shibboleth")
        return HttpResponseServerError()


class DevLoginView(View):
    """
    Log in a test user.
    Does not use Shibboleth
    """

    @staticmethod
    def populate_user_data():
        NAMES = [
            "George Washington",
            "John Adams",
            "Thomas Jefferson",
            "James Madison",
            "James Monroe",
            "John Quincy Adams",
            "Andrew Jackson",
            "Martin Van Buren",
            "William Harrison",
            "John Tyler",
        ]
        users = []
        for i, name in enumerate(NAMES):
            first, last = name.split(" ", 1)
            pennkey = first.lower() + last[0].lower()
            affiliation = "student;member"
            users.append(
                {
                    # if leave as i, g. wash's pennid is 0, which makes not remote_user true
                    "pennid": i + 1,
                    "pennkey": pennkey,
                    "first_name": first,
                    "last_name": last,
                    "affiliation": affiliation,
                }
            )
        return users

    def get(self, request):
        users = DevLoginView.populate_user_data()
        return render(request, "accounts/devlogin.html", {"users": users})

    def post(self, request):
        choice = int(request.POST.get("userChoice", ""))
        users = DevLoginView.populate_user_data()
        if choice - 1 < 0 or choice - 1 >= len(users):
            choice = 1
        user_data = users[choice - 1]
        pennid = user_data["pennid"]
        pennkey = user_data["pennkey"]
        first_name = user_data["first_name"]
        last_name = user_data["last_name"]
        affiliation = user_data["affiliation"]
        shibboleth_attributes = {
            "username": pennkey,
            "first_name": first_name,
            "last_name": last_name,
            "affiliation": affiliation,
        }
        user = auth.authenticate(remote_user=pennid, shibboleth_attributes=shibboleth_attributes)
        auth.login(request, user)
        return redirect(request.GET.get("next", "/"))


class DevLogoutView(View):
    """
    Log out a test user from Platform
    """

    def get(self, request):
        auth.logout(request)
        return redirect("accounts:login")


class LogoutView(View):
    """
    Log out a user from both Platform and Shibboleth.
    """

    def get(self, request):
        auth.logout(request)
        return redirect("/Shibboleth.sso/Logout?return=https://idp.pennkey.upenn.edu/logout")


@method_decorator(csrf_exempt, name="dispatch")
class UUIDIntrospectTokenView(IntrospectTokenView):
    @staticmethod
    def get_token_response(token_value=None):
        try:
            token = get_access_token_model().objects.get(token=token_value)
        except ObjectDoesNotExist:
            return HttpResponse(
                content=json.dumps({"active": False}), status=401, content_type="application/json"
            )
        else:
            if token.is_valid():
                data = {
                    "active": True,
                    "scope": token.scope,
                    "exp": int(calendar.timegm(token.expires.timetuple())),
                }
                if token.application:
                    data["client_id"] = token.application.client_id
                if token.user:
                    data["user"] = UserSerializer(token.user).data
                return HttpResponse(
                    content=json.dumps(data), status=200, content_type="application/json"
                )
            else:
                return HttpResponse(
                    content=json.dumps({"active": False}),
                    status=200,
                    content_type="application/json",
                )


class UserSearchView(PennView, generics.ListAPIView):
    """
    Search for users by first name, last name, or pennkey. Authentication Required.
    """

    serializer_class = UserSearchSerializer

    def get_queryset(self):
        query = self.request.query_params.get("q", "")
        if len(query) < 2:  # Do not show anything if query is less than two characters
            return None
        qs = User.objects.none()
        if " " in query:  # First and last name provided
            # Returns the following results in sorted order:
            # 1. Exact match on first and last name
            # 2. Starting match on first name and exact match on last name
            # 3. Starting match on first and last name

            first, last = query.split()

            q1 = Q(first_name__iexact=first) & Q(last_name__iexact=last)
            q2 = Q(first_name__istartswith=first) & Q(last_name__iexact=last)
            q3 = Q(first_name__istartswith=first) & Q(last_name__istartswith=last)
            qs = (
                User.objects.filter(q1 | q2 | q3)
                .annotate(
                    search_type_ordering=Case(
                        When(q1, then=Value(2)),
                        When(q2, then=Value(1)),
                        When(q3, then=Value(0)),
                        default=Value(-1),
                        output_field=IntegerField(),
                    )
                )
                .order_by("-search_type_ordering")
            )
        else:
            # Returns the following results in sorted order:
            # 1. Exact first name match
            # 2. Exact last name match
            # 3. Starting first name match
            # 4. Starting last name match
            # 5. Exact pennkey match

            q1 = Q(first_name__iexact=query)
            q2 = Q(last_name__iexact=query)
            q3 = Q(first_name__istartswith=query)
            q4 = Q(last_name__istartswith=query)
            q5 = Q(username__iexact=query)
            qs = (
                User.objects.filter(q1 | q2 | q3 | q4 | q5)
                .annotate(
                    search_type_ordering=Case(
                        When(q1, then=Value(5)),
                        When(q2, then=Value(4)),
                        When(q3, then=Value(3)),
                        When(q4, then=Value(2)),
                        When(q5, then=Value(1)),
                        default=Value(-1),
                        output_field=IntegerField(),
                    )
                )
                .order_by("-search_type_ordering")
            )
        return qs


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
