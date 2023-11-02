from announcements.models import Announcement
from announcements.permissions import IsSuperuser
from announcements.serializers import AnnouncementSerializer
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets


class AnnouncementsViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer

    def get_permissions(self):
        if self.request.method != "GET":
            self.permission_classes = [IsSuperuser]
        return super(AnnouncementsViewSet, self).get_permissions()

    def get_queryset(self):
        queryset = Announcement.objects.all()
        active = self.request.query_params.get("active")
        audiences = self.request.query_params.get("audience")

        if active == "true":
            queryset = queryset.filter(Q(end_time__gte=timezone.now()) | Q(end_time__isnull=True))

        if audiences:
            audience_names = audiences.split(",")
            queryset = queryset.filter(
                audiences__name__in=[name.strip().upper() for name in audience_names]
            )

        return queryset.distinct()
