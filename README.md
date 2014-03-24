Webchat
=======

Basically this Prodromus (An XMPP javascript client) wrapped in a Django project.
The goal here is to extend Prodromus to support invitation based chat tokens.

Components needed:
==================
* Any version of Apache
* Python 2.5 or above
* python-django (1.4+)
* libapache2-mod-wsgi

How to install:
===============

* git clone https://github.com/SheriefAlaa/webchat.git
* cd webchat/webchat && mkdir webchatDB
* python manage.py syncdb (Would you like to create one now? (yes/no): no)
* chown -R www-data:www-data webchatDB/ 
* chmod -R 770 webchatDB/
* python manage.py createuser username password
 
* Add the following to your httpd/apache2.conf:
```
Alias /static/ /home/user/webchat/webchat/static/
 
<Directory /home/user/webchat/webchat/static>
  Order deny,allow
  Allow from all
</Directory>
 
WSGIScriptAlias / /home/user/webchat/webchat/webchatapp/wsgi.py
WSGIPythonPath /home/user/webchat/webchat/
<Directory /home/user/webchat/webchatapp>
 <Files wsgi.py>
   Order allow,deny
   Allow from all
 </Files>
</Directory>
```

* Visit localhost/login from your browser.
