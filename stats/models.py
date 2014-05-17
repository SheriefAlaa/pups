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

import datetime
from django.db import models
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.utils import timezone
from pups import settings


# Status codes
_issueDoesNotExist, _issuesIsLocked, _issueIsNotLocked, \
_failure = range(1,5)

class Issue(models.Model):
    text = models.TextField()
    frequency = models.IntegerField(default=1)
    created_by = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited_at = models.DateTimeField(auto_now_add=True)
    is_locked = models.BooleanField(default=False)
    locked_by = models.CharField(max_length=64)
    locked_since = models.DateTimeField(null=True)
    last_edited_by = models.CharField(max_length=64)

    def __unicode__(self):
        return u'ID: %s Text: %s Freq: %s locked: %s' % \
            (self.pk, self.text, self.frequency, self.is_locked)

    @staticmethod
    def get_issues_json():
        return serializers.serialize(
            "json",
            Issue.objects.all().order_by('-frequency'))

    @staticmethod
    def create_issue(user, text):
        q = Issue(
            text=text,
            created_by=user
            )
        q.save()

        return q.id is not None

    @staticmethod
    def delete_issue(id):
        issue = Issue.objects.filter(id=id)
        issue.delete()

    @staticmethod
    def save_edit(id, edited_text, user):
        issue = Issue.objects.filter(id=id)

        if not issue:
            return _failure

        issue.update(text=edited_text)
        issue.update(last_edited_by=user)

    @staticmethod
    def plus_one(id):
        issue = Issue.objects.filter(id=id)
        issue.update(frequency=F('frequency')+1)

    @staticmethod
    def lock(id, user):
        issue = Issue.objects.filter(id=id)
        issue.update(is_locked=True)
        issue.update(locked_since=timezone.now())
        issue.update(locked_by=user)

    @staticmethod
    def unlock(id):
        issue = Issue.objects.filter(id=id)

        if not issue:
            return _failure

        issue.update(is_locked=False)
        issue.update(locked_by="")

    @staticmethod
    def lock_status(id):
        '''
        Returns a single issue's status code and unlocks it if it's
        less than timezone.now() < locked_until
        '''
        try:
            issue_obj = Issue.objects.get(id=id)
        except ObjectDoesNotExist:
            return [_issueDoesNotExist]

        if issue_obj.is_locked:
            locked_until = issue_obj.locked_since + datetime.timedelta(
                           minutes=settings.CONFIG['edit_lock_expiration'])
            
            if timezone.now() < locked_until:
                return [_issuesIsLocked, issue_obj.locked_by, 
                        (locked_until - timezone.now()).seconds / 60,
                        settings.CONFIG['edit_lock_expiration']]
            else:
                Issue.unlock(id)

        return [_issueIsNotLocked,
                settings.CONFIG['edit_lock_expiration']]
