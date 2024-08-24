from .base import *
ALLOWED_HOSTS = ["*"]

DEBUG = False

try:
    from .local import *
except ImportError:
    pass

SECRET_KEY = "django-insecure-6-n199)x+*ndh1(ea*oadw@&z2gkx9qa&la!i5l&al39e0bee="

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'uNVLMIFOIcXEpaXEECFshzsWnCgkHeVH',
        'HOST':'junction.proxy.rlwy.net',
        'PORT': '15394',
    }
}

MEDIA_URL = os.getenv('PRD_MEDIA_URL')
AWS_S3_ENDPOINT_URL = os.getenv('PRD_AWS_S3_ENDPOINT_URL')
print('this is production')
print('this is production')
print('this is production')
print('this is production')
print('this is production')
print('this is production')
print('this is production')
print('this is production')
print('this is production')