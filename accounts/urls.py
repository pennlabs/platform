from django.urls import path
from accounts.views import LabsProtectedViewSet, LoginView, ProtectedViewSet, UUIDIntrospectTokenView
from oauth2_provider.views import AuthorizationView, TokenView


app_name = 'accounts'


urlpatterns = [
    path("login/", LoginView.as_view(), name='login'),
    path("authorize/", AuthorizationView.as_view(), name='authorize'),
    path("token/", TokenView.as_view(), name='token'),
    path("introspect/", UUIDIntrospectTokenView.as_view(), name='introspect'),
    path("protected/", ProtectedViewSet.as_view(), name='protected'),
    path("labsprotected/", LabsProtectedViewSet.as_view(), name='labsprotected'),
]
