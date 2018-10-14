from rest_framework import viewsets
from .models import LabMember, Team, Update, Event
from .serializers import LabMemberSerializer, TeamSerializer, UpdateSerializer, EventSerializer


class LabMemberViewSet(viewsets.ModelViewSet):
    queryset = LabMember.objects.all()
    serializer_class = LabMemberSerializer
    http_method_names = ['get']


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    http_method_names = ['get']


class UpdateViewSet(viewsets.ModelViewSet):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    http_method_names = ['get']


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ['get']
