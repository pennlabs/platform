from django.urls import path
from accounts.views import LabsProtectedViewSet, LoginView, ProtectedViewSet
from oauth2_provider.views import AuthorizationView, IntrospectTokenView, TokenView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("authorize/", AuthorizationView.as_view()),
    path("token/", TokenView.as_view()),
    path("introspect/", IntrospectTokenView.as_view()),
    path("protected/", ProtectedViewSet.as_view()),
    path("labsprotected/", LabsProtectedViewSet.as_view()),
]
