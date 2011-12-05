# Django settings for indivo project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# base URL for the app
import os
APP_HOME = os.path.abspath(os.path.dirname(__file__))

# URL prefix
SITE_URL_PREFIX = "http://localhost:8000"

# Audit Settings
AUDIT_LEVEL = 'HIGH' # 'HIGH', 'MED', 'LOW', 'NONE'
AUDIT_OAUTH = True # Audit the calls used solely for the oauth dance?
AUDIT_FAILURE = True # Audit the calls that return with unsuccessful status (4XX, 5XX)?

ADMINS = (
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'indivo'             # Or path to database file if using sqlite3.
DATABASE_USER = 'indivo'             # Not used with sqlite3.
DATABASE_PASSWORD = 'indivo'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.

## IMPORTANT for Indivo: do NOT change this timezone to your local timezone.
## KEEP IT as UTC.
TIME_ZONE = 'UTC'

## ALSO, we recommend that, if you use PostgreSQL, you set the timezone to UTC in postgresql.conf

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = APP_HOME + '/indivo_files/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'REPLACEMENOW'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'indivo_server.indivo.middlewares.authentication.Authentication',
    'indivo_server.indivo.middlewares.paramloader.ParamLoader',
    'indivo_server.indivo.middlewares.authorization.Authorization',
    'indivo_server.indivo.middlewares.audit.AuditWrapper'
)


ROOT_URLCONF = 'indivo_server.urls'

TEMPLATE_DIRS = (
  APP_HOME + "/templates",
  APP_HOME + "/indivo/templates"
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'indivo',
    'codingsystems',
    # for migrations
    'south',
)

XSLT_STYLESHEET_LOC = APP_HOME + '/indivo/document_processing/stylesheets/'
XSD_SCHEMA_LOC = APP_HOME + '/schemas/doc_schemas/'
VALIDATE_XML_SYNTAX = True # Validate all incoming XML docs for basic syntax?
VALIDATE_XML = True # Validate XML docs to process against the Indivo schemas?

# the standard port for the UI server is 80 on the same machine
UI_SERVER_URL = 'http://localhost'

# cookie
SESSION_COOKIE_NAME = "indivo_sessionid"

# auth
LOGIN_URL = "/account/login"

# no trailing slash just because
APPEND_SLASH = False

# email
EMAIL_HOST = ""
EMAIL_PORT = 25
EMAIL_FROM_ADDRESS = "Indivo <support@indivo.localhost>"
EMAIL_SUPPORT_ADDRESS = "support@indivo.localhost"
EMAIL_SUPPORT_NAME = "Indivo Support"


# excluse a URL pattern from access control
INDIVO_ACCESS_CONTROL_EXCEPTION = "^/codes/"

# logging
import logging
logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s %(levelname)s %(message)s',
	    filename = APP_HOME + '/indivo.log', filemode = 'a'
	    )

# send email?
SEND_MAIL = False

# default carenets for new records
INDIVO_DEFAULT_CARENETS = ['Family', 'Physicians', 'Work/School']

# timeout before reenabling a disabled account
# time in seconds. None if you don't want reenabling
ACCOUNT_REENABLE_TIMEOUT = None
