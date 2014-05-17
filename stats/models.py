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

from django.db import models


class Issue(models.Model):
    issue_id = models.CharField(max_length=64)
    text = models.TextField()
    frequency = models.IntegerField()
    created_by = models.CharField(max_length=64)
    is_locked = models.BooleanField()
    locked_by = models.CharField(max_length=64)
    last_edited_by = models.CharField(max_length=64)

    def __unicode__(self):
        return u'ID: %s Owner: %s Text: %s' % (self.issue_id, self.owner, self.text)
