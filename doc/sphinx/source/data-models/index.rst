Indivo Data Models
==================

Introduction
------------

:term:`Data Models <data model>` in Indivo describe the format in which Indivo represents medical information. They are
**NOT** the same as :term:`Schemas <schema>`, which describe formats that Indivo recognizes as valid input data. Rather,
data models describe the final processed state of medical data in Indivo: how data are stored, how they are queryable via
the :doc:`Query API </query-api>`.

We also introduce one additional term: :term:`Medical Facts <fact>`. A Fact is one datapoint corresponding to a data 
model: for example, a latex allergy is a Fact that is an instance of the :doc:`Allergy data model <allergy>`. Internally,
Indivo represents facts as Python objects, so you'll see us referencing medical facts as *fact objects* as well.

.. _data-model-definition-types:

Defining a Data Model
---------------------

At its most basic level, a data model definition is just a list of fields and their types. For example, our 
:doc:`Problem data model <problem>` is defined as (some fields omitted):

* *startDate*: Date
* *endDate*: Date
* *name*: String
* *notes*: String

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

.. autoclass:: indivo.fields.CodeField(Type)
   :noindex:
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.CodedValueField(Type)
   :noindex:
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.ValueAndUnitField(Type)
   :noindex:
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.AddressField(Type)
   :noindex:
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.NameField(Type)
   :noindex:
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.TelephoneField(Type)
   :noindex:
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.PharmacyField(Type)
   :noindex:
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.ProviderField(Type)
   :noindex:
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.VitalSignField(Type)
   :noindex:
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.BloodPressureField(Type)
   :noindex:
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.ValueRangeField(Type)
   :noindex:
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.fields.QuantitativeResultField(Type)
   :noindex:
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

Since the :doc:`Query API </query-api>` allows app developers to directly apply filters and ranges to the Data Models they
are selecting, they need to know what fields they are allowed to query against. The answer is simple:

**ANY FIELD ON A DATA MODEL THAT IS NOT A RELATION TO ANOTHER MODEL MAY BE USED IN THE QUERY API!**

For example, we introduced the 'Problem' model above, which has the fields:

* *startDate*: Date
* *endDate*: Date
* *name*: String
* *notess*: String

If you were making an API call such as :http:get:`/records/{RECORD_ID}/reports/Problem/`, you could filter by
any of:

* *startDate*
* *endDate*
* *name*
* *notes*

The Problem model is actually a bit more complicated, and has another field:

* *encounters*: Encounter

You won't be able to filter by *encounters*, since that field is a relation to another model.

The only exceptions to this rule are :ref:`custom Django Model Fields <custom-model-fields>`. Such fields are translated
into fields with other names, as described above. Any of these fields may be used in the query API, but (for example), 
when looking at a model with a Code element such as: 

* *name*: Code

You would be able to filter by *name_identifier*, *name_title*, or *name_system*, but not by
*name* itself. 

.. _core-data-models:

Core Data Models
----------------

Here is a listing of the core data models currently supported by Indivo. Each instance might define other, contributed models:
see :ref:`below <add-data-model>` for information on how to add data models to Indivo.

.. toctree::
   :maxdepth: 1

   allergy
   clinical_note
   encounter
   immunization
   lab_panel
   lab_result
   medication
   problem
   procedure
   social_history
   vital_signs

Advanced Data-Model Tasks
-------------------------

.. _data-model-options:

Adding Advanced Features to a Data-Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For complicated data models, a simple SDML definition just won't suffice. For a few specific features, such as 
:ref:`custom object serialization <custom-serializers>` or :ref:`creation-time field validation <data-model-validators>`, 
you can define (in python) an extra options file for a data model.

This file should be named ``extra.py``, and can be dropped into the filesystem next to any data model, as described 
:ref:`below <data-model-filesystem>`. The file should contain subclasses of 
:py:class:`indivo.data_models.options.DataModelOptions`, each of which describes the options for one data model defined in 
the ``model.py`` file in the same directory. Options are:

.. autoclass:: indivo.data_models.options.DataModelOptions(Type)
   :noindex:
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

For example, here's our options file for the Problem data model::

  from indivo.serializers import DataModelSerializers
  from indivo.data_models.options import DataModelOptions
  from indivo.validators import ExactValueValidator

  SNOMED_URI = 'http://purl.bioontology.org/ontology/SNOMEDCT/'

  class ProblemSerializers(DataModelSerializers):

      def to_rdf(query, record=None, carenet=None):
          # ... our SMART RDF serializer implementation here ... #
          return 'some RDF'

  class ProblemOptions(DataModelOptions):
    model_class_name = 'Problem'
    serializers = ProblemSerializers
    field_validators = {
        'name_title': [NonNullValidator()],
        'name_code_system': [ExactValueValidator(SNOMED_URI)],
        'name_code_identifier': [NonNullValidator()],
        'name_code_title': [NonNullValidator()],
        'startDate': [NonNullValidator()],
    }

Make sure to restart Indivo for your changes to take effect after you add your ``extra.py`` file--but there's no need to 
*reset* Indivo.

.. _custom-serializers:

Adding Custom Serializers to a Data-Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, when returning data via the :doc:`generic reporting API </generic-reports>`, Indivo will attempt to serialize
data as :ref:`SDMJ <sdmj>` or :ref:`SDMX <sdml>`, depending on the requested response format. If you need your data to come
back in other formats, or if the default serializers aren't smart enough to represent your data model correctly, you can 
implement custom serializers for the data model.

Defining the Serializers
""""""""""""""""""""""""

Serializers for a data model are implemented as simple methods that take a Django queryset object, and return a serialized
string. For a given data-model, you should define a subclass of :py:class:`indivo.serializers.DataModelSerializers`, and
add your desired serializers as methods on the class. Currently, available serializers are:

.. py:function:: to_xml(queryset, result_count, record=None, carenet=None)

   returns an XML string representing the model objects in *queryset*. 
   
   :param QuerySet queryset: the objects to serialize
   :param integer result_count: the total number of items in *queryset*
   :param Record record: the patient record that the objects belong to, if available.
   :param Carenet carenet: the Carenet via which the objects have been retrieved, if available.
   :rtype: string

.. py:function:: to_json(queryset, result_count, record=None, carenet=None)

   returns a JSON string representing the model objects in *queryset*.

   :param QuerySet queryset: the objects to serialize
   :param integer result_count: the total number of items in *queryset*
   :param Record record: the patient record that the objects belong to, if available.
   :param Carenet carenet: the Carenet via which the objects have been retrieved, if available.
   :rtype: string

.. py:function:: to_rdf(query, record=None, carenet=None)

   returns an RDF/XML string representing the model objects in *query.results*.

   :param FactQuery query: the Indivo FactQuery, containing the results and query options
   :param Record record: the patient record that the objects belong to, if available.
   :param Carenet carenet: the Carenet via which the objects have been retrieved, if available.
   :rtype: string

For example, here's a (non-functional) implementation of the serializers for the Problems data-model::

  from indivo.serializers import DataModelSerializers
  
  class ProblemSerializers(DataModelSerializers):
      def to_xml(queryset, result_count, record=None, carenet=None):
          return '''<Problems>...bunch of problems here...</Problems>'''

      def to_json(queryset, result_count, record=None, carenet=None):
          return '''[{"Problem": "data here"}, {"Problem": "More data here..."}]'''

      def to_rdf(query, record=None, carenet=None):
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

Adding custom serializers to a data-model is simple: simply set your :py:class:`~indivo.serializers.DataModelSerializers`
subclass to the ``serializers`` attribute of a :py:class:`~indivo.data_models.options.DataModelOptions` subclass in
an ``extra.py`` file (see :ref:`above <data-model-options>` for info on adding advanced data-model options.

.. _data-model-validators:

Adding Field Validation to a Data-Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, data models defined in SDML are very permissive: all fields are nullable, and there are no constraints on valid
data points other than their type (string, date, etc.). In some cases, a data element could satisfy these constraints, but
still be invalid. For example, an Indivo Problem must have its name coded using SNOMED, so a problem without a snomed code is
invalid.

Defining the Validators
"""""""""""""""""""""""

In such cases, you can attach validators to the data model. `Django Validators <https://docs.djangoproject.com/en/1.2/ref/validators/>`_ are essentially just python callables that raise a :py:class:`django.core.exceptions.ValidationError` if they are
called on an invalid data point. We've defined a couple of useful validators, though you could use any function you'd like. 

For example, here's a validator that will accept only the value ``2``::

  from django.core.exceptions import ValidationError

  def validate_2(value):
      if value != 2:
          raise ValidationError("Invalid value: %s. Expected 2"%str(value))

Built in Validators
"""""""""""""""""""

Django provides a number of built-in validators, for which a full reference exists here: 
https://docs.djangoproject.com/en/1.2/ref/validators/#built-in-validators.

In addition, Indivo defines a few useful validators in :py:mod:`indivo.validators`:

.. autoclass:: indivo.validators.ValueInSetValidator(valid_values, nullable=False)
   :noindex:
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

.. autoclass:: indivo.validators.ExactValueValidator(valid_value, nullable=False)
   :noindex:
   :no-members:
   :no-undoc-members:
   :no-private-members:
   :no-show-inheritance:

Attaching Validators to a Data Model
""""""""""""""""""""""""""""""""""""

Adding custom validators to a data-model is simple: simply add the validator to the field_validators attribute of a 
:py:class:`~indivo.data_models.options.DataModelOptions` subclass in an ``extra.py`` file 
(see :ref:`above <data-model-options>` for info on adding advanced data-model options).

For example, let's add the requirement that Problem names must be coded as snomed. We can write the validator using
the built-in :py:class:`~indivo.validators.ExactValueValidator`::

  from indivo.validators import ExactValueValidator
  SNOMED_URI = 'http://purl.bioontology.org/ontology/SNOMEDCT/'
  snomed_validator = ExactValueValidator(SNOMED_URI)

We can then attach it to the ``name_system`` field of a Problem, which will guarantee that we only accept problems which
identify themselves as having a snomed code for their names::

  class ProblemOptions(DataModelOptions):
      model_class_name = 'Problem'
      field_validators = {
        'name_code_system': [snomed_validator]
      }  

Note that we put ``snomed_validator`` in a list, since we might theoretically add additional validators to the 
``name_code_system`` field.

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

.. _data-model-filesystem:

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
