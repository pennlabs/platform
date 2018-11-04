from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/auth/', include('knox.urls')),
    path('api/', include('api.urls')),
    path('clubs/', include('clubs.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
