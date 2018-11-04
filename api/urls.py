from django.urls import path
from shortener.views import index
from api.views import (ShortURLViewSet, MemberViewSet, AlumniViewSet, TeamViewSet,
    RoleViewSet, UpdateViewSet, ProtectedViewSet)

urlpatterns = [
    path("urls/get/<slug:short>/", index, name='index'),
    path("urls/create/", ShortURLViewSet.as_view()),
    path("members/", MemberViewSet.as_view({'get': 'list'})),
    path("members/<slug:url>", MemberViewSet.as_view({'get': 'single_member'})),
    path("alumni/", AlumniViewSet.as_view({'get': 'list'})),
    path("teams/", TeamViewSet.as_view({'get': 'list'})),
    path("roles/", RoleViewSet.as_view({'get': 'list'})),
    path("updates/", UpdateViewSet.as_view({'get': 'list'})),
    path("protected/", ProtectedViewSet.as_view())
]
