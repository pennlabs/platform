from rest_framework import viewsets, generics
from .models import Member, Team, Update, Event
from .serializers import MemberSerializer, TeamSerializer, UpdateSerializer, EventSerializer
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
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


class ProtectedViewSet(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return Response({"secret_information": "this is a protected route"})
