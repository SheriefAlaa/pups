from django.conf import settings
from django.conf.urls import patterns, url

urlpatterns = patterns('',
     # Serves static files
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.STATIC_ROOT}),

    url(r'^$', 'webchat.views.home'), # Root site, explains to users how to use webchat.
    url(r'^chat/(?P<token>\w{0,32})$', 'webchat.views.chat'), # chat with a support assistant
    url(r'^login$', 'webchat.views.login'),
    url(r'^logout$', 'webchat.views.logout'), 
    url(r'^chpass$', 'webchat.views.change_password'), 
    url(r'^logged$', 'webchat.views.logged_in'),
    url(r'^tokens$', 'webchat.views.tokens_page'), # Token management page
)