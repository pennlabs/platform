from rest_framework.routers import SimpleRouter
from .views import MemberViewSet, TeamViewSet, UpdateViewSet, EventViewSet

router = SimpleRouter()
router.register("members", MemberViewSet)
router.register("teams", TeamViewSet)
router.register("updates", UpdateViewSet)
router.register("events", EventViewSet)

urlpatterns = router.urls
