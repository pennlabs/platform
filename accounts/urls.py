from django.urls import path
from oauth2_provider.views import AuthorizationView, TokenView

from accounts.views import LoginView, LogoutView, UserSearchView, UUIDIntrospectTokenView


app_name = "accounts"


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("search/", UserSearchView.as_view(), name="search"),
    path("authorize/", AuthorizationView.as_view(), name="authorize"),
    path("token/", TokenView.as_view(), name="token"),
    path("introspect/", UUIDIntrospectTokenView.as_view(), name="introspect"),
]
