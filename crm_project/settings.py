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
    'django_tenants',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',

    # Your app
    'apps.website',
    'apps.accounts',
    'apps.dashboard',
    'apps.customers',

    'apps.activity.apps.ActivityConfig',
    'apps.jobs',
    'apps.tasks.apps.TasksConfig',
    'apps.invoices',

    # 3rd-party apps
    'rest_framework',
    'corsheaders',
    'widget_tweaks',  # ✅ Added here
]

# Multi-tenancy settings
SHARED_APPS = [
    'django_tenants',  # Must be first
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps that are NOT tenant-specific
    'apps.tenants',  # We'll create this next
]

TENANT_APPS = [
    # Apps that ARE tenant-specific (separate data per company)
    'apps.website',
    'apps.accounts',
    'apps.dashboard',
    'apps.customers',
    'apps.jobs',
    'apps.tasks',
    'apps.invoices',
    'apps.activity',
    
    'rest_framework',
    'corsheaders',
    'widget_tweaks',
]

TENANT_MODEL = "tenants.Organization"
TENANT_DOMAIN_MODEL = "tenants.Domain"

# Middleware configuration
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'SecureCRM_MultiTenant',  # PostgreSQL name
        'USER': 'admin_user',               # ← PostgreSQL user
        'PASSWORD': 'BAHBEJ-TUHWO2-wYCHEQ',
        'HOST': '156.38.163.242',           # ← Server IP
        'PORT': '5432',
    }
}

DATABASE_ROUTERS = [
    'django_tenants.routers.TenantSyncRouter',
]

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
