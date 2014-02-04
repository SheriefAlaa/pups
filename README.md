webchat
=======

Basically this is just Prodromus inside a Django project.

Components needed:
==================
-Any version of Apache
-Python 2.5 or above
-python-django (1.4+)
-libapache2-mod-wsgi

How to install
==============

1) Clone.
 
2) Add these lines to httpd/apache2.conf:
=========================================
Alias /static/ /home/USER/webchat/static/
 
<Directory /home/USER/webchat/static>
  Order deny,allow
  Allow from all
</Directory>
 
WSGIScriptAlias / /home/USER/webchat/webchat/wsgi.py
WSGIPythonPath /home/USER/webchat
<Directory /home/USER/webchat/webchat>
 <Files wsgi.py>
   Order allow,deny
   Allow from all
 </Files>
</Directory>

3) Visit localhost/webchat from your browser.
 
Note:
=====
1) webchat/webchat/settings.py line 26 (ALLOWED_HOSTS = ['*']) should be
(ALLOWED_HOSTS = ['www.domainname.org'])
2) On each change in any file apachectl restart is needed (needs virtualenv and mod_wsgi as a daemon).
