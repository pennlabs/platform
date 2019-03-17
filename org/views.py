from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from rest_framework import viewsets, generics
from rest_framework.response import Response
from shortener.models import shorten
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
    retrieve:
    Return a single member of Penn Labs using their unique url.

    list:
    Return a list of current Penn Labs members.
    """
    queryset = Member.objects.all().filter(alumnus=False)
    serializer_class = MemberSerializer
    http_method_names = ['get']
    lookup_field = 'url'


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
