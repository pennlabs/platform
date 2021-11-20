from django.conf import settings
from django.urls import path
from oauth2_provider.views import AuthorizationView, TokenView
from rest_framework import routers

from accounts.views import (
    DevLoginView,
    DevLogoutView,
    EmailViewSet,
    LoginView,
    LogoutView,
    MajorViewSet,
    PhoneNumberViewSet,
    ProductAdminView,
    SchoolViewSet,
    UserSearchView,
    UserView,
    UUIDIntrospectTokenView,
)


app_name = "accounts"

router = routers.SimpleRouter()
router.register("me/phonenumber", PhoneNumberViewSet, basename="me-phonenumber")
router.register("me/email", EmailViewSet, basename="me-email")
router.register("majors", MajorViewSet, basename="majors")
router.register("schools", SchoolViewSet, basename="schools")

FinalLoginView = DevLoginView if settings.IS_DEV_LOGIN else LoginView
FinalLogoutView = DevLogoutView if settings.IS_DEV_LOGIN else LogoutView

urlpatterns = [
    path("login/", FinalLoginView.as_view(), name="login"),
    path("logout/", FinalLogoutView.as_view(), name="logout"),
    path("me/", UserView.as_view(), name="me"),
    path("search/", UserSearchView.as_view(), name="search"),
    path("authorize/", AuthorizationView.as_view(), name="authorize"),
    path("token/", TokenView.as_view(), name="token"),
    path("introspect/", UUIDIntrospectTokenView.as_view(), name="introspect"),
    path("productadmin/", ProductAdminView.as_view(), name="productadmin"),
]

urlpatterns += router.urls
