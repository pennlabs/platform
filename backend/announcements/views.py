from announcements.serializers import AnnouncementSerializer
from rest_framework import generics, mixins, status, viewsets
from announcements.models import Announcement
from rest_framework.response import Response


class AnnouncementsView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer

    def list(self, request):
        announcement_list = Announcement.objects.all()
        return Response(announcement_list)
