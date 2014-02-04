from django.conf.urls import patterns, include, url
from webchat.views import webchat, notfound
#from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webchat.views.home', name='home'),
    # url(r'^webchat/', include('webchat.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^chat$', webchat),
    url(r'^.*$', notfound),
)
