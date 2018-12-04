from django.urls import path
from engagement.views import ClubViewSet, ClubDetail, EventViewSet


urlpatterns = [
    path("clubs/", ClubViewSet.as_view({'get': 'list'})),
    path('clubs/<str:pk>/', ClubDetail.as_view()),
    path("events/", EventViewSet.as_view({'get': 'list'}))
]
