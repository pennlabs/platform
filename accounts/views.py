import calendar
import json

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import call_command
from django.db.models import Case, IntegerField, Q, Value, When
from django.http import HttpResponseServerError
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from oauth2_provider.models import get_access_token_model
from oauth2_provider.views import IntrospectTokenView
from rest_framework import generics, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response
from sentry_sdk import capture_message

from accounts.auth import LabsView, PennView
from accounts.models import Major, School, Student, User
from accounts.serializers import (
    EmailSerializer,
    MajorSerializer,
    PhoneNumberSerializer,
    SchoolSerializer,
    UserSearchSerializer,
    UserSerializer,
)


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

    def get(self, request):
        call_command("populate_users")
        user_objects = get_user_model().objects.all()
        user_data = []
        for user in user_objects:

            try:
                student = Student.objects.get(user=user)
                user_majors = student.major.all()
                user_major_list = []
                for major in user_majors:
                    user_major_list.append(major.name + " " + major.degree_type)
                user_schools = student.school.all()
                user_school_list = []
                for school in user_schools:
                    user_school_list.append(school.name)
                user_data.append(
                    {"user": user, "majors": user_major_list, "schools": user_school_list}
                )
            except Student.DoesNotExist:
                user_data.append({"user": user, "majors": ["N/A"], "schools": ["N/A"]})
        return render(request, "accounts/devlogin.html", {"user_data": user_data})

    def post(self, request):
        choice = int(request.POST.get("userChoice", ""))
        try:
            user = get_user_model().objects.get(pennid=choice)
        except Student.DoesNotExist:
            user = get_user_model().objects.get(pennid=1)
        affiliations = ""
        for group in user.groups.all():
            affiliations += group.name + ";"
        shibboleth_attributes = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "affiliation": affiliations,
        }
        user = auth.authenticate(
            remote_user=user.pennid, shibboleth_attributes=shibboleth_attributes
        )
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


class UserView(generics.RetrieveUpdateAPIView):
    """
    get:
    Return information about the logged in user.

    update:
    Update information about the logged in user.
    You must specify all of the fields or use a patch request.

    patch:
    Update information about the logged in user.
    Only updates fields that are passed to the server.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PhoneNumberViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return a single phone number with all information fields present.

    list:
    Return a list of phone numbers associated with current user.

    create:
    Add new unverified phone number.

    update:
    Update all fields.
    You must specify all of the fields or use a patch request.

    partial_update:
    Update certain fields.
    Only specify the fields that you want to change.

    destroy:
    Delete a phone number.
    """

    serializer_class = PhoneNumberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.phone_numbers.all()

    def destroy(self, request, *args, **kwargs):
        is_primary = self.get_object().primary
        self.get_object().delete()
        next_number = self.get_queryset().filter(verified=True).first()
        if is_primary and next_number is not None:
            next_number.primary = True
            next_number.save()
        return Response({"detail": "Phone number successfully deleted"}, status=200)


class EmailViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return a single email with all information fields present.

    list:
    Return a list of emails associated with current user.

    create:
    Add new unverified email.

    update:
    Update all fields.
    You must specify all of the fields or use a patch request.

    partial_update:
    Update certain fields.
    Only specify the fields that you want to change.

    destroy:
    Delete an email.
    """

    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.emails.all()

    def destroy(self, request, *args, **kwargs):
        if self.get_queryset().filter(verified=True).count() < 2:
            return Response({"detail": "You can't delete the only verified email"}, status=405)

        is_primary = self.get_object().primary
        self.get_object().delete()
        next_email = self.get_queryset().filter(verified=True).first()
        if is_primary and next_email is not None:
            next_email.primary = True
            next_email.save()
        return Response({"detail": "Email successfully deleted"}, status=200)


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


class MajorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Retrieve a list of all of the active majors/programs
    (supports search functionality on name and degree type)

    retrieve:
    Retrieve a specific major by id
    """

    serializer_class = MajorSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "degree_type"]
    queryset = Major.objects.filter(is_active=True)


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Retrieve a list of all of the schools
    (supports search functionality on name)

    retrieve:
    Retrieve a specific school by id
    """

    serializer_class = SchoolSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]
    queryset = School.objects.all()
