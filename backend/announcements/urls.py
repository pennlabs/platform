from announcements.views import AnnouncementsViewSet
from rest_framework import routers


app_name = "announcements"
router = routers.SimpleRouter()
router.register("", AnnouncementsViewSet, basename="announcements")
urlpatterns = router.urls
