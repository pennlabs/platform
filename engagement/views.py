from django.shortcuts import render
from django.http import Http404
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from engagement.models import Club, Event
from engagement.serializers import ClubSerializer, EventSerializer


class ClubViewSet(viewsets.ModelViewSet):
    """
    Return a list of clubs.
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    http_method_names = ['get']

class ClubDetail(APIView):
    """
    Return a single club.
    """
    def get_object(self, pk):
        try:
            return Club.objects.get(pk=pk)
        except Club.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        club = self.get_object(pk)
        serializer = ClubSerializer(club)
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    """
    Return a list of events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ['get']