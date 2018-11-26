from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import list_route
from shortener.models import shorten
from accounts.auth import PennAuthMixin, LabsAuthMixin
from org.models import Member, Team, Role
from org.serializers import ShortUrlSerializer, MemberSerializer, TeamSerializer, RoleSerializer


class ShortUrlViewSet(generics.GenericAPIView):
    """
    Return the long URL of a given short slug.
    """
    serializer_class = ShortUrlSerializer

    def post(self, request):
        try:
            url = request.data.get('url', '')
            URLValidator()(url)
            short = shorten(url)
            return Response({'short': short.short_id, "long": url})
        except ValidationError:
            return HttpResponse(status=400)


class MemberViewSet(viewsets.ModelViewSet):
    """
    Return a list of current Penn Labs members.
    """
    queryset = Member.objects.all().filter(alumnus=False)
    serializer_class = MemberSerializer
    http_method_names = ['get']

    @list_route()
    def single_member(self, request, url=None):
        """
        Return a single member of Penn Labs using their unique url
        """
        obj = get_object_or_404(Member, alumnus=False, url=url)
        return Response(self.get_serializer(obj).data)


class AlumniViewSet(viewsets.ModelViewSet):
    """
    Return a list of Penn Labs alumni.
    """
    queryset = Member.objects.all().filter(alumnus=True)
    serializer_class = MemberSerializer
    http_method_names = ['get']


class TeamViewSet(viewsets.ModelViewSet):
    """
    Return a list of Penn Labs teams.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    http_method_names = ['get']


class RoleViewSet(viewsets.ModelViewSet):
    """
    Return a list of Penn Labs roles.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    http_method_names = ['get']


class ProtectedViewSet(LabsAuthMixin, generics.GenericAPIView):
    """
    An example api endpoint to test user authentication.
    """
    def get(self, request, format=None):
        return Response({"secret_information": "this is a protected route"})
