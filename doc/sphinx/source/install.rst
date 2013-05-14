Installation Instructions for Ubuntu
====================================

Defaults
--------

This document sets up the Indivo backend server and Indivo UI server on the same machine. The backend server runs on port 8000, the UI server on port 80 by default. This is configurable by changing the appropriate port numbers in the instructions below.

Pre-Requisites
--------------

This documents the installation of a complete Indivo X server and user interface. For concreteness, we show all of the exact instructions needed when installing on Ubuntu Linux 11.04 (Natty) or 11.10 (Oneiric). We welcome variants of these explicit instructions from folks installing on other operating systems, we will be happy to post them alongside these instructions.

*Note*: We recommend you do this by sudo'ing from a non-root user.  If you would like to do this as root make sure you create at least one non-root user with::

	useradd -m {USER}
	
otherwise the default locale will not be set.  This issue is most common on a new OS build.

You will need the following for Indivo:

* Recent Linux installation (Kernel 2.6+)

* Python 2.6+ (**NOT 2.5 or below**) with package ``lxml``::

	apt-get install python-lxml

* Django 1.2 or 1.3 (**1.1 is NO LONGER SUPPORTED**)

  From source::
	
		wget http://www.djangoproject.com/download/1.3.1/tarball/
		tar xzvf Django-1.3.1.tar.gz
		cd Django-1.3.1
		sudo python setup.py install
		cd ..
		rm -rf Django-1.3.1 Django-1.3.1.tar.gz

  Using a package manager (**Ubuntu 10.10 or later**)::

		apt-get install python-django

* Apache 2 (for production) with module ``mod_wsgi`` (``mod_ssl`` for HTTPS is strongly recommended for production, but we won't cover its installation here.)::

	apt-get install apache2-mpm-prefork 

  *NOTE*: For Lucid, you may need to do an apt-get update before making the following command::

	apt-get install libapache2-mod-wsgi

* easy_install for Python::
 
	apt-get install python-setuptools

* the Django South DB migration library::

	easy_install South 

* Python Markdown support::

	easy_install Markdown

* RDF support::

	easy_install rdflib

Database Install
----------------

Postgres
^^^^^^^^

Install
"""""""

* PostgreSQL 8.3+ (8.4 recommended and the default on Ubuntu 10.10)::

	apt-get install postgresql

* The psycopg python binding for postgres.
  
  For Ubuntu 11.04 and below, simply install with::

	apt-get install python-psycopg2

  Recent versions of psycopg2 (2.4.2+) are incompatible with Django. If your 
  default version is 2.4.2 or greater (true as of Ubuntu 11.10), install version 
  2.4.1 instead, from http://initd.org/psycopg/tarballs/PSYCOPG-2-4/psycopg2-2.4.1.tar.gz 
  (instructions for installation may be found at http://initd.org/psycopg/install/ ). 
  If you've already installed a newer version of psycopg2, you can downgrade with::

		pip install psycopg2==2.4.1


Setup
"""""

*Note*: You'll have the easiest time naming your database ``indivo``

There are two ways to authenticate to PostgreSQL: use your Unix credentials, or use a separate username and password. 
We strongly recommend the latter, and our instructions are tailored appropriately. If you know how to use PostgreSQL 
and want to use Unix-logins, go for it, just remember that when you use Apache, it will usually try to log in using its 
username, ``www-data``.

in ``/etc/postgresql/8.4/main/pg_hba.conf``, find the line that reads::

	local     all     all        ident

This should be the second uncommented line in your default config. Change it to::

	local     all     all        md5

You will need to restart PostgreSQL::

	service postgresql-8.4 restart

or, on postgres  9+::

	service postgresql restart

Create a PostgreSQL user for your Indivo service, e.g. "indivo" and setup a password::

	su - postgres
	createuser --superuser indivo
	psql
	postgres=# \password indivo
	postgres=# \q
	logout

Create the Database and make the Indivo user its owner::

	createdb -U indivo -O indivo indivo

More Information
""""""""""""""""

See the `Django PostgreSQL notes <https://docs.djangoproject.com/en/1.3/ref/databases/#postgresql-notes>`_

MySQL
^^^^^

Install
"""""""

* The Mysql server (*only tested with v5.0+*)::
	
	sudo apt-get install mysql-server
	
  When prompted, enter a password for the root user.

* The MySQLdb python binding (*v1.2.1p2 or greater required for django*)::

	sudo apt-get install python-mysqldb

Setup
"""""

* Change the default storage engine to InnoDB, which supports transactions. In ``/etc/mysql/my.cnf``, find the line reading ``[mysqld]``. Directly underneath that line, add::

	default-storage-engine = innodb
	default-character-set = utf8

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

See the `Django MySQL notes <https://docs.djangoproject.com/en/1.3/ref/databases/#mysql-notes>`_

Oracle
^^^^^^

Install
"""""""

If you do not have a supported installation of Oracle already, the odds are good that you shouldn't be running Indivo on Oracle. Also, Oracle doesn't play nicely with Debian Linux, so you also probably shouldn't be setting it up on Ubuntu. These installation instructions assume that you have a running instance of Oracle on another machine, and describe how to connect to it from an Indivo instance running on Ubuntu.

You'll need an installation of Oracle against which to bind the Python drivers. You can use Oracle XE (express edition), which is free and based on Oracle 11i. We used the `following installation instructions <http://www.cyberciti.biz/faq/howto-install-linux-oracle-database-xe-server/>`_. **NOTE**: These instructions only work for 32-bit Linux. For 64-bit versions, Oracle doesn't offer a solution.

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

See the `Django Oracle notes <https://docs.djangoproject.com/en/1.3/ref/databases/#oracle-notes>`_

Indivo Server
-------------

Get the Code
^^^^^^^^^^^^

From A Packaged Release
"""""""""""""""""""""""

* Download the latest release of Indivo X and untar into ``indivo_server/``. Do not change this directory name--it will break the django settings file.

From Github
"""""""""""

* From the commandline, run::

	cd /desired/install/directory
	git clone --recursive git://github.com/chb/indivo_server.git

* If you want to run the bleeding edge version of Indivo, you're done. If you want to use an official release, you can list releases with::

	git tag -n1
	
  and checkout your desired release and update its submodules with::
  
	git checkout {TAGNAME}
	git submodule update
	
where tagname might be (i.e., for version 2.0) ``v2.0.0``.

Configuration
^^^^^^^^^^^^^

Copy ``settings.py.default`` to ``settings.py``, and open it up. Make sure to look at the 'Required Setup' settings, and examine 'Advanced Setup' if you are interested. As an absolute minimum, update the following:

* set ``SECRET_KEY`` to a unique value, and don't share it with anybody
* set ``APP_HOME`` to the complete path to the location where you've installed ``indivo_server``, e.g. ``/web/indivo_server``
* set ``SITE_URL_PREFIX`` to the URL where your server is running, including port number e.g. ``https://pchr.acme.com:8443``
* Database Settings: Edit the 'default' database under ``DATABASES``, and:

  * set ``ENGINE`` to the database backend you are using, prefixed by 'django.db.backends.'. Available options are 'postgresql_psycopg2', 'mysql', and 'oracle'.
  * set ``NAME`` to the name you would like to use for your database. If you followed the database setup instructions above, you should leave this as 'indivo'.
  * set ``USER`` to the username you chose, in this documentation ``indivo``, and set ``PASSWORD`` accordingly.
  * If your database is located on another machine, set ``HOST`` and ``PORT`` appropriately.
  * If you are running Oracle, see https://docs.djangoproject.com/en/1.2/ref/databases/#id11 for how to configure the database settings.
  
* set the ``SEND_MAIL`` parameter to True or False depending on whether you want emails actually being sent.
* set the ``EMAIL_*`` parameters appropriately for sending out emails.
* Under ``utils/`` copy ``indivo_data.xml.default`` to ``indivo_data.xml`` and edit accordingly.  **Note**: Make sure to do this step before 
  resetting the database, as the credentials for users/apps in ``indivo_data.xml`` cannot be changed without an additional reset of the database.

Resetting the Database
^^^^^^^^^^^^^^^^^^^^^^

* On postgres or mysql from your base install directory::

	python utils/reset.py 

* On other database backends, we don't yet have reset scripts. You can reset Indivo by:

  * Flushing the database:: 

		python manage.py flush
  	
  * Telling South that the database is actually in the correct state after migration::

		python manage.py migrate --fake
		
  * Importing the initial Indivo data::

		python utils/importer.py -v
		
  * Loading Coding Systems (optional)::

		python load_codingsystems.py

You must run ``reset.py`` or ``utils/importer.py`` before the accounts and applications you set up in indivo_data.xml exist.

.. _coding-systems-install:

Coding Systems
^^^^^^^^^^^^^^

TODO
Indivo uses SNOMED CT for problem coding, HL7v3 for immunization coding, and LOINC for lab coding. Medication coding will likely use RxNorm. In most cases, the license on these coding systems does **not** allow us to redistribute these codes with Indivo. We don't like this. We wish we had truly free coding systems for health. We've told the folks at the National Library of Medicine as much. But there's not much we can do about this for now.

What we've done is make it easy for you to load coding systems into Indivo if you can get them independently. Get the HL7 v3 codes from hl7.org, get the SNOMED CT dataset from UMLS. You should see "|"-separated files. Examples of how these files are formatted can be found in ``codingsystems/data/sample``. Once you've downloaded these files independently from the coding system agencies, copy them to:

* ``codingsystems/data/complete/SNOMEDCT_CORE_SUBSET_200911_utf8.txt``
* ``codingsystems/data/complete/HL7_V3_VACCINES.txt``
* ``codingsystems/data/complete/LOINCDB.txt``

Once that's done, assuming you've installed everything in ``/web/indivo_server``, you can run::

	utils/reset.sh.py -c

and have everything loaded properly.

See more info on codingsystems and where to find the data files [TODO](www.junk.com).

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

* Download the latest release of Indivo X UI Server (see [TODO](www.junk.com)) and untar into ``indivo_ui_server/``. Do not change this directory name--it will break the django settings file.

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

* Check your ``/etc/apache2/sites-enabled/000-default`` file again and make sure that your ``Alias /static/ `` lines match the above example exactly

* Restart Apache::

		service apache2 restart

What Next?
----------

You should be able to log in and add the default apps. These apps are **purposely** limited in functionality. May the best apps win.
