import environ
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize django-environ
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

# Security
SECRET_KEY = env("SECRET_KEY", default="your-default-secret-key")
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    "anymail",  # Added for Brevo email integration

    # TicketEase apps
    "apps.users",
    "apps.movies",
    "apps.events",
    "apps.bookings",
    "apps.payments",
    "apps.notifications",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("POSTGRES_DB"),
        'USER': env("POSTGRES_USER"),
        'PASSWORD': env("POSTGRES_PASSWORD"),
        'HOST': env("POSTGRES_HOST"),
        'PORT': env.int("POSTGRES_PORT"),
    }
}

# Custom User Model
AUTH_USER_MODEL = "users.CustomUser"

# Static and Media Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


#  Brevo SMTP Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp-relay.brevo.com"  # Ensure this matches Brevo SMTP relay
EMAIL_PORT = 587  # Brevo uses port 587 for TLS
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER")  # Use your Brevo email
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")  # Brevo SMTP API key
DEFAULT_FROM_EMAIL = "TicketEase <noreply@ticketease.com>"



ANYMAIL = {
    "EMAIL_HOST_PASSWORD": env("EMAIL_HOST_PASSWORD"),
}

# Authentication Settings
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
#LOGIN_REDIRECT_URL = "/payments/checkout/"

# Stripe API Key
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_PARSER_CLASSES': ['rest_framework.parsers.JSONParser'],
}
