from pennlabs.settings.base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'platform',
        'USER': 'platform',
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': 'sql.pennlabs.org',
        'PORT': 3306,
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

# Disable Django's own staticfiles handling in favour of WhiteNoise, for
# greater consistency between gunicorn and `./manage.py runserver`. See:
# http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
MIDDLEWARE.remove('django.middleware.security.SecurityMiddleware')
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
] + MIDDLEWARE

# Honour the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow production host headers
ALLOWED_HOSTS = ['platform.pennlabs.org', 'platform.apps.pennlabs.org']
