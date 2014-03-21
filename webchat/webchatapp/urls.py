from django.conf import settings
from django.conf.urls import patterns, include, url
from webchatapp.views import *
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

    # Serves static files
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.STATIC_ROOT}),

    url(r'^$', home), # Root site, explains to users how to use webchat.
    #url(r'^chat/[a-z0-9]{32}$', check_token), # chat with a support assistant
    url(r'^chat/(?P<token>\w{0,32})$', chat), # chat with a support assistant
    url(r'^login$', login),
    url(r'^logout$', logout), 
    url(r'^chpass$', change_password), 
    url(r'^logged$', logged_in),
    url(r'^tokens$', tokens_page), # Token management page
    # url(r'^.*$', not_found), # Catches everything that's not a page and has to be the last rule.
)
