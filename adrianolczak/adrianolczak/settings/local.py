from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-mn$fnh=--_0et(ep_-(fsk!$qyeefijz(p&f*iyauy-+5k&4^t"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Email backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
