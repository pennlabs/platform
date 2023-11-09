from announcements.models import Announcement
from announcements.permissions import AnnouncementPermissions
from announcements.serializers import AnnouncementSerializer
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets


class AnnouncementsViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    permission_classes = [AnnouncementPermissions]

    def get_queryset(self):
        # automatically filter for active announcements
        queryset = Announcement.objects.filter(
            Q(release_time__lte=timezone.now())
            & (Q(end_time__gte=timezone.now()) | Q(end_time__isnull=True))
        ).prefetch_related("audiences")
        audiences = self.request.query_params.get("audience")

        if audiences:
            audience_names = audiences.split(",")
            queryset = queryset.filter(
                audiences__name__in=[name.strip().upper() for name in audience_names]
            )

        return queryset.distinct()
