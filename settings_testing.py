# Django settings for bviz project.
# Uses sqlite for database, for faster setup / teardown.
from settings_common import *;

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': 'blogviz',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SOUTH_TESTS_MIGRATE = False
