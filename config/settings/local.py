from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'my_ancestors',
        'USER': 'doogan',
        'PASSWORD': 'doogan',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
