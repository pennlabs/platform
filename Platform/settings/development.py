from Platform.settings.base import *  # noqa
from Platform.settings.base import INSTALLED_APPS, MIDDLEWARE


# Development extensions
INSTALLED_APPS += ["django_extensions", "debug_toolbar"]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
INTERNAL_IPS = ["127.0.0.1"]

# Disable admin login through shibboleth
SHIB_ADMIN = False
