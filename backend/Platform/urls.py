from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view


admin.site.site_header = "Platform Admin"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("announcements/", include("announcements.urls", namespace="announcements")),
    path("accounts/", include("accounts.urls", namespace="oauth2_provider")),
    path("options/", include("options.urls", namespace="options")),
    path("identity/", include("identity.urls", namespace="identity")),
    path("healthbackend/", include("health.urls", namespace="health")),
    path("s/", include("shortener.urls", namespace="shortener")),
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

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        path("emailpreview/", include("email_tools.urls", namespace="email_tools")),
    ] + urlpatterns
