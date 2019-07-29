from django.urls import include, path

from org.views import AlumniViewSet, MemberViewSet, RoleViewSet, ShortUrlCreateView, TeamViewSet


app_name = 'org'


urlpatterns = [
    path('urls/get/', include('shortener.urls')),
    path('urls/create/', ShortUrlCreateView.as_view(), name='create_url'),
    path('members/', MemberViewSet.as_view({'get': 'list'}), name='members'),
    path('alumni/', AlumniViewSet.as_view({'get': 'list'}), name='alumni'),
    path('teams/', TeamViewSet.as_view({'get': 'list'}), name='teams'),
    path('roles/', RoleViewSet.as_view({'get': 'list'}), name='roles'),
]
