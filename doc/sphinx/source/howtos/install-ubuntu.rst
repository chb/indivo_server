Installation Instructions for Ubuntu 12.04
==========================================

Defaults
--------

This document sets up the Indivo backend server and Indivo UI server on the same machine. The backend server runs on port 8000, the UI server on port 80 by default. This is configurable by changing the appropriate port numbers in the instructions below.  For databases, the instructions below assume ``indivo`` for the user and database name

Pre-Requisites
--------------

This documents the installation of a complete Indivo X server and user interface. For concreteness, we show all of the exact instructions needed when installing on Ubuntu Linux 12.04.  We welcome variants of these explicit instructions from folks installing on other operating systems, and are happy to post them alongside these instructions.

.. note::

	We recommend you do this by sudo'ing from a non-root user.  If you would like to do this as root make sure you create at least one non-root user with::

		useradd -m {USER}
	
	otherwise the default locale will not be set.  This issue is most common on a new OS build.

Install the following system packages::

	apt-get install libxslt-dev libxml2-dev python-dev git


Database Install
----------------

Postgres
^^^^^^^^

Install
"""""""

Install the PostgreSQL meta package (currently PostgreSQL 9.1 on 12.04) and header files for libpq5::

    apt-get install postgresql libpq-dev


Setup
"""""

.. note:: 

	the instructions below assume you have named your database ``indivo`` and will create a database user named ``indivo``

Create a PostgreSQL user for your Indivo service, e.g. "indivo" and setup a password::

	su postgres
	createuser --superuser indivo
	psql
	postgres=# \password indivo
	postgres=# \q

Create the Database and make the Indivo user its owner::

	createdb -U indivo -O indivo indivo

There are two ways to authenticate to PostgreSQL: use your Unix credentials, or use a separate username and password. 
We strongly recommend the latter, and our instructions are tailored appropriately. If you know how to use PostgreSQL 
and want to use Unix-logins, go for it, just remember that when you use Apache, it will usually try to log in using its 
username, ``www-data``.

in ``/etc/postgresql/9.1/main/pg_hba.conf``, find the line that reads::

	local     all     all        peer

This should be the second uncommented line in your default config. Alter it to be::

	local     all     all        md5

You will need to restart PostgreSQL::

	service postgresql restart



More Information
""""""""""""""""

See the `Django PostgreSQL notes <https://docs.djangoproject.com/en/1.4/ref/databases/#postgresql-notes>`_

MySQL
^^^^^

Install
"""""""

* The Mysql server (*only tested with v5.0+*)::
	
	sudo apt-get install mysql-server libmysqlclient-dev
	
  When prompted, enter a password for the root user.

* The MySQLdb python binding (*v1.2.1p2 or greater required for django*)::

	sudo apt-get install python-mysqldb

Setup
"""""

* Change the default storage engine to InnoDB, which supports transactions. In ``/etc/mysql/my.cnf``, find the line reading ``[mysqld]``. Directly underneath that line, add::

	default-storage-engine = innodb
	character-set-server = utf8

  Then restart mysql with::

	sudo service mysql restart

* Create the Indivo User by logging in (using the password you set up for the root user during install)::
	
	mysql -uroot -p
	
  And then running the following commands::

	> CREATE USER 'indivo'@'%' IDENTIFIED BY 'YOURPASSWORD'; # Replace YOURPASSWORD with a password for the new user
	> GRANT ALL PRIVILEGES ON *.* TO 'indivo'@'%' WITH GRANT OPTION;
	> exit

* Create the Indivo Database::
	
	mysqladmin -u indivo -p create indivo
	
  Authenticating with the password you set up for the indivo user.

Idiosyncracies
""""""""""""""

Date formatting doesn't work quite the same as it does on the other backends. Specifically:

* "Week of the Year" (00-53), which normally counts weeks as increments of 7 days starting at Jan 01, in mysql counts week 0 as anything before the first Sunday of the year, and after that counts weeks in increments of 7 days, starting on Sunday.
* "Day of the Week", which is normally indexed from 1 to 7, starting on Sunday, on mysql is indexed from 0 to 6, starting on Sunday.

More Information
""""""""""""""""

See the `Django MySQL notes <https://docs.djangoproject.com/en/1.4/ref/databases/#mysql-notes>`_

Oracle
^^^^^^

Install
"""""""

If you do not have a supported installation of Oracle already, the odds are good that you shouldn't be running Indivo on Oracle. Also, Oracle doesn't play nicely with Debian Linux, so you also probably shouldn't be setting it up on Ubuntu. These installation instructions assume that you have a running instance of Oracle on another machine, and describe how to connect to it from an Indivo instance running on Ubuntu.

You'll need an installation of Oracle against which to bind the Python drivers. You can use Oracle XE (express edition), which is free and based on Oracle 11i. We used the `following installation instructions <http://www.cyberciti.biz/faq/howto-install-linux-oracle-database-xe-server/>`_. 

.. note::

	These instructions only work for 32-bit Linux. For 64-bit versions, Oracle doesn't offer a solution.

Get the Python Oracle driver, `cx_Oracle <http://cx-oracle.sourceforge.net/>`_, with installation instructions `explained here <http://catherinedevlin.blogspot.com/2008/06/cxoracle-and-oracle-xe-on-ubuntu.html>`_.

Setup
"""""
Set up your Oracle user on the remote system. From the Django docs, you'll need to insure that you have access to your Oracle instance as a user with the following privileges:

* CREATE TABLE
* CREATE SEQUENCE
* CREATE PROCEDURE
* CREATE TRIGGER

To run Indivo's test suite, the user needs these additional privileges:

* CREATE USER
* DROP USER
* CREATE TABLESPACE
* DROP TABLESPACE
* CONNECT WITH ADMIN OPTION
* RESOURCE WITH ADMIN OPTION

Make sure your environment variables are set properly as described in the install instructions for cx_Oracle. Importantly:

* set ``ORACLE_HOME`` to the home directory for oracle, ``/usr/lib/oracle/xe/app/oracle/product/10.2.0/server/`` by default
* set ``LD_LIBRARY_PATH`` to ``$ORACLE_HOME/lib``
* add ``$ORACLE_HOME/bin`` to your ``$PATH`` variable.

If you intend on running Indivo on Apache, the Apache user will also need access to these environment variables. You can set this up by editing ``/etc/apache2/envvars`` and adding the above variable declarations.

Test that cx_Oracle has been installed. If the following command exits silently, your setup is correct::

	python -c "import cx_Oracle"

More Information
"""""""""""""""" 

See the `Django Oracle notes <https://docs.djangoproject.com/en/1.4/ref/databases/#oracle-notes>`_

Indivo Server
-------------

Get the Code
^^^^^^^^^^^^

From A Packaged Release
"""""""""""""""""""""""

* Download the latest release of Indivo X from our `tags page <https://github.com/chb/indivo_server/tags>`__ and untar into ``indivo_server/``. Do not change this directory name--it will break the django settings file.

From Github
"""""""""""

* From the commandline, run::

	cd /desired/install/directory
	git clone --recursive git://github.com/chb/indivo_server.git

* If you want to run the stable version of Indivo, you're done. If you want to use a tagged release, you can list them with::

	git tag -n1
	
  and checkout your desired release and update its submodules with::
  
	git checkout {TAGNAME}
	git submodule init
	git submodule update
	
where tagname might be (i.e., for version 2.0) ``v2.0.0``.

Configuration
^^^^^^^^^^^^^

Copy ``indivo/settings.py.default`` to ``indivo/settings.py``, and open it up. Make sure to look at the 'Required Setup' settings, and examine 'Advanced Setup' if you are interested. As an absolute minimum, update the following:

* set ``SECRET_KEY`` to a unique value, and don't share it with anybody
* set ``SITE_URL_PREFIX`` to the URL where your server is running, including port number e.g. ``https://pchr.acme.com:8443``
* Edit the 'default' database under ``DATABASES``, and:

  * set ``ENGINE`` to the database backend you are using, prefixed by 'django.db.backends.'. Supported options are 'postgresql_psycopg2', 'mysql', and 'oracle'.
  * set ``NAME`` to the name you would like to use for your database. If you followed the database setup instructions above, you should leave this as 'indivo'.
  * set ``USER`` to the username you chose, in this documentation ``indivo``, and set ``PASSWORD`` accordingly.
  * If your database is located on another machine, set ``HOST`` and ``PORT`` appropriately.
  * If you are running Oracle, see https://docs.djangoproject.com/en/1.4/ref/databases/#id11 for how to configure the database settings.

* If you are running MySQL, add the line ``SOUTH_TESTS_MIGRATE = False`` to your settings file
* set the ``SEND_MAIL`` parameter to True or False depending on whether you want emails actually being sent.
* set the ``EMAIL_*`` parameters appropriately for sending out emails.
* Under ``utils/`` copy ``indivo_data.xml.default`` to ``indivo_data.xml`` and edit to configure initial accounts, records, and sample data profiles.

  .. note::
  
	  Make sure to complete these steps before running the reset script below

Install Required Packages
^^^^^^^^^^^^^^^^^^^^^^^^^

We provide a pip requirements file for Indivo, so you just need to make sure you have pip installed on your system.  The easiest way to get pip in Ubuntu 12.04 is to run::

    apt-get install python-pip

If you want to read more about other installation methods, please visit http://www.pip-installer.org/en/latest/installing.html

Depending on your database of choice, you will want to edit ``requirements.txt`` and make sure you comment out or uncomment the libraries you need.  Once you have done this and have pip installed, run::

    pip install -r requirements.txt

Resetting the Database
^^^^^^^^^^^^^^^^^^^^^^

PostgreSQL
""""""""""
From your base install directory::

	python utils/reset.py 

MySQL
"""""

Currently some migrations on our development branch create rows that are too wide for MySQL when using UTF-8, so until we merge these appropriately you will have to perform a few extra steps

* turn off South migrations in your `settings.py` by commenting it out from your `INSTALLED_APPS`
* run::

    python manage.py syncdb

* turn South migrations back on
* run::

    python manage.py syncdb
    python manage.py migrate --fake indivo
    python utils/reset.py --no-syncdb


Other
"""""

* On other database backends, we don't yet have reset scripts. You can reset Indivo by:

  * Flushing the database:: 

		python manage.py flush
  	
  * Telling South that the database is actually in the correct state after migration::

		python manage.py migrate --fake
		
  * Importing the initial Indivo data::

		python utils/importer.py -v
		
  * Loading Coding Systems (optional)::

		python load_codingsystems.py

You must run ``reset.py`` or ``utils/importer.py`` before the accounts and records you set up in indivo_data.xml exist.


Database Cleanup
^^^^^^^^^^^^^^^^
Each request made against Indivo Server generates some oauth-related data that is stored in the database for security reasons (for example, session tokens are stored whenever a user logs in, and oAuth Nonces are stored for every request). This data is only relevant for a certain duration (i.e., the length of a web session), after which point it becomes needless clutter in the database. In order to remove all such clutter, from ``APP_HOME`` run::

	python manage.py cleanup_old_tokens

This command should be set up to run as a cron job, and should be run regularly to make sure the size of the database doesn't get out of control (we recommend at least once a week, and more frequently for high traffic installations).

Testing Indivo Backend Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Indivo uses the django-tests framework to provide some basic unit and API testing. If you want to make sure everything is setup properly before opening the server up to the network, running these tests is a good start. Django tests set up a clean test database for each run of the tests, so don't worry about your installation being corrupted. To run the Indivo tests, in ``APP_HOME`` run::

	python manage.py test indivo

Indivo UI Server
----------------

Get the Code
^^^^^^^^^^^^

From a Packaged Release
"""""""""""""""""""""""

* Download the latest release of Indivo X UI Server from our `tags page <https://github.com/chb/indivo_ui_server/tags>`__ and untar into ``indivo_ui_server/``. 
  
  .. note::
  
  	Do not change this directory name--it will break the django settings file.

From Github
"""""""""""

* From the commandline, run::

	cd /desired/install/directory
	git clone --recursive git://github.com/chb/indivo_ui_server.git

* If you want to run the bleeding edge version of Indivo, you're done. If you want to use an official release, you can list releases with::

	git tag -n1

  and checkout your desired release and update its submodules with::
  
	git checkout {TAGNAME}
	git submodule update
		
  where tagname might be (i.e., for Version 2.0) ``v2.0.0``

Configuration
^^^^^^^^^^^^^

* Copy ``settings.py.default`` to ``settings.py``, and update a few key parameters:

  * set ``SERVER_ROOT_DIR`` to the complete filesystem path to the location where you've installed ``indivo_ui_server``, e.g. ``/web/indivo_ui_server``, with no trailing slash.
  * set ``INDIVO_UI_SERVER_BASE`` to the URL at which your UI server will be accessible, e.g. ``http://localhost``, with no trailing slash.
  * set ``INDIVO_SERVER_LOCATION``, ``CONSUMER_KEY``, ``CONSUMER_SECRET`` appropriately to match the Indivo Server's location and chrome credentials (check ``indivo_server/utils/indivo_data.xml`` BEFORE you reset the database on the indivo_server end).
  * set ``SECRET_KEY`` to a unique value, and don't share it with anybody

Running Indivo
--------------

Django Development Servers
^^^^^^^^^^^^^^^^^^^^^^^^^^

The Django development servers are easy to run at the prompt.  The backend server can run on localhost in the configuration given above::

	cd /web/indivo_server/
	python manage.py runserver 8000

The UI server, if you want it accessible from another machine, needs to specify a hostname or IP address. If you want port 80, you need to be root of course::

	cd /web/indivo_ui_server/
	python manage.py runserver HOSTNAME:80

**IMPORTANTLY**, if you've installed Apache, you'll need to turn it off to run your UI server from the prompt::

	/etc/init.d/apache2 stop

Apache
^^^^^^

Assuming you installed Indivo Server and UI in ``/web``, the steps to getting Apache2 serving Indivo and its UI are:

* in ``/etc/apache2/sites-available/default``, add::

	<VirtualHost *:8000>
		ServerAdmin YOU@localhost
		ServerName localhost
		DocumentRoot /web/indivo_server
		Alias /static/ /web/indivo_server/static/
		EnableMMAP On
		EnableSendfile On
		LogLevel warn

		<Directory /web/indivo_server>
			Order deny,allow
			Allow from all
		</Directory>

		WSGIApplicationGroup %{GLOBAL}
		WSGIScriptAlias / /web/indivo_server/django.wsgi
		WSGIPassAuthorization On
	</VirtualHost>
	
	<VirtualHost *:80>
		ServerAdmin YOU@localhost
		ServerName localhost
		DocumentRoot /web/indivo_ui_server
		Alias /static/ /web/indivo_ui_server/ui/static/
		EnableMMAP On
		EnableSendfile On
		LogLevel warn

		<Directory /web/indivo_ui_server>
		 Order deny,allow
		 Allow from all
		</Directory>

		WSGIDaemonProcess indivo_ui user=www-data group=www-data processes=1 maximum-requests=500 threads=10
		WSGIScriptAlias / /web/indivo_ui_server/django.wsgi
		WSGIPassAuthorization On
	</VirtualHost>

  In our experience, using ``WSGIProcessGroup`` directive with a specific group (not global), even when it matches the ``WSGIDaemonProcess`` group name (i.e. indivo_ui), can cause a permission issue with reading the Unix socket. We will continue to investigate this issue. However, due to incompatibilities between the lxml package and mod_wsgi, it is necessary to set Indivo Server to the global ``WSGIProcessGroup`` instead of running daemons.

* Make sure ports.conf has::

		NameVirtualHost *:80
		Listen 80
		Listen 8000

* Make sure that www-data (or whoever is in ``/etc/apache2/envvars``) has access to ``indivo_server`` and ``indivo_ui_server`` AND can write to ``indivo_server/indivo.log`` and ``indivo_ui_server/sessions/*``, including the ``sessions/`` directory itself.

* Since you probably did a ``python manage.py syncdb``, you almost certainly want to just remove the current ``indivo.log`` before you move ahead.

* *Really*, have you checked this www-data permission issue? This will be the cause of all your problems if you don't check this carefully.

* Check your ``/etc/apache2/sites-enabled/000-default`` file again and make sure that your ``Alias /static/`` lines match the above example exactly

* Restart Apache::

		service apache2 restart

What Next?
----------

You should be able to log in and add the default apps. These apps are **purposely** limited in functionality. May the best apps win.
