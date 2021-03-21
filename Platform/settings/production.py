import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from Platform.settings.base import *  # noqa
from Platform.settings.base import DOMAIN


DEBUG = False

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
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = ["GET"]
CORS_URLS_REGEX = r"^/options/$"

# Email client settings
EMAIL_HOST = os.getenv("SMTP_HOST")
EMAIL_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_HOST_USER = os.getenv("SMTP_USERNAME")
EMAIL_HOST_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_USE_TLS = True

IS_DEV_LOGIN = False
