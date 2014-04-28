Overview:
=========

pups_project contains small projects that helps the support teams.

* pups: The main Django app that handles login/logout/registration
* webchat: Extends Prodromus (An XMPP javascript client) to support invitation based chat tokens.
* stats: A CRUD tool that stores some text that can be edited by multiple users at same time.

Components needed:
==================
* Any version of Apache
* Python 2.5 or above
* python-django (1.4.5)
* libapache2-mod-wsgi
* mod_auto_accept_subscriptions (https://code.google.com/p/prosody-modules/wiki/mod_auto_accept_subscriptions)

How to install:
===============

* git clone https://github.com/SheriefAlaa/projectpups.git
* python manage.py syncdb (Would you like to create one now? (yes/no): no)
* chown -R www-data:www-data databases/ 
* chmod -R 770 databases/
* python manage.py createuser USERNAME PASSWORD
* vim projectpups/pups/settings.py and fill in the CONFIG dict (See settings.py.sample)
 
* Add the following to your httpd/apache2.conf:
```
# This apache configuration is for a single production instance

WSGIPythonPath /path/to/projectpups

WSGIScriptAlias / /path/to/wsgi.py

<Directory /path/to/projectpups/pups>
<Files wsgi.py>
Order deny,allow
Allow from all
</Files>
</Directory>

# Serves static files
Alias /static/ /home/user/path/to/static/
 
<Directory /home/user/path/to/static>
  Order deny,allow
  Allow from all
</Directory>

```

* Visit localhost/login from your browser.

Possible extensions:
===============
* Resize the chat window on visiting the link?
* Give the support assistant the ability to send a notification email (eg: I am available for chatting for the next X hours).
* Localization.

License:
========
Do whatever you want with this application, just point to the original git repo.

Contact:
========
sheriefalaa dot w [at] gmail dot com