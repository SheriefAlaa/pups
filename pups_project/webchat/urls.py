from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'webchat.views.home'), # Root site, explains to users how to use webchat.
    url(r'^chat/(?P<token>\w{0,32})$', 'webchat.views.chat'), # chat with a support assistant
    url(r'^chpass$', 'webchat.views.change_password'), 
    url(r'^tokens$', 'webchat.views.tokens_page'), # Token management page
)