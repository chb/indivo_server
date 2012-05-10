Indivo Schemas
==============

Introduction
------------

:term:`Schemas <schema>` in Indivo are used to describe valid formats in which data may enter Indivo. Right now, we
use `XSDs <http://www.w3.org/XML/Schema>`_ as schemas, since we accept input data only in XML form, but in the future
we might extend this to include schemas for validating other formats of data (OWL for RDF, etc.). Note that schemas
describe *the format of input data only!* For information on how data is processed and stored in Indivo, see
:doc:`/data-pipeline`.

There are a number of XML standards for medical activities, ranging from the CCR summary to the highly detailed 
CCD. None of these are particularly well tuned to the needs of a PCHR, where an individual datum may come from a 
hospital data feed, or from patient-based data entry. The Indivo schemas are built to serve the specific PCHR needs. 
Importantly, the Indivo schemas *use standard coding systems* wherever possible. The schemas are also ready for new 
coding systems as they emerge, especially in the realm of personally-controlled medicine with simplified terminology.

What if I want to store data that doesn't match an Indivo schema?
-----------------------------------------------------------------

Indivo X is designed to accept documents that conform to any XML schema, such as CCR, and even documents that are not XML, 
i.e. PDFs, MPEG, etc....

XML documents that conform to the built-in schemas can be immediately transformed, via the Indivo X 
:doc:`Data Pipeline </data-pipeline>`, into individual datapoints, which can then be queried using the 
:ref:`Indivo Reporting API <processed-reports>`. XML documents that conform to custom schemas are not processed, and 
therefore cannot be retrieved using the reporting API (though you can still access them with 
:ref:`API calls for retrieving unprocessed documents <reading-documents-API>`, which will return them in their original 
XML form.

If you want to extend Indivo to enable querying over data input according to a new schema, see 
:ref:`Adding Custom Schemas to Indivo <add-schema>`.

Namespace and XML Types
-----------------------

All of the default Indivo X document schemas are in a single namespace::

  http://indivo.org/vocab/xml/documents#

The use of the trailing ``#`` enables simple RDF-like concatenation of namespace prefix and suffix to generate a single 
type URL. For example, an :doc:`SDMX <sdmx-schema>` document in the Indivo documents namespace will have as its type::

  http://indivo.org/vocab/xml/documents#Models

Design Rationale for Inclusion vs. Relation
-------------------------------------------

Indivo X brings the ability to relate documents to one another using metadata, rather than document payload. This is 
particularly important when the payload might not be under the user's control, i.e. a CCR document. It can also be useful
even in the design of new Indivo schemas.

One could imagine separation the prescription information from the medication information, having two documents related to 
one another rather than one bigger document. However, our design rationale for now is to keep medication and its 
prescription data in the same XML document because those two chunks of data are generated in the same event. If, at some 
point, Indivo stores prescription filling information, then it is likely that this information would be more appropriately 
stored in a separate, linked document.

Core Schemas
------------

All schema files and sample instance documents are available at http://indivo.org/vocab/xml/. Note that these schemas
are only the ones that come with Indivo by default. Each instance of Indivo might define additional, custom schemas that
are not documented here. See :ref:`add-schema` for instructions on how to add custom schemas to Indivo.

Metadata and Indivo Internal Data Structures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   metadata-schema
   account-schema
   pha-schema
   audit-schema
   carenet-schema
   doc-status-schema
   message-schema
   notification-schema
   permissions-schema
   record-schema
   reqtoken-schema
   codes-schema
   values-schema
   provider-schema

Reporting
^^^^^^^^^

.. toctree::
   :maxdepth: 2

   reporting-schema
   aggregate-schema
   aggregate-generic-schema

Special Documents
^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   demographics-schema
   contact-schema
   annotation-schema

.. _medical-schemas:

Medical Documents
^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   immunization-schema
   vitals-schema
   procedure-schema
   lab-schema
   equipment-schema
   scn-schema
   sdmx-schema

.. _add-schema:

Adding Custom Schemas to Indivo
-------------------------------

As of version 1.1 of Indivo X, we've added a feature that makes it much easier to add (in a drag-and-drop fashion)
new supported schemas to an instance of Indivo. Adding a new schema to Indivo involves:

* Creating the schema
* Mapping the schema to Indivo's Data Models
* Dropping the schema into the filesystem

Creating the Schema
^^^^^^^^^^^^^^^^^^^

Indivo currently accepts schemas only in XSD form. There are numerous tutorials and tools on the web to help you create
an XSD, so we won't presume to tell you how you should do it. What matters is that you build an XSD which can validate
documents for further processing in the :doc:`Indivo data pipeline </data-pipeline>`.

Mapping the Schema to Data Models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to arrived at processed :term:`facts <Fact>` that can be queried and retrieved, you'll need to a way to transform
documents matching your schema into a form understood by Indivo. We call this tool (intuitively) a :term:`Transform`, and
you can learn how to build one :doc:`here </transform>`.

If the data in your new schema doesn't fit into any of the Indivo Data Models, and you want to add a new data-model to
Indivo, see :ref:`add-data-model`.

Dropping the Schema into the Filesystem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Indivo schemas currently have the following layout on the filesystem::

  indivo_server/
      indivo/
            ...
          schemas/
              utils/
              metadata/
              data/
                  common/
                  output/
                  core/
                      sdmx/
                          schema.xsd
                          transform.[xslt | py]
                          sdmx.xml
                        ...
                  contrib/

The ``indivo/schemas/data/core/`` directory contains all of our built-in schemas, and you shouldn't modify it. Since you are
'contributing' a schema to Indivo, add your schema to the ``indivo/schemas/data/contrib/`` directory. Simply:

* Create a new subdirectory under ``indivo/schemas/data/contrib/``.

* Drop the following files into that directory:

  * ``schema.xsd``: Your schema. This file **MUST BE NAMED SCHEMA.XSD** to be identified as a schema.
  * ``transform.xslt`` or ``transform.py``: Your transform. This file **MUST BE NAMED 'transform'** to be identified.
  * ``sample.xml`` (*optional*): A sample document that should validate against your schema. This is optional, but is 
    a good way to make sure your schema works as intended. If you have one or more sample xml files in your directory
    (you can name them anything, as long as the filename ends in '.xml'), you can make sure that they all validate by 
    running::
    
      cd indivo_server/indivo/schemas
      python utils/validate.py

    This will validate all sample documents against their schema: you should see 'ok' at the end of each line of output
    if there were no errors.

* Restart Indivo for your changes to take effect. Your final directory structure should now look something like::

    indivo_server/
        indivo/
              ...
            schemas/
                utils/
                metadata/
                data/
                    common/
                    output/
                    core/
                        sdmx/
                            schema.xsd
                            transform.[xslt | py]
                            sdmx.xml
                          ...
                    contrib/
                        your_schema/
                            schema.xsd
                            transform.[xslt | py]
                            your_example1.xml
                            your_exampl2.xml
                              ...
