from rest_framework import generics, viewsets

from org.models import Member, Role, Team
from org.serializers import MemberSerializer, RoleSerializer, ShortUrlSerializer, TeamSerializer


class ShortUrlCreateView(generics.CreateAPIView):
    """
    Create a short slug for a long url.
    """

    serializer_class = ShortUrlSerializer


class MemberViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return a single member of Penn Labs using their unique url.

    list:
    Return a list of current Penn Labs members.
    """

    queryset = Member.objects.all().filter(alumnus=False)
    serializer_class = MemberSerializer
    http_method_names = ["get"]
    lookup_field = "url"


class AlumniViewSet(viewsets.ModelViewSet):
    """
    Return a list of Penn Labs alumni.
    """

    queryset = Member.objects.all().filter(alumnus=True)
    serializer_class = MemberSerializer
    http_method_names = ["get"]


class TeamViewSet(viewsets.ModelViewSet):
    """
    Return a list of Penn Labs teams.
    """

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    http_method_names = ["get"]


class RoleViewSet(viewsets.ModelViewSet):
    """
    Return a list of Penn Labs roles.
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    http_method_names = ["get"]
