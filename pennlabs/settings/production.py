import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from pennlabs.settings.base import *


DEBUG = False

# Disable Django's own staticfiles handling in favour of WhiteNoise, for
# greater consistency between gunicorn and `./manage.py runserver`. See:
# http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
MIDDLEWARE.remove('django.middleware.security.SecurityMiddleware')
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
] + MIDDLEWARE

# Fix MySQL Emoji support
DATABASES['default']['OPTIONS'] = {'charset': 'utf8mb4'}

# Honour the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow production host headers
ALLOWED_HOSTS = ['platform.pennlabs.org', 'platform.apps.pennlabs.org']

SENTRY_URL = os.environ.get('SENTRY_URL', '')

sentry_sdk.init(
    dsn=SENTRY_URL,
    integrations=[DjangoIntegration()]
)

# CORS settings
CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'auth.pennlabs.org',
    'pennbasics.com',
    'penncfa.com',
    'pennclubs.com',
    'penncoursealert.com',
    'penncourseplan.com',
    'penncoursereview.com',
    'pennlabs.org',
)

# Allow session cookie to be set from auth

SESSION_COOKIE_DOMAIN = 'pennlabs.org'
