from django.urls import path
from clubs.views import ClubViewSet, EventViewSet


urlpatterns = [
    path("clubs/", ClubViewSet.as_view({'get': 'list'})),
    path("events/", EventViewSet.as_view({'get': 'list'})),
]
