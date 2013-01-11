Indivo Client Libraries
=======================

An Indivo client library is any code (in any language) provided as a standard package to app developers which
enables them to make :doc:`API calls <api-overview>` against Indivo without worrying about low-level implementation
details such as OAuth signing. We currently support a couple simple libraries: this document lists those
libraries, and provides advice for generating new libraries.

Supported Client Libraries
--------------------------

Currently, we have released the following client libraries:

Python Client
^^^^^^^^^^^^^

Our python client is a simple wrapper around the commonly used and supported 
`Python Oauth2 <https://github.com/simplegeo/python-oauth2>`_ library for making OAuth-signed REST calls.

Our code is available `on github <https://github.com/chb/indivo_client_py>`__, and documentation is 
available :doc:`in the Indivo docs <py-client-reference>`.

iOS Framework
^^^^^^^^^^^^^

The Indivo iOS Framework is an object-oriented wrapper that provides class-based access to core Indivo
data-types using the Indivo API.

The code is available `on github <https://github.com/chb/IndivoFramework-ios>`__, and documentation is
available `in the Indivo docs <http://docs.indivohealth.org/projects/indivo-x-ios-framework/en/latest/>`_.


SMART Clients
^^^^^^^^^^^^^

Since Indivo now supports the `SMART API <http://smartplatforms.org>`_, apps written using SMART client libraries
will also run on Indivo. See the documentation for SMART client libraries:

* `in javascript <http://dev.smartplatforms.org/libraries/javascript/>`_

* `in python <http://dev.smartplatforms.org/libraries/python/>`_

* `in java <http://dev.smartplatforms.org/libraries/java/>`_

* or `in .NET <http://dev.smartplatforms.org/libraries/dotnet/>`_

Building a Client Library
-------------------------

A client library's responsibilities are simple: it must be able to sign HTTP requests using OAuth, send them
to Indivo Server or an Indivo UI App (for OAuth authorization), and present the results of the requests back
to the app developer. Most languages have libraries for doing these things already, so building a new Indivo
client library is actually quite simple.

In order to facilitate auto-generation of clients, Indivo provides an ``api.xml`` file, which describes all 
of the calls a complete client should support. This file can be found in the indivo server source code, in
``indivo_server/api.xml``.

The ``api.xml`` file should be updated whenever the supported API calls are modified. In order to insure
that you have the most up-to-date version of the file, you can run (from a valid indivo_server checkout)::

  python manage.py generate_api_spec

Which will update the ``api.xml`` file to be consistent with the current codebase.
