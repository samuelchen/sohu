# -*- coding: utf-8 -*-

import os
import sys
import socket

sys.path.append(os.path.dirname(__file__))

PRODUCTION_SERVER_HOSTNAMES = ('tc_69_53', 'tc_69_54')

if  socket.gethostname() in PRODUCTION_SERVER_HOSTNAMES:
    IS_PRODUCTION_SERVER = True
else:
    IS_PRODUCTION_SERVER = False
    
if IS_PRODUCTION_SERVER:
    DEBUG = TEMPLATE_DEBUG = False
else:
    DEBUG = TEMPLATE_DEBUG = True

ADMINS = (
    ('admin', 'admin@sohu-inc.com'),
)

MANAGERS = ADMINS
try:
    import local_settings
except ImportError:
    raise

DATABASES = {
    'default': {
        'ENGINE': local_settings.DATABASE_ENGINE, # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': local_settings.DATABASE_NAME,                      # Or path to database file if using sqlite3.
        'USER': local_settings.DATABASE_USER,                      # Not used with sqlite3.
        'PASSWORD': local_settings.DATABASE_PASSWORD,                  # Not used with sqlite3.
        'HOST': local_settings.DATABASE_HOST,                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': local_settings.DATABASE_PORT,                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_hm)58*^+c!n_ytsqbw#n=!2px1xl58$b3yzkdro4e&^^@*_-n'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'SohuPocketLib.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#    'django.contrib.admin',
#    'django.contrib.admindocs',
    'djcelery',
#    'storage',
#    'article',
#    'image',
#    'page',
    'user',
    'south'
)

if  socket.gethostname() in PRODUCTION_SERVER_HOSTNAMES:
    CACHE_BACKEND = 'memcached://10.10.69.53:11211;10.10.69.54:11211/?timeout=60'
else:
#    CACHE_BACKEND = 'memcached://localhost/?timeout=60'
    CACHE_BACKEND = 'db://cache?timeout=3600'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

import djcelery
djcelery.setup_loader()

BROKER_HOST = local_settings.BROKER_HOST
BROKER_PORT = local_settings.BROKER_PORT
BROKER_USER = local_settings.BROKER_USER
BROKER_PASSWORD = local_settings.BROKER_PASSWORD
BROKER_VHOST = local_settings.BROKER_VHOST

CELERY_DISABLE_RATE_LIMITS = True

CELERY_QUEUES = {
                 "default": {
                             "exchange": "default",
                             "binding_key": "default"
                             },
                 "upload": {
                            "exchange": "media",
                            "exchange_type": "topic",
                            "binding_key": "#.upload",
                            },
                 "download": {
                              "exchange": "media",
                              "exchange_type": "topic",
                              "binding_key": "#.download",
                              },
                 "encode": {
                            "exchange": "media",
                            "exchange_type": "topic",
                            "binding_key": "#.encode",
                            },
                 "store": {
                           "exchange": "media",
                           "exchange_type": "topic",
                           "binding_key": "#.store",
                           },
                 "article": {
                          "exchange": "media",
                          "exchange_type": "topic",
                          "binding_key": "article.#",
                          },
                 "image": {
                           "exchange": "media",
                           "exchange_type": "topic",
                           "binding_key": "image.#",
                           },
                 "audio": {
                           "exchange": "media",
                           "exchange_type": "topic",
                           "binding_key": "audio.#",
                           },
                 "video": {
                           "exchange": "media",
                           "exchange_type": "topic",
                           "binding_key": "video.#",
                           },
                 }

CELERY_DEFAULT_QUEUE = "default"
CELERY_DEFAULT_EXCHANGE = "default"
CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_DEFAULT_ROUTING_KEY = "default"

AWS_SECRET_ACCESS_KEY = 'rfUdPSAC2hXhHMGG0wXiHcxeuEpqybEGxn8xPYMy'
AWS_ACCESS_KEY_ID = 'AKIAIXEPRIJSQA4A2KOA'

APP_ID = '1088'
APP_KEY = "f9#7V-RA)pnnXfE0Xq'jFb2t<m-43T"