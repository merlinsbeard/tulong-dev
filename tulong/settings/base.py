import os

import dj_database_url

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('bj paat', 'bjpaat01@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

DATABASES['default'] =  dj_database_url.config()


LOGIN_URL = '/login/'

#LOGIN_REDIRECT_URL = '/dashboard/'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts

ALLOWED_HOSTS = '*'


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Manila'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/medias/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

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
SECRET_KEY = 'dmd^(pyl_&amp;$0&amp;3c0(ez_7bq-n*k*$(gp_po1%0b^b3vwx#k76l'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    #
)

ROOT_URLCONF = 'tulong.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'tulong.wsgi.application'

TEMPLATE_DIRS = (
    'templates',
    'templates/job'

)

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django_admin_bootstrapped',
    'django.contrib.admin',
)

LOCAL_APPS=(
   'person',
   'job',
   'payment',
   'bid',
   'message',
   'comment',
   'discussion',
    )

THIRD_PARTY_APPS = (
    'south',
    'ckeditor',
    'storages',
    'easy_maps',
    'imagekit',
    #'django_markdown',
    #'gunicorn',   

    )

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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

from unipath import Path
PROJECT_ROOT = Path(__file__).ancestor(3)
MEDIA_ROOT = PROJECT_ROOT.child('medias')
STATIC_ROOT = PROJECT_ROOT.child('static')
STATIC_URL = 'http://localhost/tulong/static/'

STATICFILES_DIRS = (
    PROJECT_ROOT.child('assets'),
)

CKEDITOR_UPLOAD_PATH = PROJECT_ROOT.child('medias')

CKEDITOR_CONFIGS = {
    'awesome_ckeditor': {
        'toolbar': 'Basic',
        'height': 100,
        'width': 500,
        'skin': 'kama',
    },
}


#aws
AWS_ACCESS_KEY_ID     = os.environ['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = os.environ['aws_secret_access_key']
BOTO_S3_BUCKET        ='tulong'
#BOTO_S3_HOST=''
AWS_STORAGE_BUCKET_NAME = 'tulong'
S3_URL = 'http://s3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME

STATIC_DIRECTORY      = '/static/'
MEDIA_DIRECTORY       = '/media/'
STATIC_URL = S3_URL + STATIC_DIRECTORY
MEDIA_URL = S3_URL + '/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE   = 'storages.backends.s3boto.S3BotoStorage'

#email 
EMAIL_HOST          = 'smtp.live.com'
EMAIL_PORT          = 587
EMAIL_HOST_USER     = os.environ['tulongemail']
EMAIL_HOST_PASSWORD = os.environ['tulongemailpass']
EMAIL_USE_TLS       = True
#google map configurations
GOOGLEMAP_API_SENSOR = False
EASY_MAPS_GOOGLE_KEY = os.environ['map_key']
EASY_MAPS_CENTER = (14.625361, 121.124482)
MAPS_API_KEY = EASY_MAPS_GOOGLE_KEY

SERVER_EMAIL='cs@tulong.ph'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

##TWILIO settings
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_FROM_ = os.environ['TWILIO_FROM_']

