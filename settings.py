# Django settings for bviz project.
from settings_etc import *;

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'blogviz',                      
        'USER': 'liblist',                      
        'PASSWORD': 'liblist',                  
        'HOST': '',                      
        'PORT': '',                      
    }
}
MONGODB_NAME = 'blogviz'

SECRET_KEY = '^=c@y)-rkxi#+_3k!9&c6@x)t%h=)3u#!e+byewim)&3r^1ynr'
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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    # First party apps.
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Third party apps
    'social_auth',
    'south',
    'debug_toolbar',
    # Actual application.
    'bviz',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "social_auth.context_processors.social_auth_by_type_backends",
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.google.GoogleOAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_ENABLED_BACKENDS = ('google-oauth','google')

###
# Google settings
### 
GOOGLE_OAUTH2_CLIENT_ID = '412634461797-f8r3oc7k3q0pvokde3emlcf7mnv2lh2a.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = "2NAL_U4RYGkxuMta4XY1X0Xh"
# Extra permissions for Google.
GOOGLE_OAUTH_EXTRA_SCOPE = [
  'https://www.googleapis.com/auth/analytics.readonly',
]
GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
  'access_type': 'offline',
  'approval_prompt': 'force',
}

# Required for social-auth.
LOGIN_URL          = '/login-form/'
LOGIN_REDIRECT_URL = '/logged-in/'
LOGIN_ERROR_URL    = '/login-error/'

# pymongo related settings.
# import mongoengine
# mongoengine.connect(MONGODB_NAME)
