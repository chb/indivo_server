Indivo Simple Data Modeling Lanaguage (SDML)
============================================

Introduction
------------

As of version 1.1, Indivo supports drag-and-drop substitution of data models within the filesystem. We expect that this will
encourage Indivo administrators to try their hands at building new data models for use with Indivo, but we recognize that
many will not have the python expertise necessary to implement models using the Django web framework. To enable the rapid
development and deployment of very simple data models without the overhead of learning Django, we have defined a basic 
language for representing data models: Simple Data Modeling Language, or SDML.

Data in Indivo is written to the database as python objects using Django's Object-Relational Mapper: this will be equally
problematic for those without python experience. Therefore, we have also defined languages for representing data in JSON
or XML with similar degrees of simplicity: Simple Data Modeling JSON (SDMJ) and Simple Data Modeling XML (SDMX).

.. seealso::

   | This document contains the specifications for these languages. For information on how and when to use them, see:

   * :doc:`transform`
   * :doc:`data-models/index`
   * :ref:`add-transform`
   * :ref:`add-data-model`
   
.. _sdml:

Defining Data Models: SDML
--------------------------

There are a number of existing languages for defining data models (see 
http://en.wikipedia.org/wiki/Category:Data_modeling_languages for a listing). However, most of these are much too 
generalized and powerful for our use case. What we want is a language that is very simple to use (low learning curve), and 
very limited in functionality (medical data models shouldn’t be too complex, and shouldn’t need most of the capabilities of 
a relational database). SDML therefore uses JSON’s syntax exactly, but has restrictions that allow us to define 
Django models with it.

Syntax
^^^^^^^

* A data model in SDML is represented by a JSON object: ``{}``
* Attributes are represented by JSON pairs: ``‘name’:’value’``
* All attributes are optional.
* The special attribute named ``’__modelname__’`` defines the name of the model.
* Fieldtypes (which are defined by the ‘value’ of an attribute) are restricted to the following:

   * Number
   * String
   * Date
   * :py:class:`CodedValue <indivo.fields.CodedValueField>`
   * :py:class:`ValueAndUnit <indivo.fields.ValueAndUnitField>`
   * :py:class:`Address <indivo.fields.AddressField>`
   * :py:class:`Name <indivo.fields.NameField>`
   * :py:class:`Telephone <indivo.fields.TelephoneField>`
   * :py:class:`Pharmacy <indivo.fields.PharmacyField>`
   * :py:class:`Provider <indivo.fields.ProviderField>`
   * :py:class:`VitalSign <indivo.fields.VitalSignField>`
   * :py:class:`BloodPressure <indivo.fields.BloodPressureField>`
   * :py:class:`ValueRange <indivo.fields.ValueRangeField>`
   * :py:class:`QuantitativeResult <indivo.fields.QuantitativeResultField>`
   * One-to-One
   * One-to-Many

* All types but One-to-One and One-to-Many are indicated by a simple string (i.e. ‘Number’ | 'CodedValue' | 'Provider')

* One-to-One fields are indicated by a sub-object, and may be nested arbitrarily::
  
    { 
        "__modelname__": "mymodel",
        "field1": "Date",
    	"field2": { 
	    "__modelname__": "mysubmodel",
            "subfield1": "String",
	    "subfield2": "Number",
	    "subfield3": {
	        "__modelname__": "mysubsubmodel",
	        "subsubfield1": "String"
      	    }
	} 
    }

* One-to-Many fields are indicated by a list containing a definition of a sub-object::

    { 
        "__modelname__": "mymodel",
        "field1": "Date",
    	"field2": [{ 
	    "__modelname__": "mysubmodel",
            "subfield1": "String",
	    "subfield2": "Number"
	}]
    }

And that’s it.

Example
^^^^^^^^

Here is an example definition of a medication data model (more complicated than our model, actually) using SDML::

  {
      "__modelname__": "TestMedication",
      "name": "String",
      "date_started": "Date",
      "date_stopped": "Date",
      "brand_name": "String", 
      "route": "String",
      "prescription": {
          "__modelname__": "TestPrescription",
          "prescribed_by_name": "String",
          "prescribed_by_institution": "String",
          "prescribed_on": "Date",
          "prescribed_stop_on": "Date"
      },
      "fills": [{
          "__modelname__": "TestFill",
          "date_filled": "Date",
          "supply_days": "Number",
          "filled_at_name": "String"
      }]
  }

This definition will create three new data models: *TestMedication*, *TestPrescription*, and *TestFill*. It will add a
one-to-one relation between TestMedication and TestPrescription, and a one-to-many relation between TestMedication and
TestFill. That is to say, each TestMedication might have one prescription and multiple fills.


Representing Data: SDMJ and SDMX
--------------------------------

Simple Data Modeling JSON (SDMJ) and Simple Data Modeling XML (SDMX) are two nearly identical methods of representing data 
that matches an SDML definition. The only difference is the form of the envelope around the data.

.. _sdmj:

SDMJ
^^^^

SDMJ looks exactly like SDML, with four key differences:

* The datatypes in SDML ('Number', 'String', 'Date') are replaced by the datapoints in SDMJ
* Each model has an attribute ``’__documentid__’``, specifying the ID of the source document
* Since all attributes are optional, any attribute may be omitted in SDMJ.
* In one-to-many attributes, SDMJ actually specifies multiple datapoints, instead of just defining a submodel in a list.

Here's an example SDMJ document matching the SDML definition above::

  {
      "__modelname__": "TestMedication",
      "__documentid__": "b1d83191-6edd-4aad-be4e-63117cd4c660",
      "name": "ibuprofen",
      "date_started": "2010-10-01T00:00:00Z",
      "date_stopped": "2010-10-31T00:00:00Z",
      "brand_name": "Advil",
      "prescription": {
          "__modelname__": "TestPrescription",
          "__documentid__": "b1d83191-6edd-4aad-be4e-63117cd4c660",
          "prescribed_by_name": "Kenneth D. Mandl",
          "prescribed_by_institution": "Children's Hospital Boston",
          "prescribed_on": "2010-09-30T00:00:00Z",
          "prescribed_stop_on": "2010-10-31T00:00:00Z"
      },
      "fills": [
          {
              "__modelname__": "TestFill",
              "__documentid__": "b1d83191-6edd-4aad-be4e-63117cd4c660",
              "date_filled": "2010-10-01T00:00:00Z",
              "supply_days": "15",
              "filled_at_name": "CVS"
          },
          {
              "__modelname__": "TestFill",
              "__documentid__": "b1d83191-6edd-4aad-be4e-63117cd4c660",
              "date_filled": "2010-10-16T00:00:00Z",
              "supply_days": "15",
              "filled_at_name": "CVS"
          }
      ]
  }

Note: we've removed the 'route' attribute as it was not required, and have added two fills. This will result in 4 
:term:`Fact objects <fact>` being saved to the database: one TestMedication, one TestPrescription, and two TestFills.

.. _sdmx:

SDMX
^^^^

SDMX looks exactly like SDMJ, with the exceptions that:

* It's XML
* attribute-value pairs are represented as ``<Field name="attribute_name">attribute_value</Field>``
* The ``__modelname__`` attribute is pulled out as a toplevel tag with ``documentId`` as an attribute: ``<Model name="model_name" documentId="id">``
* Each ``<Model />`` tag contains an attribute ``documentId``, specifying the ID of the source document
* In order to represent multiple toplevel datapoints, SDMX must always live under a root <Models> tag.

Here's the same example document we just saw as SDMJ in SDMX form:

.. include:: /../../../indivo/schemas/metadata/sdmx/sdmx.xml
   :literal:

For those who like to work with XML in conjunction with schemas, here's an XSD which describes SDMX and can be used to
validate it:

.. include:: /../../../indivo/schemas/metadata/sdmx/schema.xsd
   :literal:

Representing Dates
^^^^^^^^^^^^^^^^^^

Strings and Numbers in SDMX and SDMJ should simply be input as JSON or XML literals as appropriate. Dates work the same way,
with the exception that they need to be formatted (as with all dates and date-times in Indivo) as ISO 8601 UTC timestamps
as described in :ref:`data-formats`.
