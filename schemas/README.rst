Indivo Schemas
==============

This repository contains XML Schemas defining how Indivo accepts data
from apps, and presents data to them.

Schemas are divided into the following categories:

* *Metadata*: schemas that represent Indivo-specific or internal
  data structures, not medical data.

* *Ouput Data*: schemas that represent the way Indivo presents medical
  data to apps in response to API calls.

* *Core Input Data*: built-in schemas that represent medical data 
  formats that Indivo will recognize, process, and present via its
  reporting API.

* *Contributed Input Data*: Like Core Input Data, but the schemas are
  provided (and installed) by third parties.

* *Common*: schemas that provide supporting definitions for other 
  schemas (i.e. the schema for CodedValues).

Directory Format
----------------

Each schema should have its own directory, containing:

* A ``*.xsd`` file, which is the schema itself.

* Any number of ``*.xml`` files, which are examples of the schema,
  and which should validate against it.

* A ``transform.[py | xslt]`` file, which maps XML matching the schema
  to internal Indivo data models. Only required for Input Data schemas.

Validation
----------

The scripts in the ``utils`` folder can be used to validate datamodels in 
the repository. To validate, run::

  python utils/validate.py $ARGS

where ``$ARGS`` can be a list of schema directories to validate. If empty,
the script will validate all schemas in:

* ``metadata/``
* ``data/core/``
* ``data/contrib/``
* ``data/output/``

To validate a schema, the script will simply attempt to validate each
``*.xml`` file in the folder against the ``*.xsd`` file in the folder.
