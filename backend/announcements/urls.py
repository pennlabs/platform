from django.urls import path
from announcements.views import AnnouncementsViewSet
from rest_framework import routers

app_name = "announcements"
router = routers.SimpleRouter()
router.register("", AnnouncementsViewSet)
urlpatterns = router.urls
