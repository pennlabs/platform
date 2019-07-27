from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls


admin.site.site_header = 'Platform Admin'

urlpatterns = [
    path('', include('application.urls')),
    path('accounts/', include('accounts.urls')),
    path('org/', include('org.urls')),
    path('services/', include('services.urls')),
    path('documentation/', include_docs_urls(title='Platform Documentation')),
    path('admin/', admin.site.urls),
]
