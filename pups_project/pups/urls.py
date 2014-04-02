from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'', include('webchat.urls', 'webchat')),
    url(r'', include('stats.urls', 'stats')),
)