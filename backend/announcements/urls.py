from django.urls import path
from announcements.views import AnnouncementsView

app_name = "announcement"

urlpatterns = [path("list", AnnouncementsView.as_view(), name="list")]
