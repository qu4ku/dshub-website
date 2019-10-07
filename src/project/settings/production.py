from .base import *
import os

DEBUG = False
ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ.get('SECRET_KEY'),

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('NAME'),
        'USER': os.environ.get('USER'),
        'PASSWORD': os.environ.get('PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Needs to be updated
MEDIA_ROOT = '/var/www/datasciencevault/media/'
STATIC_ROOT = '/var/www/datasciencevault/static/'

# Conf for dropbox dbbackup
DBBACKUP_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DBBACKUP_STORAGE_OPTIONS = {
	'oauth2_access_token': os.environ.get('DB_AUTH'),
}