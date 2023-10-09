import os

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ADMINS = [("Adrian Olczak", "adrianolczakdev@gmail.com")]

ALLOWED_HOSTS = ["adrianolczak.pl", "www.adrianolczak.pl"]

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
DEFAULT_FROM_EMAIL = "blog@adrianolczak.pl"
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_USE_TLS = True


SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
