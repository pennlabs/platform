from rest_framework.routers import SimpleRouter
from .views import MemberViewSet, ProductViewSet, UpdateViewSet

router = SimpleRouter()
router.register("members", MemberViewSet)
router.register("products", ProductViewSet)
router.register("updates", UpdateViewSet)

urlpatterns = router.urls