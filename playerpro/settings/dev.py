from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass

MEDIA_URL = os.getenv('DEV_MEDIA_URL')
AWS_S3_ENDPOINT_URL = os.getenv('DEV_AWS_S3_ENDPOINT_URL')



DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'uNVLMIFOIcXEpaXEECFshzsWnCgkHeVH',
        'HOST':os.getenv('DEV_PGHOST'),
        'PORT':os.getenv('DEV_PGPORT'),
    }
}

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
