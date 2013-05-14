Installation Instructions for OSX Lion
======================================


Requirements Overview
---------------------
* OS X 10.7 & 10.8
* PostgreSQL 9.0.4
* Python 2.7.1
* Django 1.3.1
* lxml 2.3.4
* psycopg2 2.4.5
* git 1.7.4.4

*Optional*:

* Apache 2.2.18 (Unix)
* mod_wsgi 3.3


Prerequisites
-------------

Command Line Tools
^^^^^^^^^^^^^^^^^^

If you have **Xcode** installed, make sure the command line tools are also installed (in Xcode > Preferences > Downloads > Components > Command Line Tools). You can download Xcode for free from the `Mac App Store <http://itunes.apple.com/ch/app/xcode/id497799835?l=en&mt=12>`_, but it will cost you several GB of disk space. Alternatively, you can register a free developer account with Apple and download an `installer for just the command line tools <https://developer.apple.com/downloads/index.action>`_.

You should now have the compilers and git installed.

PostgreSQL
^^^^^^^^^^

It's easiest to use the `Mac installer <http://www.postgresql.org/download/macosx/>`_ because it also sets up the ``postgres`` user which is needed.

* Download the latest installer (I used 9.1.4) and run it. You can keep most default settings:
    * Install into ``/Library/PostgreSQL/9.1``
    * Port ``5432``
    * Remember your password!
    * Locale ``en_US.UTF-8`` (any ``.UTF-8`` will do)

* Your PostgreSQL Server should now be running. You can restart Postgres with::

    sudo launchctl stop com.edb.launchd.postgresql-9.1 (it will then automatically restart)


**Make PostgreSQL more secure; only needed when using Postgres < 9.1!**

* Login as postgres if you're not already::

    sudo su - postgres

  (We should now be in /Library/PostgreSQL/9.0)

* Make the changes to ``data/pg_hba.conf``: Close to the bottom of the file, change the lines that end with "ident" or "trust" into "md5", for example::

    local     all     all        ident

  to::

    local     all     all        md5

Python: lxml
^^^^^^^^^^^^

Instructions taken from: http://lxml.de/build.html#building-lxml-on-macos-x

* Download: http://pypi.python.org/pypi/lxml/2.3.4#downloads (download the source tarball, double click to unarchive)
* Build & Install::

    cd lxml-2.3.4
    python setup.py build --static-deps
    sudo python setup.py install

Python: psycopg2
^^^^^^^^^^^^^^^^

* Download: http://www.psycopg.org/psycopg/tarballs/PSYCOPG-2-4/psycopg2-2.4.5.tar.gz (download the source, double click to unarchive)
* Build & Install::

    cd psycopg2-2.4.5
    python setup.py build
    sudo python setup.py install

Python: Markdown support
^^^^^^^^^^^^^^^^^^^^^^^^
::

    sudo easy_install Markdown

Python: RDF support
^^^^^^^^^^^^^^^^^^^
::

    sudo easy_install rdflib

Django
^^^^^^

* Download: https://www.djangoproject.com/download/ (download the source tarball, version **1.3** is currently needed!)
* Install::

    sudo python setup.py install

Django South DB migration library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    sudo easy_install South

Indivo Setup
------------

* It's easiest if you put both indivo_server and indivo_ui_server into the same directory (I used ``/Library/Indivo``), the commands below will do just that
* If you clone the Indivo code from github, don't forget to init the submodules::

    cd /Library/Indivo/
    git clone git@github.com:chb/indivo_server.git
    cd indivo_server/
    git submodule init
    git submodule update
    cd ..
    git clone git@github.com:chb/indivo_ui_server.git
    cd indivo_ui_server/
    git submodule init
    git submodule update

* Submodules may stall, you can clone them by hand (these three did stall for me)::

    cd indivo_ui_server/ui/jmvc/
    git clone git@github.com:jupiterjs/funcunit
    git clone git@github.com:jupiterjs/jquerymx jquery
    git clone git@github.com:jupiterjs/steal
    cd ../..
    git submodule update


Create the Indivo postgres user
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will create a PostgreSQL user named ``indivo`` and any password. Be sure to remember the password as you will need to put it into the Indivo settings later!::

    sudo su - postgres
    createuser --superuser indivo
    psql postgres
    postgres=# \password indivo
    postgres=# \q


Follow the instructions to configure Indivo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  :ref:`Server Config <indivo-server-config>`

  :ref:`UI Server Config <indivo-ui-server-config>`


Optional for Apache 2: mod_wsgi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Only needed if you want to run Indivo on top of Apache

* Check: Run ``httpd -M`` to check whether you have it already installed
* If not, download: http://code.google.com/p/modwsgi/downloads/detail?name=mod_wsgi-3.3.tar.gz (There is an installer ready made for OS X 10.6, but we're using the tarball here)
* Build & Install::

    ./configure
    make
    sudo make install

* Setup: To have Apache load the module, add this line to ``/etc/apache2/httpd.conf``::

    LoadModule wsgi_module libexec/apache2/mod_wsgi.so

* Follow the Wiki instructions to setup Apache. For OS X, there are minor deviations of the procedure. Two hints:
    * The virtual hosts config is in: ``/etc/apache2/extra/httpd-vhosts.conf``. Uncomment the inclusion command for this file in the main ``httpd.conf``
    * Restart Apache with::

        sudo apachectl graceful

* Some permission settings, make sure Apache has access to these files/directories:
  ``indivo_server/indivo.log``
  ``indivo_ui_server/settings``
  ``indivo_ui_server/indivo_client_py``
