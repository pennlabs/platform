from announcements.serializers import AnnouncementSerializer
from rest_framework import viewsets
from announcements.models import Announcement
from announcements.permissions import IsSuperuser


class AnnouncementsViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()

    def get_permissions(self):
        if self.request.method != "GET":
            self.permission_classes = [IsSuperuser]
        return super(AnnouncementsViewSet, self).get_permissions()
