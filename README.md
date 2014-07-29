Overview:
=========

Pups is a Django/Python Project that contains small apps that helps the support teams.

* pups: The main Django app that handles login/logout/registration
* webchat: Extends Prodromus (An XMPP javascript client) to support invitation based chat tokens.
* stats: A CRUD tool that stores some text that can be edited by multiple users at same time.

Requirements:
==================
* Any version of Apache
* Python 2.5 or above
* python-django (1.4.5)
* libapache2-mod-wsgi
* mod_auto_accept_subscriptions (https://code.google.com/p/prosody-modules/wiki/mod_auto_accept_subscriptions)
* python-django-south (https://packages.debian.org/wheezy/python-django-south)

Installation:
===============

* git clone https://github.com/SheriefAlaa/projectpups.git
* cp projectpups/pups/settings.py.sample projectpups/pups/settings.py
* python manage.py syncdb (Would you like to create one now? (yes/no): no)
* chown -R www-data:www-data databases/ 
* chmod -R 770 databases/
* python manage.py createuser USERNAME PASSWORD
* vim projectpups/pups/settings.py and fill in the CONFIG dict (See settings.py.sample)

Single pups instance:
=====================

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
Alias /static/ /path/to/static/
 
<Directory /path/to/static>
  Order deny,allow
  Allow from all
</Directory>
```

* Visit localhost/login from your browser.

Running multipule instances:
============================

First method:
------------
Note: requires virtualenv and the installation of django using pip.

```
<VirtualHost *:80>
    ServerName pups.example.com

    WSGIDaemonProcess pups processes=5 python-path=/path/to/prod_env/pups:/path/to/prod_env/lib/python2.7/site-packages threads=1
    WSGIProcessGroup pups
    WSGIScriptAlias / /path/to/prod_env/pups/pups/wsgi.py

    Alias /static/ /path/to/prod_env/pups/static/ 

    <Directory /path/to/prod_env/pups/static> 
      Order deny,allow
      Allow from all
    </Directory>

</VirtualHost>

<VirtualHost *:80>
    ServerName pups-staging.example.com

    WSGIDaemonProcess pups-staging processes=5 python-path=/path/to/stag_env/pups:/path/to/stag_env/lib/python2.7/site-packages threads=1
    WSGIProcessGroup pups-staging
    WSGIScriptAlias / /path/to/stag_env/pups/pups/wsgi.py

    Alias /static/ /path/to/stag_env/pups/static/ 

    <Directory /path/to/stag_env/pups/static> 
      Order deny,allow
      Allow from all
    </Directory>
</VirtualHost>
```

Second method:
--------------
Note: requires mod_passenger
...

Adding DB columns:
==================
Sometimes after creating your schema you'd want to add a column 
or two but django 1.4.5 doesn't support that. Luckily there is 
a solution for this (python-django-south) and this is how to use it..

```
#app_name can be pups/webchat/stats

./manage.py schemamigration app_name --init

./manage.py migrate app_name --fake

# Now you can add db columns

./manage.py schemamigration app_name --auto

./manage.py migrate app_name
```

Possible extensions:
====================
* Resize the chat window on visiting the link.
* Give the support assistant the ability to send a notification email.
* When will the assistant be available count down timer.
* Localization.

Contact:
========
sheriefalaa dot w [at] gmail dot com