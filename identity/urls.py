from django.urls import path
from oauth2_provider.views import AuthorizationView, TokenView

from identity.views import (
    AttestView,
    JwksInfoView,
    RefreshJWTView
)


app_name = "identity"


urlpatterns = [
    path("jwks/", JwksInfoView.as_view(), name="jwks"),
    path("attest/", AttestView.as_view(), name="attest"),
    path("refresh/", RefreshJWTView.as_view(), name="refresh"),
]
