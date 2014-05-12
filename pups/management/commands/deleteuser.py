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

import sys
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = 'Deletes a support assistant account'

    def handle(self, *args, **options):
        if len(args) != 1:
            print "Usage: python manage.py deleteuser user_to_be_deleted"
            sys.exit(0)

        try:
            user = User.objects.get(username=args[0])
            user.delete()
            print "Deleted: %s" % args[0]
            sys.exit(1)
        except ObjectDoesNotExist:
            print '"%s" does not exist in the database.' % (args[0])
            sys.exit(-1)
