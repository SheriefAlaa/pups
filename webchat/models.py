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

import uuid
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F


class Token(models.Model):
    t_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User)
    token = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    comment = models.CharField(max_length=128)
    visits = models.IntegerField(default=0)

    def __unicode__(self):
        return u'ID: %s Owner: %s visits: %s' % (self.t_id, self.owner, self.visits)

    def create_token(self, owner_id, expiration_days, comment):
        q = Token(
            owner=User.objects.get(id=owner_id),
            token=uuid.uuid4().hex,
            expires_at=timezone.now() + timedelta(expiration_days),
            comment=comment
            )
        q.save()

        return q.t_id is not None

    def get_token(self, token):
        try:
            return Token.objects.get(token=token)
        except ObjectDoesNotExist:
            return []

    def revoke_tokens(self, token_list):
        '''
        Sets the expiration date equals to the creation date of a token or more
        '''

        for token in token_list:
            Token.objects.filter(token=token)\
                .update(expires_at=F('created_at'))
        return True

    def get_assistant_tokens(self, assistant):
        '''
        Returns a list of non-expired/revoked assistant's tokens
        '''
        return Token.objects.filter(owner=assistant).order_by('-t_id')\
            .filter(expires_at__gt=timezone.now())

    def increment_visits(self, id):
        token = Token.objects.filter(t_id=id)

        if not token:
            return False

        token.update(visits=F('visits')+1)
        return True
