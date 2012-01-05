# Django settings for bviz project.
from settings_common import *;

DEBUG = True
TEMPLATE_DEBUG = DEBUG

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
