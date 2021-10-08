"""
Django settings for Main project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from .env import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$bkt&r3q#t*wix#uyfrj!khf0o+j-_$8=pfgc+$r!1+7giouat'
ENCRYPTION_KEY = b'G7Kh5fJ9FsNZA5F43FdRQQJtehMKx4Xico9J6haHBM8='
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = IS_PROD is False

ALLOWED_HOSTS = []

# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    "storages",
    'django_user_agents',
    'Apps.Users',
    'Apps.Authentication',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'Main.urls'

AUTH_USER_MODEL = "Users.User"

AUTHENTICATION_BACKENDS = ["Apps.Users.backend.UserAuthenticateBackend"]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'Templates'],
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

WSGI_APPLICATION = 'Main.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'HOST': DB_HOST,
        'PASSWORD': DB_PASSWORD,
        'PORT': DB_PORT,
        'USER': DB_USER

    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25

}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# AUTH_USER_MODEL = "Users.models.User"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# S3 BUCKETS CONFIG

MEDIA_URL = f"/media/"
MEDIA_ROOT = BASE_DIR / "Assets/Media"

if USE_AWS:
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_S3_REGION_NAME = "ap-southeast-1"

    MEDIAFILES_LOCATION = 'Media'
    STATICFILES_LOCATION = 'Static'

    DEFAULT_FILE_STORAGE = 'Main.storages.MediaStorage'
    STATICFILES_STORAGE = 'Main.storages.StaticStorage'


STATICFILES_DIRS = [
    BASE_DIR / "Assets/Static",
]

STATIC_ROOT = BASE_DIR / "Assets/StaticRoot"

FILE_UPLOAD_TEMP_DIR = BASE_DIR / "Assets" / "__temp__"

STATIC_URL = '/static/'

# CORS_ALLOWED_ORIGINS = [
#     WHITELIST_URL
# ]
#
# CORS_ORIGIN_WHITELIST = (
#     WHITELIST_URL
# )

CORS_ORIGIN_ALLOW_ALL = IS_PROD is False
