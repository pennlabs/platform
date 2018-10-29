from .views import MemberViewSet, TeamViewSet, RoleViewSet, UpdateViewSet, EventViewSet, ProtectedViewSet
from django.urls import path

urlpatterns = [
    path("members/", MemberViewSet.as_view({'get': 'list'})),
    path("teams/", TeamViewSet.as_view({'get': 'list'})),
    path("roles/", RoleViewSet.as_view({'get': 'list'})),
    path("updates/", UpdateViewSet.as_view({'get': 'list'})),
    path("events/", EventViewSet.as_view({'get': 'list'})),
    path("protected/", ProtectedViewSet.as_view())
]
