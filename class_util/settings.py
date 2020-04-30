"""
https://docs.djangoproject.com/en/2.0/topics/settings/
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

from os import environ, path
import dj_database_url

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

SECRET_KEY = environ.get('CLASS_UTIL_SECRET_KEY')

DEBUG = int(environ.get('CLASS_UTIL_DEBUG'))

ALLOWED_HOSTS = environ.get('CLASS_UTIL_ALLOWED_HOSTS').split(',')

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'distributions',
    'django_tables2',
    'django_filters',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'class_util.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'class_util.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}

USE_TZ = False
USE_I18N = False
USE_L10N = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',  'rest_framework.filters.OrderingFilter',),
    'DEFAULT_PAGINATION_CLASS': 'distributions.api.paginators.DistributionsLimitOffsetPaginator',
    'UNAUTHENTICATED_USER': None,
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = ('GET', 'OPTIONS',)
