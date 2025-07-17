from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security key (keep it secret, don't share this in public repositories)
SECRET_KEY = 'django-insecure-7tgm*btfveg5lwxiukrqm24236numr-jx&7!kaf!b28d0q%9!p'

# Debug mode (set to False in production)
DEBUG = True

# Hosts allowed to access this application
ALLOWED_HOSTS = []

# URL configuration
ROOT_URLCONF = 'crm_project.urls'

# Application definition
INSTALLED_APPS = [
    "jazzmin",  # Jazzmin admin theme (optional, but recommended for better UI)

    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',

    # UI / admin helpers
    "import_export",               # django-import-export
    "simple_history",              # django-simple-history
    "adminsortable2",              # django-admin-sortable2
    "django_otp",
    "django_otp.plugins.otp_totp",   # TOTP tokens
    "two_factor",                    # the wrapper UI+flows

    # Your apps
    'apps.website',
    'apps.accounts',
    'apps.dashboard',
    'apps.customers',
    'apps.activity.apps.ActivityConfig',
    "apps.jobs.apps.JobsConfig",
    'apps.tasks.apps.TasksConfig',
    'apps.invoices',

    'apps.activity.apps.ActivityConfig',
    'apps.jobs',
    'apps.tasks.apps.TasksConfig',
    'apps.invoices',

    # 3rd-party apps
    'rest_framework',
    'corsheaders',
    'widget_tweaks',
    'django_filters',                # Django REST Framework filters
    'django_extensions',             # Useful for development (shell_plus, graph_models, etc.)
    'django.contrib.humanize',       # Humanize numbers and dates in templates
    'django.contrib.sites',          # Required for Django Allauth
    'allauth',                       # Django Allauth for authentication
    'allauth.account',               # Django Allauth account management    
    'allauth.socialaccount',         # Django Allauth social account management
    'allauth.socialaccount.providers.google',  # Google OAuth2 provider
    'allauth.socialaccount.providers.github',  # GitHub OAuth2 provider
    'allauth.socialaccount.providers.facebook',  # Facebook OAuth2 provider
    'allauth.socialaccount.providers.twitter',  # Twitter OAuth2 provider
    
]

SITE_ID = 1 

# minimal allauth settings
ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "optional"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Middleware configuration
MIDDLEWARE = [
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

    # only if using sites framework (e.g. allauth, flatpages, sitemaps):
    "django.contrib.sites.middleware.CurrentSiteMiddleware",

    # conditional GET support (this replaces the old ETagMiddleware)
    "django.middleware.http.ConditionalGetMiddleware",

    # clickjacking protection
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # locale (if you internationalize)
    "django.middleware.locale.LocaleMiddleware",

    'django.middleware.cache.FetchFromCacheMiddleware',  # Middleware for caching
    'django.middleware.cache.UpdateCacheMiddleware',  # Middleware for caching
    'django.middleware.http.ConditionalGetMiddleware',  # Middleware for conditional GET
]

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Points to the templates directory
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

# Static files (CSS, JavaScript, images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / "static"]
ADMIN_STYLES = ["admin/css/local_overrides.css"]

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'SecureCRM_2',                # ← PostgreSQL DB name
        'USER': 'admin_user',               # ← PostgreSQL user
        'PASSWORD': 'BAHBEJ-TUHWO2-wYCHEQ',
        'HOST': '156.38.163.242',           # ← Server IP
        'PORT': '5432',
    }
}

# Django Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}

# Default auto field for models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
LOGIN_URL = '/accounts/login/'    # when you call @login_required, send folks here
LOGIN_REDIRECT_URL = '/home/'     # after a successful login, send them here
LOGOUT_REDIRECT_URL = 'accounts:login'

# Email settings for using Gmail SMTP server

import os
from dotenv import load_dotenv          # pip install python-dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv (BASE_DIR / ".env", override=False)

ENV = os.getenv("DJANGO_ENV", "development")

# e-mail back-end
if ENV == "production":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
elif ENV == "staging":
    EMAIL_BACKEND  = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = BASE_DIR / "tmp_emails"
else:                           # development
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_HOST = 'smtp.gmail.com'  # Gmail SMTP server
EMAIL_PORT = 587  # SMTP port for TLS
EMAIL_USE_TLS = True  # Use TLS encryption
EMAIL_HOST_USER = 'goodiematthews@gmail.com'  # Your Gmail address (replace with your email)
EMAIL_HOST_PASSWORD = 'MarmalaideSandwich'  # Your Gmail app-specific password
DEFAULT_FROM_EMAIL = 'goodiematthews@gmail.com'  # Default sender email (replace with your email)

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "send-reminders-every-minute": {
        "task": "tasks.tasks.send_due_reminders",
        "schedule": crontab(),        # every minute
    },
}

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=False)

ENV = os.getenv("DJANGO_ENV", "development")

# For development, print email content to the console instead of sending it (uncomment for testing)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Uncomment for testing
