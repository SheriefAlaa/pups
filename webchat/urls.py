from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    # Root client interface page eg: webchat.torproject.org
    url(r'^$', 'webchat.views.index'),
    # chat with a support assistant
    url(r'^chat/(?P<token>\w{0,32})$', 'webchat.views.chat'),
    # Token management page
    url(r'^tokens$', 'webchat.views.tokens_page'),
)
