from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from oauth2_provider.views import (
    AuthorizationView,
    ConnectDiscoveryInfoView,
    JwksInfoView,
    TokenView,
)
from rest_framework import routers

from accounts.views import (
    DevLoginView,
    DevLogoutView,
    EmailViewSet,
    FindUserView,
    LoginView,
    LogoutView,
    MajorViewSet,
    PhoneNumberViewSet,
    PrivacySettingView,
    ProductAdminView,
    ProfilePicViewSet,
    SchoolViewSet,
    UserSearchView,
    UserView,
    UUIDIntrospectTokenView,
)


app_name = "accounts"

router = routers.SimpleRouter()
router.register("me/phonenumber", PhoneNumberViewSet, basename="me-phonenumber")
router.register("me/email", EmailViewSet, basename="me-email")
router.register("me/pfp", ProfilePicViewSet, basename="me-pfp")
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
    path("privacy/", PrivacySettingView.as_view(), name="privacy"),
    path("privacy/<int:pk>/", PrivacySettingView.as_view(), name="privacy"),
    path("user/<str:username>", FindUserView.as_view(), name="user"),
    path(
        ".well-known/openid-configuration",
        ConnectDiscoveryInfoView.as_view(),
        name="oidc-connect-discovery-info",
    ),
    path(".well-known/jwks.json", JwksInfoView.as_view(), name="oidc-jwks-info"),
]

urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
