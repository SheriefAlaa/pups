from django.conf import settings
from django.conf.urls import patterns, include, url
from webchatapp.views import *

urlpatterns = patterns('',
     # Serves static files
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.STATIC_ROOT}),

    url(r'^$', home), # Root site, explains to users how to use webchat.
    url(r'^chat/(?P<token>\w{0,32})$', chat), # chat with a support assistant
    url(r'^login$', login),
    url(r'^logout$', logout), 
    url(r'^chpass$', change_password), 
    url(r'^logged$', logged_in),
    url(r'^tokens$', tokens_page), # Token management page
)