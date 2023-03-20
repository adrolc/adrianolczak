import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ADMINS = [('Adrian Olczak', 'adrianolczakdev@gmail.com')]

ALLOWED_HOSTS = ['adrianolczak.pl', 'www.adrianolczak.pl']

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRESQL_NAME'),
        'USER': os.environ.get('POSTGRESQL_USER'),
        'PASSWORD': os.environ.get('POSTGRESQL_PASSWORD'),
        'HOST': os.environ.get('POSTGRESQL_HOST'),
        'PORT': int(os.environ.get('POSTGRESQL_PORT')),
    }
}

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True