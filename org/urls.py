from django.urls import path
from shortener.views import index

from org.views import AlumniViewSet, MemberViewSet, RoleViewSet, ShortUrlViewSet, TeamViewSet


app_name = 'org'


urlpatterns = [
    path('urls/get/<slug:short>/', index, name='get_url'),
    path('urls/create/', ShortUrlViewSet.as_view(), name='create_url'),
    path('members/', MemberViewSet.as_view({'get': 'list'}), name='members'),
    path('alumni/', AlumniViewSet.as_view({'get': 'list'}), name='alumni'),
    path('teams/', TeamViewSet.as_view({'get': 'list'}), name='teams'),
    path('roles/', RoleViewSet.as_view({'get': 'list'}), name='roles'),
]
