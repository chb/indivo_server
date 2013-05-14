Installation Instructions for RHEL 5
====================================

Contributed by Timothy Kutz and Matthew Ellison.

Pre-req Installs
----------------

* RHEL 5.6
* Oracle 10g Client – installed to /data2/app/oracle
* Python 2.6.4 – installed to /usr/bin/python2.6 with libs at /usr/lib/python2.6
* Django 1.2.5 – installed to python2.6 location
* cx_Oracle-5.0.4-10g-py26-1.x86_c6.rpm
* Apache 2.2.18 – installed to /data2/app/apache22
* Mod_wsgi 3.3 for Python 2.6.4 – installed to apache modules

Install Indivo
--------------

* Indivo_server codebase – installed to /data2/app/apphome/indivo: Ensure this location is readable by the user Apache will run under (usually daemon)
* Using Virtualenv tool (http://www.virtualenv.org/en/latest/index.html), create python26 environment in /data2/app/python/python26::

    $ Python virtualenv.py /data2/app/python/python26

* Ensure the links created here point correctly to the python 2.6 locations.  If it points to 2.4, something is wrong, possibly the version of python invoked by the user running the tool.
* Ensure this environment is permissioned 755 (public readable/executable).

Apache Config
-------------

* Add to ``$APACHE_HOME/bin/envvars``::

    ORACLE_HOME="/data2/app/oracle"
    export ORACLE_HOME

    LD_LIBRARY_PATH="/data2/app/apache22/lib:$ORACLE_HOME/lib:$LD_LIBRARY_PATH"
    export LD_LIBRARY_PATH

    PATH="$ORACLE_HOME/bin:$PATH"
    export PATH

* Add to ``$APACHE_HOME/conf/httpd.conf``:

  (in modules section: )::

    LoadModule wsgi_module modules/mod_wsgi.so


  (at end of file: )::

      <IfModule wsgi_module>
          DocumentRoot /data2/app/apphome/indivo/indivo_server
          Alias /static/ /data2/app/apphome/indivo/indivo_server/static/
          EnableMMAP  On
          EnableSendfile On
          LogLevel  warn

         <Directory /data2/app/apphome/indivo/indivo_server>
            Order deny,allow
            Allow from all
         </Directory>
         WSGIPythonHome /data2/app/python/python-26/
         WSGIApplicationGroup %{GLOBAL}
         WSGIScriptAlias / /data2/app/apphome/indivo/indivo_server/django.wsgi
         WSGIPassAuthorization On
      </IfModule>


Django/Indivo Config
--------------------

* Modify settings.py (Only modified lines shown, in order)::

    # base URL for the app
    APP_HOME = '/data2/app/apphome/indivo/indivo_server'
    # URL prefix
    SITE_URL_PREFIX = "http://ndvodmo.tch.harvard.edu"
    …
    #Oracle DB settings
    #NOTE: DATABASE_NAME must be under 255 chars, so all whitespace has been removed below.
    DATABASE_ENGINE = 'django.db.backends.oracle'
    DATABASE_NAME = '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=HOST1)(PORT=1550))(ADDRESS=(PROTOCOL=TCP)(HOST=HOST2)(PORT=1550))(LOAD_BALANCE=yes)(CONNECT_DATA=(SERVER=DEDICATED(
    SERVICE_NAME=CHRACTST)(FAILOVER_MODE=(TYPE=SELECT)(METHOD=BASIC)(RETRIES=180)(DELAY=5))))'
    DATABASE_USER = 'USERNAME'
    DATABASE_PASSWORD = 'PASS'
    DATABASE_HOST = ''
    DATABASE_PORT = ''

    # logging
    #import logging
    #logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s %(levelname)s%(message)s',
    #           filename = '/data2/app/indivo/logs/indivo.log', filemode = 'w'
    #           )

Set Up Oracle Instance
----------------------

* The Oracle instance(s) serving Indivo must match the connection string in ``settings.py`` under ``DATABASE_NAME``. This will involve setting up a tablespace for Indivo (in the above example ``CHRACTST``), and user access.
