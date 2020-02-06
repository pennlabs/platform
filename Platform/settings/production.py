import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from Platform.settings.base import *  # noqa
from Platform.settings.base import DATABASES, DOMAIN


DEBUG = False

# Fix MySQL Emoji support
DATABASES["default"]["OPTIONS"] = {"charset": "utf8mb4"}

# Honour the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Allow production host headers
ALLOWED_HOSTS = [DOMAIN]

# Make sure SECRET_KEY is set to a secret in production
SECRET_KEY = os.environ.get("SECRET_KEY", None)

# Sentry settings
SENTRY_URL = os.environ.get("SENTRY_URL", "")
sentry_sdk.init(dsn=SENTRY_URL, integrations=[DjangoIntegration()])

# CORS settings
CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    "pennbasics.com",
    "penncfa.com",
    "pennclubs.com",
    "penncoursealert.com",
    "penncourseplan.com",
    "penncoursereview.com",
    "pennlabs.org",
    "studentlife.pennlabs.org",
    "api.pennlabs.org",
)
