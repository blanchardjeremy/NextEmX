import sys
import os


# assume we are ./apps/mainsite/settings.py
APPS_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
if APPS_DIR not in sys.path:
    sys.path.insert(0, APPS_DIR)

from mainsite import TOP_DIR

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'mainsite',
    'nextemx',
    'routeshout',
]

JINGO_EXCLUDE_APPS = ['admin']


MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
]


TEMPLATE_LOADERS = [
	'jingo.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


STATICFILES_DIRS = [
]

STATIC_ROOT = os.path.join(TOP_DIR, 'static')
MEDIA_ROOT = os.path.join(TOP_DIR, 'uploads')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL+'admin/'





ROOT_URLCONF = 'mainsite.urls'

TEMPLATE_DIRS = (
    os.path.join(TOP_DIR, 'templates'),
)

SITE_ID = 1

USE_I18N = True
USE_L10N = True



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




#### Local settings

# try to import settings_local if present
try:
    from settings_local import *
except ImportError as e:
    pass


def get_local_config(variable_name, default=None):
    """
    Allows for configuration to happen with environmental variables (for Heroku) or python variables (for PyCharm)
    """
    py_var = locals().get(variable_name)
    if py_var:
        return py_var
    os_var = os.environ.get(variable_name)
    if os_var:
        return os_var
    return default


DEBUG = get_local_config('DJANGO_DEBUG', True)
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'

ROUTESHOUT_API_KEY = get_local_config('ROUTESHOUT_API_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': get_local_config('DB_NAME', ''),                      # Or path to database file if using sqlite3.
        'USER': get_local_config('DB_USER', ''),
        'PASSWORD': get_local_config('DB_PASS', ''),
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': '',
        'TIMEOUT': 300,
        'KEY_PREFIX': '',
        'VERSION': 1,
    }
}


if DEBUG:
    # Example of how to include debug toolbar in local_settings
    MIDDLEWARE_CLASSES.insert(0,'debug_toolbar.middleware.DebugToolbarMiddleware')
    INSTALLED_APPS.append('debug_toolbar')
    INTERNAL_IPS = (
       '127.0.0.1',
    )
    JINGO_EXCLUDE_APPS.append('debug_toolbar')
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False
    }
