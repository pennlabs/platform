from django.urls import path
from oauth2_provider.views import AuthorizationView, TokenView
from django.conf import settings
from accounts.views import (
    DevLoginView,
    DevLogoutView,
    LabsProtectedViewSet,
    LoginView,
    LogoutView,
    ProtectedViewSet,
    UserSearchView,
    UUIDIntrospectTokenView,
)


app_name = "accounts"

if settings.IS_DEV_LOGIN:
    login_view = DevLoginView
    logout_view = DevLogoutView
else:
    login_view = LoginView
    logout_view = LogoutView

urlpatterns = [
    path("login/", login_view.as_view(), name="login"),
    path("logout/", logout_view.as_view(), name="logout"),
    path("search/", UserSearchView.as_view(), name="search"),
    path("authorize/", AuthorizationView.as_view(), name="authorize"),
    path("token/", TokenView.as_view(), name="token"),
    path("introspect/", UUIDIntrospectTokenView.as_view(), name="introspect"),
    path("protected/", ProtectedViewSet.as_view(), name="protected"),
    path("labsprotected/", LabsProtectedViewSet.as_view(), name="labsprotected"),
]
