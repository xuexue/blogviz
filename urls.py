from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('bviz.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
