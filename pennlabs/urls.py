from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.documentation import include_docs_urls

admin.site.site_header = "Platform Admin"

urlpatterns = [
    path('', include('application.urls')),
    path('accounts/', include('accounts.urls')),
    path('org/', include('org.urls')),
    path('engagement/', include('engagement.urls')),
    path('documentation/', include_docs_urls(title="Platform Documentation")),
    path('admin/', admin.site.urls),
]
