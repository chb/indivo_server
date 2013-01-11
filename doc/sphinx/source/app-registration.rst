Registering Apps with Indivo
============================

As of version 2.0, Indivo has an official process for adding and managing apps on a given instance. For those of you
familiar with using ``indivo_data.xml`` for adding apps, the ``<machine_apps>`` and ``<user_apps>`` tags will no longer
be respected, and will not add apps to Indivo.

App Manifests
-------------

Previous releases of Indivo have relied on an implicit XML syntax in ``indivo_data.xml`` for representing an app within
Indivo. Now, applications must provide a declared manifest describing the application and its requirements. We have 
adopted the `SMART Project's <http://smartplatforms.org>`_ syntax for describing apps in manifests, but have added some
Indivo-specific parameters to accommodate the way Indivo represents applications. For compatibility, any valid SMART 
manifest will also be a valid Indivo manifest. 

See `The SMART Project's documentation 
<http://dev.smartplatforms.org/reference/app_manifest/>`_ 
for a description of the basic syntax of a manifest, which is JSON based. Below, we describe only the Indivo-specific
modifications.

User Apps
^^^^^^^^^

New Fields
""""""""""

An Indivo user-app may define (beyond the SMART-supported manifest fields) any of the following additional properties in
its manifest:

* *oauth_callback_url*: A callback URL for Indivo-style oAuth access
* *autonomous_reason*: An explanation for why the app requires offline access to patient records
* *has_ui*: ``true`` or ``false``, whether the app can be displayed in a browser.
* *frameable*: ``true`` or ``false``, whether the app should be loaded in an iframe in the Indivo UI.
* *indivo_version*: Required version of Indivo for compatibility

Changes from the indivo_data.xml fields
"""""""""""""""""""""""""""""""""""""""

The following fields have changed names to match the SMART manifest fields:

* *email*: Has been renamed *id*, per SMART.

* *start_url_template*: Has been renamed *index*. If using Indivo-style oAuth authentication, the same templating
  parameters may be passed in the URL (i.e. {record_id})

* *is_autonomous*: Has been moved to the SMART *mode* property. Acceptable modes are:

  * *background*: This app will act like an autonomous Indivo app.
  * *ui*: This app will act like a non-autonomous Indivo app.

Example
"""""""

::

  {
    "name" : "Problems",
    "description" : "Display a list of problems, or enter new ones.",
    "author" : "Arjun Sanyal, Children's Hospital Boston",
    "id" : "problems@apps.indivo.org",
    "version" : "1.0.0",
    "smart_version": "0.4",

    "mode" : "ui",	
    "scope": "record",
    "has_ui": true,
    "frameable": true,

    "icon" :  "jmvc/ui/resources/images/app_icons_32/problems.png",
    "index": "/apps/problems/start_auth?record_id={record_id}&amp;carenet_id={carenet_id}",
    "oauth_callback_url": "/apps/problems/after_auth"
  }


UI and Admin Apps
^^^^^^^^^^^^^^^^^

New Fields
""""""""""

An Indivo user-app may define (beyond the SMART-supported manifest fields) any of the following additional properties in
its manifest:

* *ui_app*: ``true`` or ``false``. Whether the machineapp is a UIApp ('chrome app').
* *indivo_version*: Required version of Indivo for compatibility

Changes from the indivo_data.xml fields
"""""""""""""""""""""""""""""""""""""""

The following fields have changed names to match the SMART manifest fields:

* *email*: Has been renamed *id*, per SMART.
* *app_type*: Please use the *ui_app* field, above.

Example
"""""""

::

  {
    "name": "Sample UI App",
    "description" : "The reference Indivo UI App",
    "author" : "Ben Adida, Travers Franckle, Arjun Sanyal, Pascal Pfiffner, Daniel Haas. Children's Hospital Boston",
    "id" : "chrome@apps.indivo.org",
    "version" : "2.0.0",
    "indivo_version": "2.0.0",
    "ui_app": true
  }

App oAuth Credentials
---------------------

When authenticating to Indivo using :ref:`traditional oAuth <traditional-oauth>`, applications must provided Indivo with
their consumer key and a shared consumer_secret. As this secret is private and should not be shared with other apps (i.e.,
via a call to :http:get:`/apps/`), it should be registered in a separate file. We therefore define a simple JSON format for
specifying app oAuth credentials, which is simple JSON and has two fields:

* *consumer_key*: The oAuth consumer key for the app.
* *consumer_secret*: The oAuth consumer secret for the app.

Here's a sample credentials file, for our built-in Problems app::

  {
      "consumer_key": "problems@apps.indivo.org",
      "consumer_secret": "SECRETFORTHEPROBLEMSAPP:CHANGEME"
  }

.. note::

	* If your app is a SMART app, you probably haven't explicitly generated a 'consumer key'. You should set the 
	  ``consumer_key`` field of the credentials file to match the ``id`` field of your app manifest file.
	
	* If your app is a SMART CONNECT app (or connects to Indivo using :ref:`connect-auth`), you do not need a 
	  consumer secret. In such a case, set the ``consumer_secret`` field of the credentials file to the empty 
	  string: ``''``.

Managing the Registered Apps
----------------------------

Thus, to register an app with Indivo, you need two files: an app manifest (``manifest.json``) and a credentials file
(``credentials.json``).

Changing the set of registered apps in Indivo is now drag-and-drop, as with our process for managing datatypes and schemas.
To add, remove, or change an app, you'll need to:

* Create a manifest and credentials file for the app (or modify existing manifests/credentials)
* Drop the files into the filesystem
* Sync the database with the filesystem

Apps in the Indivo Filesystem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Indivo apps currently have the following layout on the filesystem::

  indivo_server/
      registered_apps/
          admin/
          ui/
          user/
              allergies/
                  manifest.json
                  credentials.json
		        ...

To add an app to the filesystem, simply add a subdirectory under ``indivo_server/registered_apps/admin``,
``indivo_server/registered_apps/ui``, or ``indivo_server/registered_apps/user`` (depending on the type of your app), and
drop a manifest and a credentials file into that directory.

To remove an app, just delete its directory.

To change an app's manifest or credentials, just modify the appropriate ``manifest.json`` or ``credentials.json`` file.


Syncing the Database with the Filesystem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To alert Indivo that you've changed the registered apps, run (from ``indivo_server/``)::

  python manage.py sync_apps

This will process the list of registered apps and sync any additions, deletes or updates to the database.

Resetting Indivo
^^^^^^^^^^^^^^^^

With the new system, there is **NO NEED TO RESET INDIVO TO ADD APPS!**. Simply run the ``sync_apps`` command, above. 

When you do reset Indivo, the reset script now calls ``sync_apps``, which will add all of the registered apps to Indivo.

