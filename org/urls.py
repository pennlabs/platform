from django.urls import path
from shortener.views import index
from org.views import (ShortUrlViewSet, MemberViewSet, AlumniViewSet, TeamViewSet,
    RoleViewSet, ProtectedViewSet)


urlpatterns = [
    path("urls/get/<slug:short>/", index, name='index'),
    path("urls/create/", ShortUrlViewSet.as_view()),
    path("members/", MemberViewSet.as_view({'get': 'list'})),
    path("alumni/", AlumniViewSet.as_view({'get': 'list'})),
    path("teams/", TeamViewSet.as_view({'get': 'list'})),
    # path("teams/<slug:team>/", TeamMemberViewSet.as_view({'get': 'list'})),
    path("roles/", RoleViewSet.as_view({'get': 'list'})),
    path("protected/", ProtectedViewSet.as_view())
]
