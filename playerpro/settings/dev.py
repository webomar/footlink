from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-6-n199)x+*ndh1(ea*oadw@&z2gkx9qa&la!i5l&al39e0bee="

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass

MEDIA_URL = os.getenv('DEV_MEDIA_URL')
AWS_S3_ENDPOINT_URL = os.getenv('DEV_AWS_S3_ENDPOINT_URL')

print('this is dev')
print('this is dev')
print('this is dev')
print('this is dev')
print('this is dev')
print('this is dev')
print('this is dev')
print('this is dev')
print('this is dev')
print('this is dev')
print('this is dev')
