from django.conf.urls.defaults import patterns, include, url

import bviz.views as v
import bviz.ajax as ajax

def get_ajax_patterns():
  result = []
  function_names = [
    'profile', 'query','refresh_profile',
  ]
  for name in function_names:
    func = getattr(ajax, name)
    result.append(url(r'ajax/%s' % name, func))
  return result

ajax_patterns = get_ajax_patterns()
urlpatterns = patterns('',
    (r'index/', v.index),
    (r'logged-in/', v.logged_in),
    (r'login-error/', v.login_error),
    (r'profile/', v.all_profiles),
    *ajax_patterns
)
