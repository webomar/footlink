from .base import *
ALLOWED_HOSTS = ["*"]

DEBUG = True

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
        'PASSWORD': 'E6aDDa365D4eF6ec3Caa-bB6BC5f1gab',
        'HOST': 'viaduct.proxy.rlwy.net',
        'PORT': '33811',
    }
}
