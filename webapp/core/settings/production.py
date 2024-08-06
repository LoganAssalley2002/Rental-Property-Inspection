import os
from core.settings.common import *

DEBUG = False

SERVER_IP = os.environ.get('SERVER_IP')
DOMAIN = os.environ.get('DOMAIN')

ALLOWED_HOSTS = [SERVER_IP, DOMAIN]
CSRF_TRUSTED_ORIGINS = [f'https://*.{DOMAIN}', f'https://*.{SERVER_IP}']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': os.environ.get('DB_PORT'),
    }
}

STATIC_ROOT = '/home/ubuntu/static'
MEDIA_ROOT = '/home/ubuntu/media'
