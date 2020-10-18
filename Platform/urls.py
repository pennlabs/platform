from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view


admin.site.site_header = "Platform Admin"

urlpatterns = [
    path("", include("application.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("options/", include("options.urls", namespace="options")),
    path(
        "openapi/",
        get_schema_view(title="Platform Documentation", public=True),
        name="openapi-schema",
    ),
    path(
        "documentation/",
        TemplateView.as_view(
            template_name="redoc.html", extra_context={"schema_url": "openapi-schema"}
        ),
        name="documentation",
    ),
]

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
