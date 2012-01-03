from django.conf.urls.defaults import patterns, include, url

import bviz.views as v

urlpatterns = patterns('',
    (r'index/', v.index),
    (r'logged-in/', v.logged_in),
    (r'login-error/', v.login_error),
)
