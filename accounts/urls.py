from django.urls import path
from oauth2_provider.views import AuthorizationView, TokenView
from rest_framework import routers

from accounts.views import (
    EmailViewSet,
    LabsProtectedViewSet,
    LoginView,
    LogoutView,
    PhoneNumberViewSet,
    ProtectedViewSet,
    UserSearchView,
    UserView,
    UUIDIntrospectTokenView,
    MajorView,
    StudentView,
    SchoolView,
)


app_name = "accounts"

router = routers.SimpleRouter()
router.register("me/phonenumber/", PhoneNumberViewSet, basename="me-phonenumber")
router.register("me/email/", EmailViewSet, basename="me-email")

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", UserView.as_view(), name="me"),
    # path("me/student/", StudentView.as_view(), name="me-student"),
    path("majors/", MajorView.as_view(), name="majors"),
    path("schools/", SchoolView.as_view(), name="schools"),
    path("search/", UserSearchView.as_view(), name="search"),
    path("authorize/", AuthorizationView.as_view(), name="authorize"),
    path("token/", TokenView.as_view(), name="token"),
    path("introspect/", UUIDIntrospectTokenView.as_view(), name="introspect"),
    path("protected/", ProtectedViewSet.as_view(), name="protected"),
    path("labsprotected/", LabsProtectedViewSet.as_view(), name="labsprotected"),
]

urlpatterns += router.urls
