import os
from djoonga.conf import jconfig

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

SITE_ID = 1

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'               # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = jconfig.db
DATABASE_USER = jconfig.user         # Not used with sqlite3.
DATABASE_PASSWORD = jconfig.password # Not used with sqlite3.
DATABASE_HOST = jconfig.host         # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '4040'               # Set to empty string for default. Not used with sqlite3.

# Don't share this with anybody.
SECRET_KEY = jconfig.secret

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'djoonga.users.JoomlaAuthenticationBackend',
)

ROOT_URLCONF = ('djoonga.urls')

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'djoonga.contrib.users',
    'djoonga.contrib.articles',
    'djoonga.contrib.categories',
    'djoonga.contrib.menus',
    'djoonga.contrib.modules'
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)