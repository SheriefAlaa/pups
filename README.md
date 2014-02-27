webchat
=======

Basically this is just Prodromus inside a Django project.

components needed:
==================
Any version of Apache, Python 2.5 or above, python-django (1.4+), virtualenv and libapache2-mod-wsgi

how to install:
===============

1) Run: $ virtualenv ENV

1) Clone the repo somewhere locally.
 
2) Add the following to your httpd/apache2.conf:
```
WSGIDaemonProcess example.com python-path=/home/USER/webchat:/ENV/lib/python2.7/site-packages
WSGIProcessGroup example.com
 
Alias /static/ /home/USER/webchat/static/
 
<Directory /home/USER/webchat/static>
Order deny,allow
Allow from all
</Directory>
WSGIScriptAlias / /home/USER/webchat/webchat/wsgi.py
<Directory /home/USER/webchat/webchat>
 <Files wsgi.py>
   Order allow,deny
   Allow from all
 </Files>
</Directory>
```

3) Visit localhost/webchat from your browser.
 
note:
=====
1) webchat/webchat/settings.py line 26 (ALLOWED_HOSTS = ['*']) should be
(ALLOWED_HOSTS = ['www.domainname.org'])

2) On each change python files like view.py or urls.py you will need to restart apache.
(this doesn't apply to templates and static files.)
