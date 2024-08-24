from .base import *
ALLOWED_HOSTS = ["*"]

DEBUG = False

try:
    from .local import *
except ImportError:
    pass


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