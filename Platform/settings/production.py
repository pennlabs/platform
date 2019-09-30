import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from Platform.settings.base import *


DEBUG = False

# Fix MySQL Emoji support
DATABASES['default']['OPTIONS'] = {'charset': 'utf8mb4'}

# Honour the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow production host headers
ALLOWED_HOSTS = ['platform-dev.pennlabs.org', 'platform-dev.apps.pennlabs.org']

SENTRY_URL = os.environ.get('SENTRY_URL', '')

sentry_sdk.init(
    dsn=SENTRY_URL,
    integrations=[DjangoIntegration()]
)

# CORS settings
CORS_ORIGIN_ALLOW_ALL = True
