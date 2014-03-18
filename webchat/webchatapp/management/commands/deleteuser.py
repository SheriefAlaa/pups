from django.core.management.base import BaseCommand, CommandError
import sys
from django.contrib.auth.models import User
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Deletes a support assistant account'

    def handle(self, *args, **options):
        if len(args) != 1:
            print "Usage: python manage.py deleteuser user_to_be_deleted"
            sys.exit(0)

        try:
            user = User.objects.get(username = args[0])
            user.save()
            print "Deleted: %s" % args[0]
        except IntegrityError:
            print '"%s" already exists, if you want to delete it use: $ manage.py deleteuser %s' % (args[0], args[0])