from .base_settings import *

try:
    from .local_settings import *
except ImportError:
    pass

assert SECRET_KEY
