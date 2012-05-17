Indivo Data Models
==================

Introduction
------------

:term:`Data Models <data model>` in Indivo describe the format in which Indivo represents medical information. They are
**NOT** the same as :term:`Schemas <schema>`, which describe formats that Indivo recognizes as valid input data. Rather,
data models describe the final processed state of medical data in Indivo: how data are stored, how they are queryable via
the :doc:`Query API </query-api>`, and how they are returned via the :ref:`Reporting API <processed-reports>`.

We also introduce one additional term: :term:`Medical Facts <fact>`. A Fact is one datapoint corresponding to a data 
model: for example, a latex allergy is a Fact that is an instance of the :doc:`Allergy data model <allergy>`. Internally,
Indivo represents facts as Python objects, so you'll see us referencing medical facts as *fact objects* as well.

.. _data-model-definition-types:

Defining a Data Model
---------------------

At its most basic level, a data model definition is just a list of fields and their types. For example, our 
:doc:`Problem data model <problem>` is defined as (some fields omitted):

* *date_onset*: Date
* *date_resolution*: Date
* *name*: String
* *comments*: String
* *diagnosed_by*: String

This is pretty simple, and we'd like to enable others add new data models to Indivo just as easily. So we currently
allow two formats for defining data models:

Django Model Classes
^^^^^^^^^^^^^^^^^^^^

Since our data models are directly mapped to database tables using `Django's ORM <https://www.djangoproject.com/>`_, they 
are most effectively represented as Django Models. Django has a flexible, powerful method for expressing fields as python 
class attributes, so data models defined in this way can harness the full capabilities of the Django ORM. Of course, 
representing data models in this way requires some knowledge of python. For a full reference of Django models, see 
`Django models <https://docs.djangoproject.com/en/1.4/topics/db/models/>`_ and 
`Django model fields <https://docs.djangoproject.com/en/1.4/ref/models/fields/>`_.

One important Indivo-specific note: when defining Django Model Classes, make sure to subclass 
:py:class:`indivo.models.Fact`, which will ensure that your class can be treated as a data model. For example, your class
definition might look like::

  from indivo.models import Fact
  from django.db import models
  
  class YourModel(Fact):
      your_field1 = models.CharField(max_length=200, null=True)
      
      ...
      
      # Additional fields here

.. _custom-model-fields:

Custom Django Model Fields
""""""""""""""""""""""""""

For modeling medical data, Indivo provides some custom Field Subclasses. These fields represent their data as multiple 
separate database fields, with names formed from the original field's name and some appended sufffixes (see the classes
below for some examples). You should use these fields as if they were any other Django Model Field::

  from indivo.models import Fact
  from django.db import models
  from indivo.fields import YourFavoriteFieldSubclass

  class YourModel(Fact):
      normal_field = models.CharField(max_length=200, null=True)
      special_field = YourFavoriteFieldSubclass()

Now YourModel has both a standard CharField, and also other fields defined by the Field Subclass. We define the following 
Field Subclasses:

.. autoclass:: indivo.fields.CodedValueField(Type)
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.ValueAndUnitField(Type)
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.AddressField(Type)
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.NameField(Type)
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.TelephoneField(Type)
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.PharmacyField(Type)
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.ProviderField(Type)
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.VitalSignField(Type)
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.BloodPressureField(Type)
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.ValueRangeField(Type)
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.QuantitativeResultField(Type)
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:


Simple Data Modeling Language (SDML)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For those less python-savvy who are still capable of thinking in terms of 'fields' and 'types' (which should be most 
people), we've defined a JSON-based modeling language for defining the very simple data models easily. :doc:`SDML </sdm>` is
less flexible than Django's modeling language, but is much quicker to get started with and is less verbose for describing 
simple models. See our documentation of the language :ref:`here <sdml>`.

Feeling Lost?
^^^^^^^^^^^^^

For help getting started, see our :ref:`core data models <core-data-models>`, below, each of which provide definitions 
both in SDML and Django Model classes.

.. _queryable-fields:

Data Models and the Query API
-----------------------------

Since the :doc:`Query API </query-api>` allows app developers to directly apply filters and ranges to the datamodels they
are selecting, they need to know what fields they are allowed to query against. The answer is simple:

**ANY FIELD ON A DATA MODEL THAT IS NOT A RELATION TO ANOTHER MODEL MAY BE USED IN THE QUERY API!**

For example, we introduced the 'Problem' model above, which has the fields:

* *date_onset*: Date
* *date_resolution*: Date
* *name*: String
* *comments*: String
* *diagnosed_by*: String

If you were making an API call such as :http:get:`/records/{RECORD_ID}/reports/minimal/problems/`, you could filter by
any of:

* *date_onset*
* *date_resolution*
* *name*
* *comments*
* *diagnosed_by*

If the problems model were a bit more complicated, and had another field:

* *prescribed_med*: Medication

You wouldn't be able to filter by *prescribed_med*, since that field is a relation to another model.

The only exceptions to this rule are :ref:`custom Django Model Fields <custom-model-fields>`. Such fields are translated
into fields with other names, as described above. Any of these fields may be used in the query API, but (for example), 
when looking at a model with a CodedValue element such as: 

* *problem_type*: CodedValue

You would be able to filter by *problem_type_identifier*, *problem_type_title*, or *problem_type_system*, but not by
*problem_type* itself. 

.. _core-data-models:

Core Data Models
----------------

Here is a listing of the data models currently supported by Indivo. Each instance might define other, contributed models:
see :ref:`below <add-data-model>` for information on how to add data models to Indivo.

.. toctree::
   :maxdepth: 1

   allergy
   equipment
   immunization
   lab
   medication
   problem
   procedure
   vitals
   scn

Advanced Data-Model Tasks
-------------------------

.. _custom-serializers:

Adding Custom Serializers to Indivo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, when returning data via the :doc:`generic reporting API </generic-reports>`, Indivo will attempt to serialize
data as :ref:`SDMJ <sdmj>` or :ref:`SDMX <sdml>`, depending on the requested response format. If you need your data to come
back in other formats, or if the default serializers aren't smart enough to represent your data model correctly, you can 
implement custom serializers for the data model.

Defining the Serializers
""""""""""""""""""""""""

Serializers for a data model are implemented as simple methods that take a Django queryset object, and return a serialized
string. For a given data-model, you should define a subclass of :py:class:`indivo.serializers.DataModelSerializers`, and
add your desired serializers as methods on the class. Currently, available serializers are:

* ``to_xml(queryset)``: returns an XML string representing the model objects in *queryset*
* ``to_json(queryset)``: returns a JSON string representing the model objects in *queryset*
* ``to_rdf(queryset)``: returns an RDF/XML string representing the model objects in *queryset*

For example, here's a (non-functional) implementation of the serializers for the Problems data-model::

  from indivo.serializers import DataModelSerializers
  
  class ProblemSerializers(DataModelSerializers):
      model_class_name = "Problem"

      def to_xml(queryset):
          return '''<Problems>...bunch of problems here...</Problems>'''

      def to_json(queryset):
          return '''[{"Problem": "data here"}, {"Problem": "More data here..."}]'''

      def to_rdf(queryset):
          return '''<rdf:RDF><rdf:Description rdf:type='indivo:Problem'>...RDF data here...</rdf:Description></rdf:RDF>'''

A couple things to note:

* The ``to_*()`` methods **DO NOT** take ``self`` as their first argument. Under the hood, we actually rip the methods
  out of the serializers class and attach them directly to the data-model class.

* The ``model_class_name`` attribute is required, and indicates which data-model the serializers should be attached to.

Libraries for Serialization
"""""""""""""""""""""""""""

When serializing models, the following libraries can come in handy:

* ``lxml.etree``: Our favorite XML manipulation library. See http://lxml.de/tutorial.html for the details. Lxml is required
  for a running Indivo instance, so it will always be available for import (``from lxml import etree``).

* ``simplejson``: Our favorite JSON manipulation library. See http://simplejson.readthedocs.org/en/latest/index.html. 
  Django bundles a version of simplejson, which can be imported with ``from django.utils import simplejson``.

* ``rdflib``: Our favorite RDF manipulation library. See http://readthedocs.org/docs/rdflib/en/latest/. RDFLib may not be
  installed on all systems, so if you use it, make sure to install it first.

Attaching the Serializers to a Data Model
"""""""""""""""""""""""""""""""""""""""""

Adding custom serializers to a data-model is simple: simply save your :py:class:`~indivo.serializers.DataModelSerializers`
subclass to a file named ``extra.py``, and drop it into the directory where the data-model resides. More on the structure
of those directories :ref:`below <add-data-model>`.

Make sure to restart Indivo for your changes to take effect--but there's no need to *reset* Indivo.

.. _add-data-model:

Adding Custom Data-Models to Indivo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As of version 1.1 of Indivo X, we've added a feature that makes it much easier to add (in a drag-and-drop fashion)
new supported data models to an instance of Indivo. Adding a new data model to Indivo involves:

* Creating the data model definition
* Dropping the data model into the filesystem
* Migrating the database tables to support the new model

Defining the Data Model
"""""""""""""""""""""""

As you saw :ref:`above <data-model-definition-types>`, data models can be defined in two formats: SDML or Django model
classes. Simply produce a definition in one of the two forms, and save it to a file named **model.sdml** or **model.py**.

Dropping the Definition into the Filesystem
"""""""""""""""""""""""""""""""""""""""""""

Indivo data models currently have the following layout on the filesystem::

  indivo_server/
      indivo/
            ...
          data_models/
              core/
                  allergy/
                      model.[sdml | py]
                      example.[sdmj | sdmx | py]
                      extra.py
                    ...
              contrib/

The ``indivo/data_models/core/`` directory contains all of our built-in data models, and you shouldn't modify it. 
Since you are 'contributing' a data model to Indivo, add your data model to the ``indivo/data_models/contrib/`` directory. 
Simply:

* Create a new subdirectory under ``indivo/data_models/contrib/``.

* Drop your model definition into that directory. This file **MUST BE NAMED MODEL.PY OR MODEL.SDML** to be identified as
  a data model.

* Add (optional) example files into that directory. Files should be named **example.sdmj**, **example.sdmx**, or 
  **example.py**, and should be example instances of the data model as :ref:`SDMJ <sdmj>`, :ref:`SDMX <sdmx>`,
  or :term:`Fact objects <fact>` respectively. If present, they will help others use and document your data model.

* Add an (optional) extras file to the directory. The file must be named **extra.py**, and may contain extra options
  for your data-model, such as :ref:`custom serializers <custom-serializers>`.

* Your final directory structure should now look something like::

    indivo_server/
        indivo/
              ...
            data_models/
                core/
                    allergy/
                        model.[sdml | py]
                        example.[sdmj | sdmx | py]
                        extra.py
                      ...
                contrib/
                    your_data_model/
                        model.[sdml | py]
                        example.[sdmj | sdmx | py]
                        extra.py

Migrating the Database
""""""""""""""""""""""

Indivo relies on the `South migration tool <http://south.aeracode.org/>`_ to get the database synced with the latest data 
models. Once you've dropped your data model into the filesystem, South should be able to detect the necessary changes.

To detect the new model and generate migrations for it, run (from the ``indivo_server`` directory)::

  python manage.py schemamigration indivo --auto

You should see output like::

  + Added model indivo.YOURMODELNAME
  Created 0018_auto__add_model_YOURMODELNAME.py. You can now apply this migration with: ./manage.py migrate indivo

To do a quick sanity check that you aren't about to blow away your database, run::

  python manage.py migrate indivo --db-dry-run -v2

This should output the SQL that will be run. Make sure this looks reasonable, ESPECIALLY if you are running Indivo on
Oracle, where the South tool is still in alpha. If the SQL looks reasonable, go ahead and run the migration, with::

  python manage.py migrate indivo

And you're all set!

Next Steps
""""""""""

Make sure to restart Indivo for your changes to take effect.

.. seealso::

   | Now you've added a new data model to Indivo: Congratulations! It can be stored in the database and queried via the API.
 
   But until you map a :doc:`Schema </schemas/index>` to it, you won't be able to actually add data to your new model. To 
   learn more, see:

   * :doc:`/data-pipeline`
   * :ref:`add-schema`
   * :ref:`add-transform`
