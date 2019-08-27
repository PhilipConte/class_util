"""
Django settings for class_util project.
https://docs.djangoproject.com/en/2.0/topics/settings/
https://docs.djangoproject.com/en/2.0/ref/settings/
https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/
"""

import os
import django_heroku

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ['CLASS_UTIL_SECRET_KEY']

DEBUG = os.environ.get('CLASS_UTIL_DEBUG', '0') == '1'

ALLOWED_HOSTS = os.environ.get('CLASS_UTIL_ALLOWED_HOSTS', '').split(',')

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
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'class_util.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',  'rest_framework.filters.OrderingFilter',),
    'DEFAULT_PAGINATION_CLASS': 'distributions.api.paginators.DistributionsLimitOffsetPaginator',
    'UNAUTHENTICATED_USER': None,
}

DJANGO_TABLES2_TEMPLATE = 'django_tables2/bootstrap-responsive.html'

CORS_ORIGIN_ALLOW_ALL = True

# Activate Django-Heroku.
django_heroku.settings(locals(), staticfiles=False)
