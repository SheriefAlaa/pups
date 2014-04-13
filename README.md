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

How to install:
===============

* git clone https://github.com/SheriefAlaa/webchat.git
* python manage.py syncdb (Would you like to create one now? (yes/no): no)
* chown -R www-data:www-data databases/ 
* chmod -R 770 databases/
* python manage.py createuser USERNAME PASSWORD
 
* Add the following to your httpd/apache2.conf:
```
Alias /static/ /home/user/path/to/static/
 
<Directory /home/user/path/to/static>
  Order deny,allow
  Allow from all
</Directory>
 
WSGIScriptAlias / /path/to/wsgi.py
WSGIPythonPath /path/to/pups_project

<Directory /path/to/pups_project/pups>
<Files wsgi.py>
Order deny,allow
Allow from all
</Files>
</Directory>

```

* Visit localhost/login from your browser.

TODO:
=====
* Custom django-admin command to clean up expired dates via a cron job.
* CSS, UI and branding.
* Add an is_present() method to check if a support assistant's presence.
* webchat.torproject.org should give the user an explanation on what is  going on and how to request a chat token in all help desk languages.

Possible extensions:
===============
* Resize the chat window on visiting the link?
* Give the support assistant the ability to send a notification email (eg: I am available for chatting for the next X hours).
* Localization.
* ..