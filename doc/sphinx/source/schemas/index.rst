Indivo Schemas
==============

Introduction
------------

The new Indivo X schemas are an evolution of the Indivo 3.1 schemas, which were reused by other PCHR vendors. 

There are a number of XML standards for medical activities, ranging from the CCR summary to the highly detailed 
CCD. None of these are particularly well tuned to the needs of a PCHR, where individual datum may come from a 
hospital data feed, or from patient-based data entry. The Indivo schemas are built to serve the specific PCHR needs. 
Importantly, the Indivo schemas *use standard coding systems* wherever possible. The schemas are also ready for new 
coding systems as they emerge, especially in the realm of personally-controlled medicine with simplified terminology.

Major Changes from Indivo 3.1
-----------------------------

* Separation of medical payload and Indivo-specific metadata. The Indivo account that creates a document, for example, 
  is not part of the medical payload, and would likely mean little to other EMR or PCHRs. Thus, this metadata is now kept 
  in the :ref:`Indivo Document Metadata Schema <metadata-schema>`.

* A few tweaked fields based on our experience internally at Children's Hospital Boston and with other deployments.

* More consistent and generalized support for coding systems, including current and future ones without schema changes.

What if I want to store other data?
-----------------------------------

Indivo X is designed to accept documents that conform to any XML schema, such as CCR, and even documents that are not XML, 
i.e. PDFs, MPEG, etc....

XML documents that conform to the built-in schemas can be immediately transformed, via the Indivo X 
:doc:`Data Pipeline </data-pipeline>`, into individual datapoints, which can then be aggregated into reports. XML documents 
that conform to custom schemas currently cannot be included in Indivo aggregate reports, but will eventually be integrated.

Namespace and XML Types
-----------------------

All of the default Indivo X document schemas are in a single namespace::

  http://indivo.org/vocab/xml/documents#

The use of the trailing ``#`` enables simple RDF-like concatenation of namespace prefix and suffix to generate a single 
type URL. For example, an ``Allergy`` in the Indivo documents namespace will have as its type::

  http://indivo.org/vocab/xml/documents#Allergy

Design Rationale for Inclusion vs. Relation
-------------------------------------------

Indivo X brings the ability to relate documents to one another using metadata, rather than document payload. This is 
particularly important when the payload might not be under the user's control, i.e. a CCR document. It can also be useful
even in the design of new Indivo schemas.

One could imagine separation the prescription information from the medication information, having two documents related to one 
another rather than one bigger document. However, our design rationale for now is to keep medication and its prescription data 
in the same XML document because those two chunks of data are generated in the same event. If, at some point, Indivo stores 
prescription filling information, then it is likely that this information would be more appropriately stored in a separate, 
linked document.

Schemas
-------

All schema files and sample instance documents are available at http://indivo.org/vocab/xml/.

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

   allergy-schema
   immunization-schema
   problem-schema
   vitals-schema
   procedure-schema
   lab-schema
   medication-schema
   equipment-schema
   scn-schema
