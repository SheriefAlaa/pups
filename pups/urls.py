# This file is part of Pups, a django/python project which contains
# web support tools
#
#  Author: Sherief Alaa <sheriefalaa.w@gmail.com>
#
#  Copyright:
#   © 2014 Sherief Alaa.
#   © 2014 The Tor Project, Inc.
#
# Pups is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pups is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pups.  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',

    # Serves static files
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),

    # Handles login and logout
    url(r'^login$', 'pups.views.custom_login'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^chpass$', 'pups.views.change_password'),

    # Pups views
    url(r'^home$', 'pups.views.home'),

    # Apps urls
    url(r'', include('webchat.urls', 'webchat')),
    url(r'', include('stats.urls', 'stats')),
)
