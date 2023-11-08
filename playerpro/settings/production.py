from .base import *
ALLOWED_HOSTS = ["*"]

DEBUG = True

try:
    from .local import *
except ImportError:
    pass
