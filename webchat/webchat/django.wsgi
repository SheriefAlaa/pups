import os
import sys
 
path='/home/sherief/wcDep/webchat'
 
if path not in sys.path:
	sys.path.append(path)
 
os.environ['DJANGO_SETTINGS_MODULE'] = '<my-project-name>.settings'
 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
