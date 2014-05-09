import sys
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Creates a support assistant account'

    def handle(self, *args, **options):
        if len(args) != 2:
            print "Usage: python manage.py createuser username password"
            sys.exit(0)

        try:
            user = User.objects.create_user(username=args[0], password=args[1])
            user.save()
            print "Created: %s" % args[0]
            sys.exit(1)
        except IntegrityError:
            print '"%s" already exists, if you want to delete it use:\
             $ manage.py deleteuser %s' % (args[0], args[0])
            sys.exit(-1)
