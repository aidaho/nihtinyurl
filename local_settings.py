# -*- coding: utf-8 -*-
"""
Local machine-specific settings.
"""
import os

from settings import BASE_DIR

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(sw18#8(ixw$3hcwqp(6#9c$1g9nr*ipco&&+sfywvu+fn)5z-'
