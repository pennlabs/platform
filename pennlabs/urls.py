from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view


admin.site.site_header = 'Platform Admin'

urlpatterns = [
    path('', include('application.urls')),
    path('accounts/', include('accounts.urls')),
    path('org/', include('org.urls')),
    path('services/', include('services.urls')),
    path('admin/', admin.site.urls),
    path('openapi/', get_schema_view(
        title="Platform Documentation"
    ), name='openapi-schema'),
    path('documentation/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='documentation'),
]
