from rest_framework.routers import SimpleRouter
from .views import MemberViewSet, ProductViewSet, UpdateViewSet, EventViewSet

router = SimpleRouter()
router.register("members", MemberViewSet)
router.register("products", ProductViewSet)
router.register("updates", UpdateViewSet)
router.register("events", EventViewSet)

urlpatterns = router.urls