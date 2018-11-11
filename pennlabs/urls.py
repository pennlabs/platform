from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('org/', include('org.urls')),
    path('clubs/', include('clubs.urls')),
    path('documentation/', include_docs_urls(title="Platform Documentation")),
]
