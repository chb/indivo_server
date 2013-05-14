Upgrade Instructions
====================

This article documents the necessary steps to upgrade Indivo to a newer version from an older one. In general, ``Migration`` refers to updating database schemas when moving from one version to another, presumably without losing any data in the process. As of the Beta 1 release, Indivo will provide scripts to migrate its database to the latest version. The rest of this page is concerned with other steps necessary to bring Indivo up to date with the latest release.

Get the new codebase
--------------------

* Back up your old codebase: you wouldn't want to lose all of your work!
* Option 1: if you are using the git repos::

     $ cd /path/to/indivo_server
     $ git pull origin master
     $ git checkout v1.0.0              # Or your desired version
     $ git submodule update

     $ cd /path/to/indivo_ui_server
     $ git pull origin master
     $ git checkout v1.0.0              # Or your desired version
     $ git submodule update

* Option 2: if you'd like to use the git repos, but aren't already::

     $ cd /path/to/put/new/code
     $ git clone git://github.com/chb/indivo_server.git
     $ git clone git://github.com/chb/indivo_ui_server.git

     $ cd indivo_server
     $ git checkout v1.0.0              # Or your desired version
     $ git submodule init
     $ git submodule update

     $ cd ../indivo_ui_server
     $ git checkout v1.0.0              # Or your desired version
     $ git submodule init
     $ git submodule update

* Option 3: use a packaged release::

     $ cd /path/to/put/new/code
     $ wget https://github.com/downloads/chb/indivo_server/indivo_server-v1.0.0.tar.gz             # Or your desired packaged release
     $ wget https://github.com/downloads/chb/indivo_ui_server/indivo_ui_server-v1.0.0.tar.gz    # Or your desired packaged release
     $ tar xzvf indivo_server-v1.0.0.tar.gz
     $ tar xzvf indivo_ui_server-v1.0.0.tar.gz
     $ rm indivo_*.tar.gz

Configure the New Codebase
--------------------------

Indivo Server
^^^^^^^^^^^^^

* Back up your old ``settings.py`` file, if you have one.
* Copy ``settings.py.default`` to ``settings.py``, and merge your old changes into that file.

  .. warning::

    If you don't move to the latest settings file, you might miss new settings or changes to settings that will break Indivo.

* Check your file permissions (remember, the user running Indivo must have write access to ``indivo_server/indivo.log``).
* Regenerate the python test client, which might have changed to a new version::

    $ python indivo/tests/client/lib/create_api.py

  (This script does not output anything, so don't be alarmed when it ends silently).

Indivo UI Server
^^^^^^^^^^^^^^^^

* Back up your old ``settings.py`` file, if you have one.
* Copy ``settings.py.default`` to ``settings.py``, and merge your old changes into that file.

  .. warning::
    If you don't move to the latest settings file, you might miss new settings or changes to settings that will break Indivo UI.

* Check your file permissions (remember, the user running Indivo must have write access to ``indivo_ui_server/sessions/`` and all of its contents).
* For versions < 2.0.0, regenerate the python client, which might have changed to a new version::

    $ python indivo_client_py/lib/create_api.py
    (This script does not output anything, so don't be alarmed when it ends silently).

Update Your Database
--------------------

Migration: If you have data you need to keep
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, **BACK UP YOUR DATABASE!!** Then, run the Indivo migration script. Depending on your version, the call might look slightly different.

.. note::

    The package we rely on to handle Indivo data migrations, `South <http://south.aeracode.org/>`_, is still in alpha for the Oracle backend. If you are running Oracle, you may not be able to run the migration scripts below.

2.0
"""
Unfortunately, with the adoption of SMART data models, there is **no automatic migration path** from previous versions.  The SMART data models are not too different in content from the previous Indivo ones, so it is possible to write an app for migration if you need to make the transition.

1.0
"""
For version 1.0, use the same migration script as previously, with the new target of '1.0'::

    ./migration_scripts/migrate_indivo.sh 1.0

Beta 3
""""""
As of Beta 3, the migration script now takes an additional argument: the version you wish to migrate to. If you have the Beta 3 indivo codebase or later, in the Indivo Home Directory (``indivo_server``, if you installed Indivo according to our instructions), run::

    ./migration_scripts/migrate_indivo.sh <target>

Acceptable targets are ``beta1``, ``beta2``, or ``beta3``

Beta 2
""""""
Migrating Indivo is as simple as it gets. In the Indivo Home Directory (``indivo_server``, if you installed Indivo according to our instructions), run::

    ./migration_scripts/migrate_indivo.sh

And that's it! Your database will now be ready for the newest version of Indivo.

Reset: If you don't mind losing all existing data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Version 1.0 and above
"""""""""""""""""""""
* Backup ``utils/indivo_data.xml``
    .. note::

        If you are moving to version 2.X.X, apps are no longer defined in indivo_data.xml.  Look at the latest indivo_data.xml.default for what can carry over, and then check out the new registered_apps directory for examples of how to migrate your apps in the new JSON format.

* Copy ``utils/indivo_data.xml.default`` to ``utils/indivo_data.xml``, and merge your old changes into that file.
    .. warning::

        If you don't move to the new data file, you might miss formatting changes that will prevent Indivo from loading your initial data.

* Take a look at the options for the indivo reset script::

    $ cd indivo_server
    $ python utils/reset.py --help

* After a migration, it is usually helpful to drop and recreate the database with the ``--force-drop`` option. So try resetting the database, using::

    $ python utils/reset.py --force-drop

If you have codingsystems data to load, add the ``-c`` flag::

    $ python utils/reset.py --force-drop -c

Pre-Version 1.0
"""""""""""""""
* Backup ``utils/indivo_data.xml``

* Copy ``utils/indivo_data.xml.default`` to ``utils/indivo_data.xml``, and merge your old changes into that file.
    .. warning::

        If you don't move to the new data file, you might miss formatting changes that will prevent Indivo from loading your initial data.

* Run the indivo reset script::

    $ cd indivo_server
    $ ./utils/reset.sh -sb

If you have codingsystems data to load, add the ``-c`` flag::

    $ ./utils/reset.sh -sbc

Check the Release Notes
-----------------------

There may be version-specific issues to handle. Take a look at the [[ Releases | Release Notes]].

Specifically, make sure to check that Indivo's dependencies are all up to date. For example, in the 1.0.0 release, Indivo dropped support for Django version 1.1. Make sure to upgrade Django to version 1.2+ in order to run Indivo 1.0.0+

Run Some Sanity Checks
----------------------
* Does the Indivo Test Suite run?::

    $ cd indivo_server
    $ python manage.py test indivo

* Do the development servers start up?::

    $ cd indivo_server
    $ python manage.py runserver 0.0.0.0:8000      # Or your preferred port to run Indivo Server on (MUST MATCH settings.py!)

    $ cd ../indivo_ui_server
    $ sudo python manage.py runserver 0.0.0.0:80  # Or your preferred port to run Indivo UI Server on (MUST MATCH settings.py!)

* Does Indivo seem to be working? Try logging in from a browser and clicking around.
