# This file is part of Pups, a django/python project which contains
# web support tools
#
#  Author: Sherief Alaa <sheriefalaa.w@gmail.com>
#
#  Copyright:
#   (c) 2014 Sherief Alaa.
#   (c) 2014 The Tor Project, Inc.
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

from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^stats$', 'stats.views.stats_page'),
    url(r'^create_issue$', 'stats.views.create_issue'),
    url(r'^delete_issue$', 'stats.views.delete_issue_ajax'),
    url(r'^edit_issue$', 'stats.views.edit_issue_ajax'),
    url(r'^save_issue_edit$', 'stats.views.save_issue_edit_ajax'),
    url(r'^unlock_issue$', 'stats.views.unlock_issue_ajax'),
    url(r'^plus_one$', 'stats.views.plus_one_ajax'),
    url(r'^stats_data_ajax$', 'stats.views.stats_data_ajax'),
    
)
