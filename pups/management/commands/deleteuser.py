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
