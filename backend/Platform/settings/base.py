"""
Django settings for pennlabs project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

import dj_database_url


DOMAINS = os.environ.get("DOMAINS", "example.com").split(",")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "o7ql0!vuk0%rgrh9p2bihq#pege$qqlm@zo#8&t==%&za33m*2"
)

IDENTITY_RSA_PRIVATE_KEY = os.environ.get(
    "IDENTITY_RSA_PRIVATE_KEY",
    """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCbCYh5h2NmQuBqVO6G+/CO+cHm9VBzsb0MeA6bbQfDnbhstVOT
j0hcnZJzDjYc6ajBZZf6gxVP9xrdm9Uh599VI3X5PFXLbMHrmzTAMzCGIyg+/fnP
0gocYxmCX2+XKyj/Zvt1pUX8VAN2AhrJSfxNDKUHERTVEV9bRBJg4F0C3wIDAQAB
AoGAP+i4nNw+Ec/8oWh8YSFm4xE6qKG0NdTtSMAOyWwy+KTB+vHuT1QPsLn1vj77
+IQrX/moogg6F1oV9YdA3vat3U7rwt1sBGsRrLhA+Spp9WEQtglguNo4+QfVo2ju
YBa2rG+h75qjiA3xnU//F3rvwnAsOWv0NUVdVeguyR+u6okCQQDBUmgWeH2WHmUn
2nLNCz+9wj28rqhfOr9Ptem2gqk+ywJmuIr4Y5S1OdavOr2UZxOcEwncJ/MLVYQq
MH+x4V5HAkEAzU2GMR5OdVLcxfVTjzuIC76paoHVWnLibd1cdANpPmE6SM+pf5el
fVSwuH9Fmlizu8GiPCxbJUoXB/J1tGEKqQJBALhClEU+qOzpoZ6/voYi/6kdN3zc
uEy0EN6n09AKb8gS9QH1STgAqh+ltjMkeMe3C2DKYK5/QU9/Pc58lWl1FkcCQG67
ZamQgxjcvJ85FvymS1aqW45KwNysIlzHjFo2jMlMf7dN6kobbPMQftDENLJvLWIT
qoFyGycdsxZiPAIyZSECQQCZFn3Dl6hnJxWZH8Fsa9hj79kZ/WVkIXGmtdgt0fNr
dTnvCVtA59ne4LEVie/PMH/odQWY0SxVm/76uBZv/1vY
-----END RSA PRIVATE KEY-----""",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_api_key",
    "oauth2_provider",
    "corsheaders",
    "phonenumber_field",
    "email_tools.apps.EmailToolsConfig",
    "shortener.apps.ShortenerConfig",
    "options.apps.OptionsConfig",
    "accounts.apps.AccountsConfig",
    "identity.apps.IdentityConfig",
    "announcements.apps.AnnouncementsConfig",
    "storages",
]


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Platform.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["Platform/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "Platform.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")
    )
}

# Set default PK type
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Authentication Backends

AUTHENTICATION_BACKENDS = (
    "oauth2_provider.backends.OAuth2Backend",
    "django.contrib.auth.backends.ModelBackend",
    "accounts.backends.ShibbolethRemoteUserBackend",
)


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Dev Login/Logout View toggle.
IS_DEV_LOGIN = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/assets/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# CORS Settings

CORS_ALLOW_ALL_ORIGINS = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [f"https://*.{domain}" for domain in DOMAINS]


# OAuth2 Settings

OAUTH2_PROVIDER = {
    "SCOPES": {
        "read": "Read scope",
        "write": "Write scope",
        "introspection": "Introspect token scope",
    },
    "ALLOWED_REDIRECT_URI_SCHEMES": ["http", "https"],
    "PKCE_REQUIRED": False,
}

# Custom User Model

AUTH_USER_MODEL = "accounts.User"

# Enable admin login through shibboleth
SHIB_ADMIN = True

# Email web service
EMAIL_OAUTH_CLIENT_ID = os.environ.get("EMAIL_OAUTH_CLIENT_ID", "")
EMAIL_OAUTH_CLIENT_SECRET = os.environ.get("EMAIL_OAUTH_CLIENT_SECRET", "")
EMAIL_OAUTH_TOKEN_URL = os.environ.get("EMAIL_OAUTH_TOKEN_URL", "")
EMAIL_OAUTH_API_URL_BASE = os.environ.get("EMAIL_OAUTH_API_URL_BASE", "")

# Twilio Settings

TWILIO_SID = os.environ.get("TWILIO_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_TOKEN", "")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER", "")

# Email Settings

EMAIL_TOOLS = {
    "FROM_EMAIL": "Penn Labs <accounts@pennlabs.org>",
    "TEMPLATE_DIRECTORY": os.path.join(BASE_DIR, "Platform", "templates", "emails"),
}

# Media Upload Settings
MEDIA_ROOT = os.path.join(BASE_DIR, "accounts", "mediafiles")
MEDIA_URL = "/media/"
