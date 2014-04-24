from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'webchat.views.index'), # Root client interface page eg: webchat.torproject.org
    url(r'^chat/(?P<token>\w{0,32})$', 'webchat.views.chat'), # chat with a support assistant
    url(r'^tokens$', 'webchat.views.tokens_page'), # Token management page
)