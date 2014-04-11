from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

	# Serves static files
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.STATIC_ROOT}),

    # Handles login and logout
    url(r'^login$', 'pups.views.custom_login'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),

    # Apps urls
    url(r'', include('webchat.urls', 'webchat')),
    url(r'', include('stats.urls', 'stats')),
) 