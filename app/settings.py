"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from string import Template

import environ

env = environ.Env()
environ.Env.read_env('./.env')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('DJANGO_SECRET_KEY', default="")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

INTERNAL_IPS = env.list(
    'INTERNAL_IPS',
    default=[
        '127.0.0.1',
    ],
)

# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'livereload',

    'django.contrib.staticfiles',

    'corsheaders',
    'debug_toolbar',

    'django_celery_results',
    'django_celery_beat',

    "games.apps.GamesConfig",
    "bot.apps.BotConfig"
]

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'livereload.middleware.LiveReloadScript',
]

if not DEBUG:
    MIDDLEWARE.remove('debug_toolbar.middleware.DebugToolbarMiddleware')
    MIDDLEWARE.remove('livereload.middleware.LiveReloadScript')

X_FRAME_OPTIONS = 'SAMEORIGIN'
SILENCED_SYSTEM_CHECKS = ['security.W019']

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = env.list(
    'CORS_ALLOWED_ORIGINS', default=[
        'http://localhost:8000',
        'http://127.0.0.1:8000',
    ]
)
CSRF_TRUSTED_ORIGINS = env.list(
    'CORS_ALLOWED_ORIGINS', default=[
        'http://localhost:8000',
        'http://127.0.0.1:8000',
    ]
)

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {},
    'dev': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'prod': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env('DATABASE_HOST', default='postgres'),
        'PORT': env.int('DATABASE_PORT', default=5432),
        'CONN_MAX_AGE': env.int('DATABASE_CONN_MAX_AGE', default=30),
        'NAME': env('DATABASE_NAME', default='postgres'),
        'USER': env('DATABASE_USER', default='postgres'),
        'PASSWORD': env('DATABASE_PASSWORD', default='postgres'),
        'OPTIONS': {
            'sslmode': env('DATABASE_SSL_MODE', default='prefer'),
        },
    }
}

USE_SQLITE = env.bool('USE_SQLITE', default=False)
DATABASES['default'] = DATABASES['dev'] if USE_SQLITE else DATABASES['prod']

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [Path(BASE_DIR) / 'locale']

MEDIA_URL = 'media/'
MEDIA_ROOT = Path(BASE_DIR) / 'media'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = Path(BASE_DIR) / 'static'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


REDIS_HOST = env('REDIS_HOST', default=None)
REDIS_PORT = env.int('REDIS_PORT', default=6379)
REDIS_FSM_DB = env.int('REDIS_FSM_DB', default=0)
REDIS_DB = env.int('REDIS_DB', default=1)
REDIS_CELERY_DB = env.int('REDIS_CELERY_DB', default=2)

CELERY_BROKER_URL = env('CELERY_BROKER_URL', default=f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}")
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default="django-db")
CELERY_BEAT_SCHEDULER = env('CELERY_BEAT_SCHEDULER', default='django_celery_beat.schedulers:DatabaseScheduler')
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = env.bool('CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP', default=True)
CELERY_TIMEZONE = env('CELERY_TIMEZONE', default='UTC')

BOT_TOKEN = env('BOT_TOKEN', default=None)
ADMINS = env.list('ADMINS', cast=int, default=[])
PAGE_SIZE = env.int("PAGE_SIZE", default=10)

SEQ_KEY = env('SEQ_KEY', default=None)
SEQ_URL = env('SEQ_URL', default=None)
SEQ_BATCH = env.int('SEQ_BATCH', default=10)
SEQ_TIMEOUT = env.int('SEQ_TIMEOUT', default=10)
SEQ_LEVEL = env.int('SEQ_LEVEL', default=20)

HELP_COMMAND = env('HELP_COMMAND', default="help")
RANDOM_CHOICE_GAME_COMMAND = env('RANDOM_CHOICE_GAME_COMMAND', default="random_choice_game")
CREATE_PUNISHMENT_COMMAND= env('CREATE_PUNISHMENT_COMMAND', default="create_punishment")
SHOW_USER_STATS_COMMAND = env('SHOW_USER_STATS_COMMAND', default="user_stats")
SHOW_CHAT_STATS_COMMAND = env('SHOW_CHAT_STATS_COMMAND', default="chat_stats")
CHAT_SETTINGS_COMMAND = env('CHAT_SETTINGS_COMMAND', default="chat_settings")
