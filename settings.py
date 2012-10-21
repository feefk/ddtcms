# Django settings for ddtcms project.
import os

from datetime import datetime
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
# DEBUG =False
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME':   os.path.join(PROJECT_DIR,'data.db'),     #'./data.db'                    # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
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
LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR,'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR,'static').replace('\\','/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = '/static/admin/'

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ("images", os.path.join(STATIC_ROOT,'images').replace('\\','/')),
    ("css",    os.path.join(STATIC_ROOT,'css').replace('\\','/')),
    ("js",     os.path.join(STATIC_ROOT,'js').replace('\\','/')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'wu!&o$)@gtudfaab$vc6b8dk1s)8_(80^6fq+qzfh7sgn*r4$s'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'theme.loaders.filesystem_themes.Loader',
    #'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
'django.contrib.auth.context_processors.auth',
'django.core.context_processors.debug',
'django.core.context_processors.i18n',
'django.core.context_processors.media',
'django.core.context_processors.static',
'django.core.context_processors.request',
'django.core.context_processors.csrf',
'django.contrib.messages.context_processors.messages',
"navbar.context_processors.crumbs",
"navbar.context_processors.navbar",
"navbar.context_processors.navtree",
"navbar.context_processors.navbars",
"member.context_processors.site",
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'ddtcms.urls'


THEME_ROOT  = os.path.join(MEDIA_ROOT,'themes')
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


LOCALE_PATHS =(
    os.path.join(PROJECT_DIR,'locale'),
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django.contrib.markup',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'ddtcms.home',
    'ddtcms.blog',
    'ddtcms.notice',
    'ddtcms.news',
    'ddtcms.polls',
    'ddtcms.faq',
    'ddtcms.captcha',
    'ddtcms.link',
    'ddtcms.member',
    'ddtcms.theme',
    'ddtcms.guestbook',
    'ddtcms.rte.wmdeditor',
    'photologue',
    'navbar',
    'tagging',
    
)

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
REQUIRE_EMAIL_CONFIRMATION = False

AUTH_PROFILE_MODULE= 'member.profile'
LOGIN_URL          = '/member/login/'
LOGOUT_URL         = '/member/logout/'
LOGIN_REDIRECT_URL = '/member/profile/'
DEFAULT_AVATAR_WIDTH = 96
DEFAULT_AVATAR = os.path.join(MEDIA_ROOT, 'images','avatars', 'generic.jpg')


#ddtcms.com Google Maps API Key
GOOGLE_MAPS_API_KEY = "ABQIAAAAJz81xJlb4k9e_CHmKZP5-RQP6QTUJRZkkhnvOR0xqYc51BcN2BS4B0NS5NFfgPMCo3tSoTmJdcbAeg"


#http://docs.djangoproject.com/en/1.1/ref/settings/#absolute-url-overrides
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/member/profile/%s/" % u.username,
}

GRAPPELLI_ADMIN_TITLE="<a href='/'>return DDTCMS.com</a>"