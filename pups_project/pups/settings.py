# Django settings for pups project.
import os
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
#DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'

# Removes trailing slash in urls
APPEND_SLASH=False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.abspath(os.path.join(os.path.dirname( __file__ ),  'databases/pups.db')),  # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

ALLOWED_HOSTS = ['*']

TIME_ZONE = 'GMT'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = ''

MEDIA_URL = ''

STATIC_ROOT = '/home/sherief/Projects/Work/pups/pups_project/'

STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
   # '/home/sherief/Projects/Work/pups/pups_project/static',
    #os.path.join(PROJECT_PATH, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5sdi_mga9(e01n7vm=qteo-r*v@g%uc483p@wqo%07pfb9q_0i'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'pups.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'pups.wsgi.application'

TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'templates/')),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pups',
    'webchat',
    'stats',
)

TEMPLATE_CONTEXT_PROCESSORS = (
"django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages",
"django.core.context_processors.request"
)

# pups custom configuration 
CONFIG = {
    'server' : 'localhost:8000',# eg: 188.226.179.216
    'bosh' : 'http://188.226.179.216/http-bind', # eg: http://188.226.179.216/http-bind
    'receiver' : '@localhost', # XMPP support assistant address eg: @localhost or @whatever.lit
    'expiration_days' : 3
}