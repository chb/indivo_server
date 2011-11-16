Indivo API
==========

The Indivo API provides an interface for Personal Health Applications to extend the functionality of the 
Indivo PCHR. The Indivo API abides by the REST design pattern: it is stateless, re-uses existing HTTP 
constructs such as caching, compression and content negotiation, and generally uses URLs to represent 
hierarchical resources, e.g. documents within a medical record.

Overview
--------

Personal Health Applications (PHAs) make HTTP calls to the Indivo API endpoint using the REST convention. 
`oAuth <http://oauth.net>`_ is used to authenticate all calls, either in 2-legged mode for simple 
authentication, or in 3-legged mode when the PHA is making a call with delegated authentication, i.e. on 
behalf of the user.

Application Types
^^^^^^^^^^^^^^^^^

We consider three types of applications:

* **User Applications**, which individual Indivo users can add to their record.

* **Administrative Applications**, which are used to perform account and record manipulations.

* **UI Applications**, which provide the public user interface to Indivo features.

Per Indivo installation, there is a small handful of UI and administrative applications, and quite a 
number of user applications.

Terminology
^^^^^^^^^^^

A **record** is the single set of medical information that pertains to an individual. It is composed of 
**documents**, including a **demographics document** which details the individual's contact information and 
name. A record can be accessed by one or more **accounts**.

**oAuth** is the authentication protocol used by Indivo. In 2-legged oAuth, the PHA (the oAuth **consumer**) 
makes calls to Indivo (the oAuth **service provider**) using a **consumer key** to identify itself, and a 
**consumer secret** to sign the request. In 3-legged oAuth, the PHA makes calls to Indivo to access medical 
information as delegated by the user, using an additional **token** and **token secret** that pertain to the 
specific Indivo record being accessed.

Authentication
--------------

All calls to Indivo are authenticated using `oAuth <http://oauth.net>`_.

We detail the authentication process at :doc:`authentication`.

Design Patterns
---------------

Some common design patterns are repeated throughout the API. Not all of these patterns are necessarily 100% 
supported by all Indivo API implementations, though when they are they are consistent.

Email Addresses as Identifiers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Core accounts in Indivo X are identified by email addresses, because email addresses provide mechanisms for 
distributed identification and messaging. When an email address is included in a URL, it must be URL encoded, 
where the ``@`` sign turns into ``%40``.

Paging/Filtering Results
^^^^^^^^^^^^^^^^^^^^^^^^

When a list of results are returned, the URL ends in a ``/`` and the HTTP method is a ``GET``, as is typical of 
REST design. In that case, Indivo X supports a generic query string that determines paging and ordering of 
the results::

  ?offset={offset}&limit={limit}&order_by={order_by}&status={document_status}&modified_since={modified_since}

* ``offset`` indicates which item number to start with, e.g. when getting a second batch of items.

* ``limit`` indicates the maximum number of items to return. This is used in combination with offset to 
  accomplish paging.

* ``order_by`` is dependent on the fields returned in the list of items, and each call must thus define which 
  fields are valid. Using an invalid field in order_by results in no effect on the output, as if order_by 
  were absent.

* ``status`` can be used where applicable. It pertains to the status of documents and can currently be set to 
  one of three options: 'void', 'archived' or 'active'

* ``modified_since`` allows an application to look at items that have been modified since a given timestamp, 
  so that incremental downloads may be possible.

Querying Results
^^^^^^^^^^^^^^^^

As of the Beta3 release, calls that implement the basic paging operations above may also implement a more 
powerful :doc:`query interface <query-api>`, also represented in the query string. In these cases (currently 
all of the minimal medical reports and the auditing calls), the following values may occur in the query string::

  ?offset={offset}&limit={limit}&order_by={order_by}&status={document_status}

These values function as before. ::

  ?group_by={group_field}&aggregate_by={aggregation_operator}*{aggregation_field}

``group_by`` groups results by the specified field. It must be used in conjunction with ``aggregate_by``, which 
aggregates the results by group, using the specified operation. If ``aggregate_by`` is passed without a 
``group_by`` parameter, the aggregation is performed over the entire result set. Results that have been 
aggregated are returned in an aggregated format, not the typical reporting format. ::

  ?date_range={date_field}*{start_date}*{end_date}

``date_range`` filters results and leaves only those with the specified field falling between ``start_date`` 
and ``end_date``. ::

  ?date_group={date_field}*{time_increment}&?aggregate_by={aggregation_operator}*{aggregation_field}

``date_group`` functions equivalently to ``group_by``, except the groups are formed based on the values of the 
specified date field. For example, if the date field was 'date_measured', and the time increment was 'month', 
results would be returned grouped by the month of the date_measured field for each item. As with ``group_by``, 
``date_group`` must be used with an aggregator, and results are returned in an aggregated format. ::

  ?{FIELD}={VALUE}

This syntax adds additional filters to the query, returning only results having whose value for the property 
specified by 'field' matches 'value'.

For each of these parameters, acceptable values for ``{field}`` are specified individually by the calls. A 
full listing of the minimal reporting fields, along with valid aggregation operators and date increments, 
may be found :doc:`here <query-api>`.

External IDs
^^^^^^^^^^^^

When a resource is created, the Indivo API offers the ability to create this resource using a ``PUT`` with an 
``external_id`` in the URL, so that the call is idempotent: if a failure occurs, the call can be repeated safely 
and only the resource will not be created on the second call if it was already created successfully during 
the first call.

An ``external_id`` is only valid within a particular PHA scope. Other PHAs cannot see the external_id of a given 
document if they didn't create the document, and certainly cannot access the document by external_id.

Some API calls which involve both creating documents and retrieving them, such as:

:http:put:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL_TYPE}/external/{APP_ID}/{EXTERNAL_ID}`

For these calls, it can be confusing as to which document is referenced by an 
external id. In such cases, the following rule resolves confusion:

* The newly created document will always be assigned the passed ``external_id``.
  The ``external_id`` will not be used to look up the existing document.

Managing Records and Documents
------------------------------

Data stored in Indivo cannot by permanently deleted by default: the API enforces only appending data, not fully 
replacing it or removing it.

Available Records
^^^^^^^^^^^^^^^^^

:http:get:`/accounts/{ACCOUNT_EMAIL}/records/`

::

  <Records account="joe@smith.org">
    <Record id="b43810b8-1ff0-11de-b090-001b63948875" label="Joe Smith" />
    <Record id="c002aa8e-1ff0-11de-b090-001b63948875" label="Jill Smith" />
  </Records>

supports paging, order by: label.

Single Record
^^^^^^^^^^^^^

:http:get:`/records/{RECORD_ID}`


::

  <Record id="c002aa8e-1ff0-11de-b090-001b63948875" label="Jill Smith">
    <contact document_id="83nvb-038xcc-98xcv-234234325235" />
    <demographics document_id="646937a0-1ff1-11de-b090-001b63948875" />
  </Record>

Applications attached to a Record
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:get:`/records/{RECORD_ID}/apps/`

::

  <Apps>
    <App id="f6fb1c56-1ff0-11de-b090-001b63948875">
      <startURL>http://example.org/app/start</startURL>
      <name>Medical Surveys</name>
      <frameable>false</frameable>
    </App>

    <App id="3c726d0c-1ff1-11de-b090-001b63948875">
      <startURL>http://example2.org/app/start</startURL>
      <name>Flu Tracker</name>
      <frameable>true</frameable>
    </App>
  </Apps>

supports paging, order by: name.

Documents within a Record
^^^^^^^^^^^^^^^^^^^^^^^^^

:http:get:`/records/{RECORD_ID}/documents/`

:http:get:`/carenets/{CARENET_ID}/documents/`

::

  <Documents record_id="646937a0-1ff1-11de-b090-001b63948875"
   	     xmlns:indivo="http://indivohealth.org/xml/doctypes/" type="indivo:Medication">
    <Document id="ac21fe42-1ff1-11de-b090-001b63948875">
      <.. document metadata fields ..>
    </Document>
  </Documents>

supports paging, order by document metadata fields
(see :doc:`Indivo Document Metadata Schema <schemas/metadata-schema>`).

by Type
"""""""

The calls to :http:get:`/records/{RECORD_ID}/documents/` and 
:http:get:`/carenets/{CARENET_ID}/documents/` take a ``type`` querystring 
parameter, which filters the list of returned documents by their types.

A document's ``type`` is (by default) the suffix of a URL that corresponds to 
the XML schema datatype, where the prefix is 
``http://indivo.org/vocab/xml/documents#``. Thus, type can be Medication, Lab, 
etc.

Indivo X supports storing XML documents whose datatype is not among the default 
Indivo X recommended types. In those cases, if the XML schema namespace doesn't 
end in a ``/`` or ``#``, then as is typical in the XML/RDF community, a ``#`` 
is used as delimiter in the URI. Examples of document types include:

* ``http://indivo.org/xml/phr/medication#Medication`` (Indivo 3.1 data type)

* ``urn:astm-org:CCR#ContinuityOfCareRecord``, as per 
  http://code.google.com/apis/health/ccrg_reference.html

Single Document
^^^^^^^^^^^^^^^

:http:get:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}`

:http:get:`/carenets/{CARENET_ID}/documents/{DOCUMENT_ID}`

::

  { Indivo Document Content }

Special Documents
^^^^^^^^^^^^^^^^^

The Demographics and Contact documents are special in that there should only be 
one of each per record, and they should be easy to find.

.. seealso::

   :doc:`Indivo Document Demographics Schema<schemas/demographics-schema>`
     The XML Schema for Indivo Demographics Data

   :doc:`Indivo Document Contact Schema<schemas/contact-schema>`
     The XML Schema for Indivo Contact Data

Reading Special Documents
"""""""""""""""""""""""""

:http:get:`/records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}`

:http:get:`/carenets/{CARENET_ID}/documents/special/{SPECIAL_DOCUMENT}`

::

  { Special Document }

Updating Special Documents
""""""""""""""""""""""""""

:http:put:`/records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}`

::

  ADD_FORM_PARAMS
  { Indivo Document Metadata for the new Special document }

Document Metadata
^^^^^^^^^^^^^^^^^

:http:get:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/meta`

:http:get:`/carenets/{CARENET_ID}/documents/{DOCUMENT_ID}/meta`

::

  <Document id="ac21fe42-1ff1-11de-b090-001b63948875">
    <disabledAt />
    <lastModifiedAt>2009-04-06 13:34:23</lastModifiedAt>
  </Document>

by External ID
""""""""""""""

:http:get:`/records/{RECORD_ID}/documents/external/{APP_ID}/{EXTERNAL_ID}/meta`

Document Versions
^^^^^^^^^^^^^^^^^

:http:get:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/versions/`

::

  <Documents original_id="ac21fe42-1ff1-11de-b090-001b63948875">
    <Document id="cb31fe32-1ee1-21de-c190-041b66935866">
      <.. DOC METADATA ..>
    </Document>
    <Document id="b321ee42-1fc5-12ee-b530-051b43948378">
      <.. DOC METADATA ..>
    </Document>
  </Documents>

Document Creation
^^^^^^^^^^^^^^^^^

:http:post:`/records/{RECORD_ID}/documents/`

::

  ADD_FORM_DATA
  <Document id="ac21fe42-1ff1-11de-b090-001b63948875" />

by External ID
""""""""""""""

:http:put:`/records/{RECORD_ID}/documents/external/{APP_ID}/{EXTERNAL_ID}`

ADD_FORM_DATA

Medical data cannot be replaced wholesale, only versioned. Thus, this call will 
fail (with a :http:statuscode:`409` error code) if a document already exists in 
the given record with given external ID and app ID.

Document Metadata Update
^^^^^^^^^^^^^^^^^^^^^^^^

Only the label on a document can be updated.

:http:put:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/label`

ADD_FORM_DATA{new_document_label}

::
  
  <OK />

by External ID
""""""""""""""

:http:put:`/records/{RECORD_ID}/documents/external/{APP_ID}/{EXTERNAL_ID}/label`

ADD_FORM_DATA {new_document_label}

::
  
  <OK />

Document Replacement
^^^^^^^^^^^^^^^^^^^^

This call replaces one document with a new document content. The existing 
document remains, but is marked suppressed and replaced by the new document.

:http:post:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/replace`

ADD_FORM_DATA {indivo_document_content}

::

  <Document id="e24a3b0e-1ff3-11de-b090-001b63948875">
    <.. DOC METADATA ..>
  </Document>

by external ID
""""""""""""""

:http:put:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/replace/external/{APP_ID}/{EXTERNAL_ID}`

ADD_FORM_DATA {indivo_document_content}

Medical data cannot be replaced wholesale, only versioned. Thus, this call will 
fail (with a :http:statuscode:`409` error code) if a document already exists 
in the given record with given external ID and app ID.

Document Removal and Archival
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generally, documents in Indivo cannot be removed, they can only be versioned. 
However, mistakes happen, and Indivo must deal with these somehow. Also, 
information eventually is out of date or no longer relevant.

All of the following actions are encoded in the Indivo API as changes to document 
status. The following call will change the status of a document:

:http:post:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/set-status`

ADD_FORM_DATA: reason={reason}&status=archived|void|...

Voiding a document
""""""""""""""""""

If a document is entered in error, it can be marked as voided to indicate 
that the data is invalid, by calling 
:http:post:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/set-status` with a 
status argument of ``void``.

Only active documents can be voided. Voided documents are still reachable, 
but their metadata indicates their status, and by default they are not listed 
in typical document listings.

A document can be "unvoided" if the voiding was performed in by resetting the 
status to ``active`` using 
:http:post:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/set-status`.

Archiving a document
""""""""""""""""""""

If a document is no longer relevant, it can be archived so that it doesn't show 
up by default. Archival is different from voiding in that an archived document is 
still considered medically correct, just not particularly relevant anymore.

As with voiding, archiving involves a call to 
:http:post:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/set-status`. Pass 
``archived`` as the argument for status.

Archived documents are still reachable, but their metadata indicates their 
archival status, and by default they are not listed in typical document listings.

A document can be "unarchived" if it becomes relevant again, if the archival was 
in error, etc. As with voiding, use 
:http:post:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/set-status` to set the
status to ``active``.

Document Status History
"""""""""""""""""""""""

A document can be voided, unvoided, archived, unarchived a number of times. The 
status change applies to entire version lineage of a document. The history of 
statuses, in reverse chronological order, can be obtained using the API call:

:http:get:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/status-history`

:: 
  
  <DocumentStatusHistory document_id="{document_id}">
    <DocumentStatus by="{principal}" at="{timestamp}" status="{new_status}">
      <reason>{reason}</reason>
    </DocumentStatus>
    <DocumentStatus by="{principal}" at="{timestamp}" status="{new_status}">
      <reason>{reason}</reason>
    </DocumentStatus>
    ...
  </DocumentStatusHistory>

Relating Documents
^^^^^^^^^^^^^^^^^^

It is often useful to relate documents, e.g. annotating a document, re-filling a 
prescription, connecting diagnoses to an encounter, etc. In Indivo X, these 
relations can be declared no matter the data type of the underlying document. An 
image of an X-ray might be related to an XML document that interprets it, but of 
course there is no room in the image file for a pointer. So all references are 
stored externally to the documents.

Relationship types are taken from a fixed list, including:

* interpretation
* annotation
* followup

Eventually, full URLs will be supported for relationship types. The fixed list of 
types will then correspond to ``http://indivo.org/vocab/documentrels#{rel_type}``.

In the following calls, ``{DOCUMENT_ID}`` is the document being interpreted, and 
``{OTHER_DOCUMENT_ID}`` or the ``POST`` content is the interpretation.

:http:put:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL_TYPE}/{OTHER_DOCUMENT_ID}`

:http:post:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL_TYPE}/`

ADD POST DATA: {INDIVO DOCUMENT CONTENT}

by external ID
""""""""""""""

:http:put:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL_TYPE}/external/{APP_ID}/{EXTERNAL_ID}`

ADD POST DATA: {INDIVO DOCUMENT CONTENT}

Medical data cannot be replaced wholesale, only versioned. Thus, this call will 
fail (with a :http:statuscode:`409` error code) if a document already exists in 
the given record with given external ID and app ID.

retrieving related documents
""""""""""""""""""""""""""""

In the following calls, ``{DOCUMENT_ID}`` is the interpreted document, and the 
calls return all interpretations (that are of type ``{REL_TYPE}``) of that 
document.

:http:get:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL_TYPE}/`

::

  <Documents record_id="646937a0-1ff1-11de-b090-001b63948875"
       xmlns:indivo="http://indivohealth.org/xml/doctypes/" related_to="2098ecea-23a3-11de-b4e2-001b63948875"
       relationship="http://indivo.org/vocab/documentrels#annotation">
    <Document id="ac21fe42-1ff1-11de-b090-001b63948875">
      <disabledAt />
      <lastModifiedAt>2009-04-06 13:34:23</lastModifiedAt>
    </Document>
  </Documents>

Messaging and Notifications
---------------------------

Read Messages in Account
^^^^^^^^^^^^^^^^^^^^^^^^

:http:get:`/accounts/{ACCOUNT_ID}/inbox/`

ADD QUERY_PARAMS: ?include_archive={1|0}

ADD DESCRIPTION: returns a list of messages. Schema defined in Indivo Inbox Message Schema.
By default, only non-archived messages are returned.

Read Single Message in Account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:get:`/accounts/{ACCOUNT_ID}/inbox/{MESSAGE_ID}`

ADD DESCRIPTION: returns a single message. Schema defined in Indivo Inbox Message Schema.

Archive a Message
^^^^^^^^^^^^^^^^^

:http:post:`/accounts/{ACCOUNT_ID}/inbox/{MESSAGE_ID}/archive`

Accept a Message Attachment into Record
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A user can accept an attachment from a message into their medical record.

:http:post:`/accounts/{ACCOUNT_ID}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}/accept`

Send a Message to an Account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:post:`/accounts/{ACCOUNT_ID}/inbox/`

ADD_QUERY_PARAMS: subject={subject}&body={body}&severity={severity}

Severity need not be included. If it is included, it can be low, medium, or high.

Send a Message to a Record
^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:post:`/records/{RECORD_ID}/inbox/{MESSAGE_ID}`

ADD_QUERY_PARAMS: subject={subject}&body={body}&severity={severity}&num_attachments={num_attachments}

Messages to records can have attached documents (specified by the 
``num_attachements`` parameter) which then need to be uploaded separately (the 
message isn't delivered until all of its attachments are uploaded).

Upload attachments with:

:http:post:`/records/{RECORD_ID}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}`

ADD_POST_DATA: {INDIVO_DOCUMENT}

ADD_URL_PARAM:The attachment_num URL parameter is a 1-indexed integer that represents the order 
of the attachment. It cannot be larger than ``num_attachments`` that was declared.

Send a Notification to a Record
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:post:`/records/{RECORD_ID}/notifications/`

ADD_FORM_DATA: content={notification_content}&app_url={relative_url}&document_id={document_id}

Application-Specific Storage
----------------------------

Application-specific storage is meant for bookkeeping by individual applications 
that is not specific to any given record. These documents can be deleted, since 
they are not part of any permanent medical record. All application-specific 
storage API calls behave like the prior document API calls, though the documents 
are accessible only to the application in question. Most implementations of the 
Indivo API will likely impose a quota on Applications to ensure they do not store 
large amounts of data in the application-specific storage. This quota may be 
application-specific, depending on what the application is approved to do.

Application-specific storage calls, since they don't correspond to any given 
record, are all 2-legged oAuth calls.

Application-Specific Document List
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:get:`/apps/{APP_ID}/documents/`

supports paging, order by document metadata fields
(see :doc:`Indivo Document Metadata Schema <schemas/metadata-schema>`).

Application-Specific Single Document
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:get:`/apps/{APP_ID}/documents/{DOCUMENT_ID}`

Application-Specific Document Metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:get:`/apps/{APP_ID}/documents/{DOCUMENT_ID}/meta`

by External ID
""""""""""""""

:http:get:`/apps/{APP_ID}/documents/external/{EXTERNAL_ID}/meta`

(Note: no need to put the ``APP_ID`` twice in the URL, once to identify the app,
and once to scope the external_id.)

Application-Specific Document Creation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:post:`/apps/{APP_ID}/documents/`

ADD_POST_DATA: {INDIVO_DOCUMENT_CONTENT}

by External ID
""""""""""""""

:http:put:`/apps/{APP_ID}/documents/external/{EXTERNAL_ID}`

ADD_POST_DATA: {indivo_document}

As this is application-level storage, this will replace any existing document that 
existed beforehand.

Application-Specific Document Label Update
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:put:`/apps/{APP_ID}/documents/{DOCUMENT_ID}/label`

ADD_POST_DATA: {document_label}

Record-Application-Specific Storage
-----------------------------------

Record-application-specific storage is meant for bookkeeping by individual 
applications. These documents can be deleted, since they are not part of the 
permanent medical record. All record-application-specific storage API calls behave 
like the prior document API calls, though the documents are accessible only to the 
application in question. Most implementations of the Indivo API will likely impose 
a quota on Applications to ensure they do not store large amounts of data in the 
record-application-specific storage. This quota may be application-specific, 
depending on what the application is approved to do.

Record-Application-specific storage calls are all 3-legged oAuth calls.

Record-Application-Specific Document List
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:get:`/records/{RECORD_ID}/apps/{APP_ID}/documents/`

supports paging, order by document metadata fields
(see :doc:`Indivo Document Metadata Schema <schemas/metadata-schema>`).

Record-Application-Specific Single Document
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:get:`/records/{RECORD_ID}/apps/{APP_ID}/documents/{DOCUMENT_ID}`

Record-Application-Specific Document Metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:get:`/records/{RECORD_ID}/apps/{APP_ID}/documents/{DOCUMENT_ID}/meta`

by External ID
""""""""""""""

:http:get:`/records/{RECORD_ID}/apps/{APP_ID}/documents/external/{EXTERNAL_ID}/meta`

(Note: no need to put the ``APP_ID`` twice in the URL, once to identify the app,
and once to scope the external_id.)

Record-Application-Specific Document Creation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:post:`/records/{RECORD_ID}/apps/{APP_ID}/documents/`

ADD_POST_DATA: {INDIVO_DOCUMENT_CONTENT}

by External ID
""""""""""""""

:http:put:`/records/{RECORD_ID}/apps/{APP_ID}/documents/external/{EXTERNAL_ID}`

ADD_POST_DATA: {INDIVO_DOCUMENT_CONTENT}

Record-Application-Specific Document Label Update
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:put:`/records/{RECORD_ID}/apps/{APP_ID}/documents/{DOCUMENT_ID}/label`

ADD_POST_DATA: {document_label}

Record-Application-Specific Document Deletion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:delete:`/records/{RECORD_ID}/apps/{APP_ID}/documents/{DOCUMENT_ID}`

.. _processed-reports:

Processed Medical Reports
-------------------------

Indivo processes documents into medical reports. Each report can be altered by the 
basic paging mechanism or the more complex query interface described above. Over 
time, new reports may be introduced. For now, we define these as the minimal set 
of reports. Fields supported by individual reports for the querying interface may 
be found :ref:`here <valid-query-fields>`. Response formats correspond to the 
:doc:`schemas/reporting-schema`, and individual reports fit their individual 
datatype's schema (see :ref:`medical-schemas`)

Measurements
^^^^^^^^^^^^

:http:get:`/records/{RECORD_ID}/reports/minimal/measurements/{LAB_CODE}/`

:http:get:`/carenets/{CARENET_ID}/reports/minimal/measurements/{LAB_CODE}/`

Medications
^^^^^^^^^^^

:http:get:`/records/{RECORD_ID}/reports/minimal/medications/`

:http:get:`/carenets/{CARENET_ID}/reports/minimal/medications/`

Allergies
^^^^^^^^^

:http:get:`/records/{RECORD_ID}/reports/minimal/allergies/`

:http:get:`/carenets/{CARENET_ID}/reports/minimal/allergies/`

Equipment
^^^^^^^^^

:http:get:`/records/{RECORD_ID}/reports/minimal/equipment/`

:http:get:`/carenets/{CARENET_ID}/reports/minimal/equipment/`

Immunizations
^^^^^^^^^^^^^

:http:get:`/records/{RECORD_ID}/reports/minimal/immunizations/`

:http:get:`/carenets/{CARENET_ID}/reports/minimal/immunizations/`

Procedures
^^^^^^^^^^

:http:get:`/records/{RECORD_ID}/reports/minimal/procedures/`

:http:get:`/carenets/{CARENET_ID}/reports/minimal/procedures/`

Problems
^^^^^^^^

:http:get:`/records/{RECORD_ID}/reports/minimal/problems/`

:http:get:`/carenets/{CARENET_ID}/reports/minimal/problems/`

Vitals
^^^^^^

:http:get:`/records/{RECORD_ID}/reports/minimal/vitals/`

:http:get:`/carenets/{CARENET_ID}/reports/minimal/vitals/`

Labs
^^^^

:http:get:`/records/{RECORD_ID}/reports/minimal/labs/`

:http:get:`/carenets/{CARENET_ID}/reports/minimal/labs/`

Simple Clinical Note
^^^^^^^^^^^^^^^^^^^^

:http:get:`/records/{RECORD_ID}/reports/minimal/simple-clinical-notes/`

:http:get:`/carenets/{CARENET_ID}/reports/minimal/simple-clinical-notes/`

Coding Systems
--------------

A number of Indivo documents contain coded values. These can be based on UMLS, 
SNOMED, etc. Indivo provides a generic API for looking up coded values. This API 
is particularly built to support live autocomplete in JavaScript.

List Coding Systems
^^^^^^^^^^^^^^^^^^^

:http:get:`/codes/systems/`

returns a JSON list of coding systems::

  [{'short_name': 'umls-snomed', 'name': 'UMLS SNOMED', 'description' : '...'},
   {..},
   {..}]

Search Coding System
^^^^^^^^^^^^^^^^^^^^

:http:get:`/codes/systems/{SHORT_NAME}/query`

MOVE THE QUERY TO A QUERYSTRING DESCRIPTION!! ?q={QUERY}

query the coding system with the given text. Returns a JSON list of terms::

  [{"abbreviation": null, "code": "38341003", "consumer_value": null, 
    "umls_code": "C0020538", 
    "full_value": "Hypertensive disorder, systemic arterial (disorder)"},
   {"abbreviation": null, "code": "55822004", "consumer_value": null, 
    "umls_code": "C0020473", "full_value": "Hyperlipidemia (disorder)"}]

Administrative API
------------------

Account Information
^^^^^^^^^^^^^^^^^^^

:http:get:`/accounts/{ACCOUNT_ID}`

The account_id must be in the form of an email address. This call returns 
information about the account::

  <Account id="ben@indivo.org">
    <secret>671468</secret>
    <fullName>Ben Adida</fullName>
    <contactEmail>ben@adida.net</contactEmail>
    <lastLoginAt>2009-12-11T06:29:11.556286+00:00</lastLoginAt>
    <totalLoginCount>5</totalLoginCount>
    <failedLoginCount>0</failedLoginCount>
    <state>active</state>
    <lastStateChange>2009-12-11T14:22:04.453416+00:00</lastStateChange>
    <authSystem name="password" username="joesmith" />
  </Account>

The possible account states are:

* ``uninitialized``: an account that has been created by an administrative 
  application and has not been activated by the user yet (with their confirmation 
  URL and code).

* ``active``: a normal active account.

* ``disabled``: an account locked because too many failed login attempts.

* ``retired``: an account that is no longer in use.

Account Query
^^^^^^^^^^^^^

This API call searches for accounts using a few parameters:

:http:get:`/accounts/search`

ADD_QUERY_STRING: ?fullname={fullname}&contact_email={contact_email}

::

  <Accounts>
    <Account id="ben@indivo.org">
      <secret>671468</secret>
      <fullName>Ben Adida</fullName>
      <contactEmail>ben@adida.net</contactEmail>
      <lastLoginAt>2009-12-11T06:29:11.556286+00:00</lastLoginAt>
      <totalLoginCount>5</totalLoginCount>
      <failedLoginCount>0</failedLoginCount>
      <state>ok</state>
      <lastStateChange>2009-12-11T14:22:04.453416+00:00</lastStateChange>
      <authSystem name="password" username="joesmith" />
    </Account>
  
    <Account>
    
      ....
    
    </Account>

    ...
  
  </Accounts>

Account Creation and Maintenance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:post:`/accounts/`

ADD_FORM_DATA:
account_id={account_id}&contact_email={contact_email}&full_name={full_name}&
primary_secret_p={0|1}&secondary_secret_p={0|1}
The account_id must be in the form of an email address.

The primary and secondary secret arguments are optional and are used for helping 
the user initialize their account securely. A primary secret is sent directly by 
Indivo X server to the user at their ``ACCOUNT_ID`` email address in the form of 
a URL with an embedded secret. A secondary secret is generated by Indivo X and 
made available to the admin application using the /secret API call for the account.
If it is asked for in this call, it is required at account activation time right 
after the user clicks on the activation URL (aka the primary secret). A secondary 
secret makes sense only if a primary secret is also requested. That's why it's 
called "secondary."

::

  <Account id="max@adida.net">
    <secret>671468</secret>
    <fullName>Joe Smith</fullName>
    <contactEmail>joe@smith.net</contactEmail>
    <lastLoginAt>2009-12-11T06:29:11.556286+00:00</lastLoginAt>
    <totalLoginCount>0</totalLoginCount>
    <failedLoginCount>0</failedLoginCount>
    <state>uninitialized</state>
    <lastStateChange>2009-12-11T14:22:04.453416+00:00</lastStateChange>
    <authSystem name="password" username="joesmith" />
  </Account>

Setting a Username and Password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Accounts initially have no "authentication systems" attached to them. Over time, 
Indivo accounts will be usable with OpenID and other authentication systems. An 
account needs to enabled for each authentication system that we want to use for 
that account. The default system is "password". Setting up the password and the 
associated username is done as follows:

:http:post:`/accounts/{ACCOUNT_ID}/authsystems/`

ADD_QUERY_STRING: system=password&username={username}&password={password}

Resending Initialization URL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The email sent to initialize an account may get lost. This API call resends the 
email.

:http:post:`/accounts/{ACCOUNT_ID}/secret-resend`

Resetting an Account
^^^^^^^^^^^^^^^^^^^^

If a password is forgotten, the solution is to reset the account and email the 
user as with their initialization email. This will prevent logins until the new 
initialization URL is clicked, and the new password is entered.

This could be accomplished with separate calls to 
:http:post:`/accounts/{ACCOUNT_ID}/reset`, which sets the account state to
``uninitialized`` and resets the account secrets, and
:http:post:`/accounts/{ACCOUNT_ID}/secret-resend`, but for efficiency's sake 
there exists a combined call:

:http:post:`/accounts/{ACCOUNT_ID}/forgot-password`

which does both of the above.

Note that this call resets both the primary and secondary secrets. The user will 
need to be given this secondary secret in a channel other than email. If a
User Interface Application performed this reset, then the secondary secret should 
display on screen while the primary secret is automatically sent by email. The 
user interface could obtain the secondary secret (which is short) by calling 
:http:get:`/accounts/{ACCOUNT_ID}/secret`, but the call to 
:http:post:`/accounts/{ACCOUNT_ID}/forgot-password` returns the secondary secret
to avoid the extra call.

Iniitalizing an Account
^^^^^^^^^^^^^^^^^^^^^^^

Initializing an account that has been reset requires both the primary and 
secondary secrets. The primary secret is sent in the URL, and the secondary secret 
should be collected by the user interface. Specifically, the recommended process 
is:

* Indivo Backend server sends the reinitialization URL to the user as:
  
  :file:`{INDIVO_UI_APP_LOCATION}/account/initialize/{account_id}/{primary_secret}`

* An Indivo UI App checks that the requested account is indeed in uninitialized 
  state and prompts the user for his secondary secret (which the user knows simply 
  as the "secret") and his new password.

* The Indivo UI App initializes the account:

  :http:post:`/accounts/{ACCOUNT_ID}/initialize/{PRIMARY_SECRET}`

  ADD_POST_DATA:secondary_secret={secondary_secret}

* The Indivo UI app sets the password to the new value provided by the user using 

  :http:post:`/accounts/{ACCOUNT_ID}/authsystems/password/set`

Setting Account State
^^^^^^^^^^^^^^^^^^^^^

The state of an account can be changed by an admin call:

:http:post:`/accounts/{ACCOUNT_ID}/set-state`

ADD_POST_DATA: state={new_state}

Setting a Password
^^^^^^^^^^^^^^^^^^

The UI App can change a user's password forcefully:

:http:post:`/accounts/{ACCOUNT_ID}/authsystems/password/set`

ADD_POST_DATA: password={password}

This should be used only in the context of an account reinitialization.

Changing a Password
^^^^^^^^^^^^^^^^^^^

A user can change his password, which the Chrome client can achieve by making this 
API call. The old password must be correct for this change to succeed.

:http:post:`/accounts/{ACCOUNT_ID}/authsystems/password/change`

ADD_POST_DATA: old={old_password]&new={new_password}

Account Secrets
^^^^^^^^^^^^^^^

This should be used very sparingly as the primary secret should rarely be seen 
outside of the Indivo backend.

:http:get:`/accounts/{ACCOUNT_ID}/primary-secret`

::

  <secret>{secret}</secret>

Record Creation
^^^^^^^^^^^^^^^

:http:post:`/records/`

ADD_POST_DATA: {CONTACT_DOCUMENT}

::

  <Record id="" label="Joe Smith">
    <contact document_id="" />
    <demographics document_id="" />
  </Record>

by external ID
""""""""""""""

:http:put:`/records/external/{APP_ID}/{EXTERNAL_ID}`

ADD_POST_DATA: {CONTACT_DOCUMENT}

Set Record Owner
^^^^^^^^^^^^^^^^

:http:put:`/records/{RECORD_ID}/owner`

ADD_POST_DATA:{ACCOUNT_ID}

Prime a Record with a User App
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:post:`/records/{RECORD_ID}/apps/{APP_ID}/setup`

ADD_POST_DATA: {SETUP_DOCUMENT}

Removing a PHA from a Record
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:http:delete:`/records/{RECORD_ID}/apps/{APP_ID}`

Indivo Chrome / User Interface API
----------------------------------

These API calls are reserved for the UI server, which is deeply trusted to 
authorized other applications, proxy the user's credentials, etc. It's only a 
separate server for modularity, otherwise it has the same level of trust as the 
backend Indivo server.

Create a Session
^^^^^^^^^^^^^^^^

:http:post:`/oauth/internal/session_create`

ADD_POST_DATA: username={username}&password={password}
ADD_DESCRIPTION: Start a session for a user.
::

  oauth_token=<TOKEN>&
  oauth_token_secret=<SECRET>&
  account_id=<ACCOUNT_ID>&
  x_oauth_expiration_policy=usersession

Claim a Request Token
^^^^^^^^^^^^^^^^^^^^^

Before a request token can be viewed at all, it has to be claimed by a user. This 
ensures that a request token can't be partially used by one user and completed by 
another.

:http:post:`/oauth/internal/request_tokens/{REQUEST_TOKEN}/claim`

The session-based chrome authentication will indicate to the backend which Account 
to associate with this request token. Once this call has been made for a request 
token, a second call with different session authentication will fail. (A second 
call with the same user authentication will be just fine, we don't want a reload 
to cause a problem.)

If the request token is bound to an Indivo record (because the PHA knew it was 
authorizing for a given record), and the claimant does not have administrative 
rights over the record, this call will fail and the request token will be 
invalidated.

Retrieve Information about an oAuth request token
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When authorizing a request token, the Indivo UI needs to know what that token 
represents. Once the token is claimed, the request token yields information via 
the call:

:http:get:`/oauth/internal/request_tokens/{REQUEST_TOKEN}/info`

This can only be called with session authentication matching the Account which 
claimed the request token earlier.

This call returns an XML data structure with information about exactly what the 
app is and what it's asking the user::

  <RequestToken token="{REQUEST_TOKEN_STRING}" record_id="{RECORD_ID}">

    <kind>{REQUEST-KIND}</kind>

    <App id="surveys@apps.indivohealth.org">
      <name>Medical Surveys</name>
      <description>take surveys from home</description>
      <frameable>true</frameable>
      <ui>true</ui>
    </App>

    <Permissions>
      <.. description of requested permissions ..>
    </Permissions>

    <DataUsageAgreement>
      <.. data usage intent ..>
    </DataUsageAgreement>

  </RequestToken>

The ``record_id`` attribute on the ``RequestToken`` may be absent. It is present in
the case where the request token has been pre-bound to the record (because the app 
knows that it's trying to bind a given record). In that case, the Chrome UI should 
not give the user the option of attaching the app to a different record than the 
one prescribed.

If a ``record_id`` is present, then the kind element is also present and indicates:

* ``new``: a new request for a PHA that has not been authorized for this record yet

* ``same``: a request for a PHA that is already attached to the record and no new 
  permissions are requested

* ``upgrade``: a request for a PHA that is already attached to the record but 
  that is asking for more permissions or more permissive usage of the data.

In the ``same`` case, the Chrome UI is allowed to immediately approve the request 
token. In other cases, the Chrome UI must explain to the user that new permissions 
/ rights are being granted and prompt the user for approval.

Approve a Request Token
^^^^^^^^^^^^^^^^^^^^^^^

If a user approves an app addition, then the Chrome UI server needs to let the 
backend know.

:http:post:`/oauth/internal/request_tokens/{REQUEST_TOKEN}/approve`

ADD_POST_DATA: record_id={indivo_record_id}

This call, if it succeeds with a :http:statuscode:`200`, will return the location 
to which the user's browser should be redirected::

  location={url_to_redirect_to}

This call's session authentication must match that which claimed the request token.
The ``record_id`` is the record to which the user is attaching the application 
(i.e. my child's record, not my own.) If the request token was pre-bound to a 
record, this ``record_id`` parameter must match, or this will throw an error.

Retrieve and Update Account Info
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When an Indivo account is uninitialized, the Chrome application (which is THE user 
interface) must be able to check an account's status to provide the initialization 
screen.

Retrieving the account information can be done using a call to 
:http:get:`/accounts/{ACCOUNT_ID}` from above. Checking the primary and secondary
secrets can be done using:

:http:get:`/accounts/{ACCOUNT_ID}/check-secrets/{PRIMARY_SECRET}`

This will return a :http:statuscode:`200` if the secrets matched, and a 
:http:statuscode:`403` otherwise.

Then, to initialize the account, the Chrome app makes a call to 
:http:post:`/accounts/{ACCOUNT_ID}/initialize/{PRIMARY_SECRET}`

ADD_POST_DATA: secondary_secret={secondary_secret}

Verifying Signed URLs
^^^^^^^^^^^^^^^^^^^^^

In some cases, an Indivo app will sign a URL that directs the user to the Indivo 
Chrome. A prime example is the use of Indivo Chrome widgets, i.e. the Document 
Sharing widget, that apps can embed within their user interface to reuse 
functionality from Indivo Chrome. A signed URL looks like this::

  /widgets/WidgetName?param1=foo&param2=bar&surl_timestamp={TIMESTAMP}&surl_token={TOKEN}&surl_sig={SIGNATURE}

The signature contained in surl_sig is effectively a signature on the rest of the 
URL. The signature algorithm is as follows:

#. An app, with oAuth access token ``TOKEN`` and oAuth access token secret 
   ``SECRET``, wishes to sign a URL. 

#. The app generates the SURL secret that corresponds to this access token as 
   follows::

     <SURL_SECRET> = HMAC(<TOKEN_SECRET>, "SURL-SECRET")

   using base64 encoding, where the idea is to actually sign the string 
   "SURL-SECRET" to obtain the SURL secret itself.

#. this SURL secret is then used to sign the URL, first by appending a timestamp, 
   the SURL token, and then computing the signature::

     <SURL_SIG> = HMAC(<SURL_SECRET>, 
                       "/widgets/WidgeName?...&surl_timestamp=<TIMESTAMP>&surl_token=<TOKEN>")

   in base 64, then appending it as a query parameter surl_sig.

Indivo then provides an API for verifying such signed URLs:

:http:get:`/oauth/internal/surl-verify`

ADD_QUERY_PARAMS: ?url={url}

::

  <result>{ok|bad}</result>

where the URL parameter is URL-encoded, of course.

Sharing
-------

Overview
^^^^^^^^

We want to simplify sharing. Indivo has two main mechanisms for sharing patient
records with other accounts: :dfn:`Full Shares` and :dfn:`Carenets`. 

.. _full-share:

Full Share
  A user may choose to share the entirety of their record with another account. 
  The recipient account will then have access to all data (past, present, and 
  future) contained in the record, and will be able to run any apps that have
  been bound to the record. The recipient of a full share will also be able to
  add new applications to the record and run them against data in the record.

  Similarly, a user may choose to add an application to their full record. This
  effectively creates a 'full share' of the record with that application: the 
  app has access to all data in the record.

  As an example, a teen user of Indivo might choose to set up a full share of his /
  her record with a parent of guardian.

Carenet
  Full shares are not very flexible: they are an all or nothing proposition. In 
  cases where sharing data appropriately requires more granularity or complexity,
  Indivo provides **carenets**, which allow a record to specify groups of *accounts*
  and *apps* that all have transparent access to whatever *data* the record shares
  into the carenet.

  By default, each record will have 3 simple carenets: physicians, family, and 
  work/school.

  As an example, a patient might create an 'exercise' carenet, into which they 
  place:

  * *data*: blood-pressure readings, pedometer output, and other data associated
    with maintaining a healthy lifestyle.

  * *apps*: blood-pressure viewers, exercise-trackers, and other apps that help the
    patient organize and interact with their exercise data.

  * *accounts*: The patient's Primary Care Physician, personal trainer, friends, or
    any other person with an interest in helping the patient develop healthy 
    exercise habits.

  Now anyone on the *accounts* list can log into Indivo and run any app on the 
  *apps* list against any data on the *data* list.

  Data can be placed into carenets individually, or autoshared by Document type. 
  Users can override the type-auto-sharing on a document-by-document basis.

Making Other APIs Carenet-aware
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All document and reporting calls that can be made on :file:`/records/{{RECORD_ID}}`
can be made on :file:`/carenets/{{CARENET_ID}}`. For example:

List Documents by Type in a CareNet
"""""""""""""""""""""""""""""""""""

:http:get:`/carenets/{CARENET_ID}/documents/`

ADD_QUERY_PARAM: ?type={indivo_document_type_url}

Report in a CareNet
"""""""""""""""""""

:http:get:`/carenets/{CARENET_ID}/reports/minimal/immunizations/`

For more on reporting calls please see :ref:`processed-reports`.

List Carenets
"""""""""""""

A record owner can list the available carenets:

:http:get:`/records/{RECORD_ID}/carenets/`

Basic Record Info
"""""""""""""""""

A carenet user needs basic information about the record that the carenet belongs 
to, at least for the UI.

:http:get:`/carenets/{CARENET_ID}/record`

::

  <Record id="..." label="...">
  </Record>

Authorization into a CareNet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When an app is added, it is normally given, along with its oAuth token, an 
``xoauth_indivo_record_id`` that the token corresponds to. If the app is added to
a carenet instead of a record, the app will receive instead an 
``xoauth_indivo_carenet_id``.

Sharing API
^^^^^^^^^^^

Full Shares
"""""""""""

Entire records can be shared (see :ref:`above <full-share>`). The list of accounts 
with whom a record is shared can be obtained by calling:

:http:get:`/records/{RECORD_ID}/shares/`

::

  <Shares>
    <Share id="..." account="..." />
    <Share id="..." pha="..." />
  </Shares>

Note how some of these shares indicate sharing with an app when that app has been 
added to the record.

A new full-record share with an account can be created as follows:

:http:post:`/records/{RECORD_ID}/shares/`

ADD_POST_DATA: account_id={account_id}&role_label={role_label}

The role_label is currently nothing more than that: a label. The label will come 
back in the XML for ``<Shares>``

A share can then be removed using 
:http:delete:`/records/{RECORD_ID}/shares/{ACCOUNT_ID}`

Place a document in a carenet
"""""""""""""""""""""""""""""

:http:put:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}`

When a document is explicitly shared with a carenet, it is no longer tied to the 
auto-sharing rules for that carenet. However, auto-sharing rules with other 
carenets still apply.

Remove a document from a carenet
""""""""""""""""""""""""""""""""

:http:delete:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}`

When a document is explicitly **UN**\ shared from a carenet, it is no longer tied 
to the auto-sharing rules for that carenet. However, auto-sharing rules with other 
carenets still apply.

Revert a document to auto-share rules
"""""""""""""""""""""""""""""""""""""

:http:post:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}/autoshare-revert`

This means that, for this carenet, this document reverts to automatic sharing 
rules. This might mean a removal of the share with this carenet, or an addition, 
or no effect. However, from this point on, the record-wide rules apply.

List carenets where a document is present
"""""""""""""""""""""""""""""""""""""""""

:http:get:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/`

::

  <Carenets>
    <Carenet id=".." name="..." mode="explicit" />
    <Carenet id=".." name="..." mode="bytype"/>
    <Carenet id=".." name="..." mode="explicit" value="negative" />
  </Carenets>

The mode attribute indicates how this document is shared. explicit means that the 
sharing preferences for this document are explicitly set. bytype indicates that it 
was auto-shared by document type. Other modes may be enabled in the future.

The value attribute indicates a negative share with a carenet, meaning that the 
user explicitly wants this document not shared with this carenet, even if 
auto-share rules would otherwise share it. Obviously this only makes sense for 
explicit carenet-shares.

Never Share
"""""""""""

A user should be able to ask that a document be "never shared". This flag prevents 
any sharing, no matter what the auto-share rules may be.

:http:put:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/nevershare`

And the nevershare flag can be removed easily:

:http:delete:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/nevershare`

Get Auto-Sharing Preferences
""""""""""""""""""""""""""""

:http:get:`/records/{RECORD_ID}/autoshare/bytype/`

ADD_QUERY_STRING?type={INDIVO_document_type}

::

  <Carenets>
    <Carenet id=".." name="..." />
    <Carenet id=".." name="..." />
  </Carenets>

Documents of a certain type can be auto-shared, so that they are added to a 
carenet when they are added to the record. 

ADD_DESCRIPTION: This call lists the auto-sharing by 
document type.

Get All Auto-Sharing Preferences
""""""""""""""""""""""""""""""""

:http:get:`/records/{RECORD_ID}/autoshare/bytype/all`

::

  <DocumentSchemas>
    <DocumentSchema type="..">
      <Carenets>
        <Carenet id=".." name="..." />
        <Carenet id=".." name="..." />
      </Carenets>
    </DocumentSchema>
  </DocumentSchemas>

ADD_DESCRIPTION: This call lists all auto-sharing preferences.

Set Auto-Sharing Preferences
""""""""""""""""""""""""""""

:http:post:`/records/{RECORD_ID}/autoshare/carenets/{CARENET_ID}/bytype/set`

ADD_POST_DATA: type={indivo_document_type}

This sets the auto-share preferences for a type of document for a given carenet. 
These preferences apply to all documents that do not have an explicit sharing 
preference declared on them.

:http:post:`/records/{RECORD_ID}/autoshare/carenets/{CARENET_ID}/bytype/unset`

ADD_POST_DATA: type={indivo_document_type}

ADD_DESCRIPTION: This removes the auto-share preference for that doctype and that carenet.

Managing Carenets (more Sharing API)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users needs to be able to place apps and accounts inside carenets in addition to
documents. Apps are placed inside carenets when they are authorized. Users are 
placed in carenets more explicitly.

Listing Apps in a Carenet
"""""""""""""""""""""""""

:http:get:`/carenets/{CARENET_ID}/apps/`

Adding an App to a Carenet
""""""""""""""""""""""""""

:http:put:`/carenets/{CARENET_ID}/apps/{PHA_EMAIL}`

No read/write issues here, permissions are per-user at that point, this is just 
about whether the app is visible in the carenet at all.

Removing an App from a Carenet
""""""""""""""""""""""""""""""

:http:delete:`/carenets/{CARENET_ID}/apps/{PHA_EMAIL}`

Listing People in a Carenet
"""""""""""""""""""""""""""

:http:get:`/carenets/{CARENET_ID}/accounts/`

::

  <Accounts>
    <Account id="ben@indivo.org" write="true" />
    <Account id="friend@indivo.org" write="false" />
  </Accounts>

Adding a Person to a Carenet
""""""""""""""""""""""""""""

:http:post:`/carenets/{CARENET_ID}/accounts/`

ADD_POST_DATA: account_id={account_id}&write={false|true}

Removing a Person from a Carenet
""""""""""""""""""""""""""""""""

:http:delete:`/carenets/{CARENET_ID}/accounts/{ACCOUNT_ID}`

Checking One's Own Permissions
""""""""""""""""""""""""""""""

An app or a person may need to check what permissions it has in a given carenet.

:http:get:`/carenets/{CARENET_ID}/accounts/{ACCOUNT_ID}/permissions`

:http:get:`/carenets/{CARENET_ID}/apps/{APP_ID}/permissions`

In either case, the return value is::

  <Permissions>
    <DocumentType type="*" write="{true|false}" />
  </Permissions>

Note how the document type is always "*" for now, since an app or a person can see 
anything that lives in a given carenet, although we may eventually further limit 
this for apps. The "write" attribute determines whether the account or app has the 
ability to add data to the given carenet.

Apps and Carenets
^^^^^^^^^^^^^^^^^

Indivo apps are given a ``record_id`` and an access token that matches that record to 
read and write documents, read reports, annotate, etc.. In a sharing scenario, 
apps must become carenet-aware.

Requirements
""""""""""""

* An app should be easily placed within any number of carenets, i.e. physicians 
  and family, but not work/school.

* When an app is activated on a given record, it must have access to no more data 
  than the user who activated it. For example, if the owner selects the app, then 
  the app may have access to the entire record. If the owner's school nurse 
  activates the app, the nurse should have access to only the data that is in the 
  work/school carenet.

* There may be a need to further constrain an app, so that even if the owner 
  activates the app, it should not be able to see every data type, or may be 
  constrained to one of the carenets anyways. This is DEFERRED for now.

* We must not depend on app developers to properly partition information. If an 
  app is active in both the Family and Physicians carenets, and knows that the 
  ``record_id`` is the same in both cases, it may well intermix data without 
  realizing it. This would be bad. We need to make it harder for apps to hurt the 
  user.

Scenario
""""""""

Alice owns her Indivo record and has shared it with Bob, her HR representative at 
work, placing Bob in the "Work/School" carenet. Alice is pregnant but does not 
wish to reveal this information to her co-workers just yet. She has added the 
"Pregnancy Tracker" app to her record, making it visible to her Family and 
Physician carenets, but not to to her Work/School carenet. Alice has a history of 
depression, information which she has shared with her Physicians, but not with 
her Family.

**Visible Apps**

The "Pregnancy Tracker" app has been added to the Family and Physicians carenets, 
but not the Work/School carenet, so Bob cannot even see the application when he 
visits Alice's record. This is enforced by the Indivo platform itself.

**Activating and using an App**

Charlie, Alice's father, is eager to check up on his future grandchild's progress. 
He logs into Indivo, selects Alice's record. He sees "Pregnancy Tracker" because 
that app is visible to the Family carenet. He launches the app, and uses its 
functionality to track Alice's progress, her fetus's growth, her blood tests, etc. 
The process when launching the app is:

* Clicking on the app directs the IFRAME to the start_url for the pregnancy 
  tracker. The app must receive an indication of which record is being accessed 
  at this point. This cannot be the ``record_id`` alone, and we may not even want 
  to include the ``record_id`` at all, otherwise the app might confuse this data 
  with that accessible to Physicians later on. Thus, instead of passing 
  ``record_id`` to the IFRAME, Indivo passes only ``carenet_id``.

* The oAuth process begins with the ``carenet_id`` only as part of the request for 
  a request token.

* Indivo checks that the logged-in-user has the right to access this carenet, and 
  if so authorizes the token.

* The token is bound to that carenet only, and cannot be used on any other carenet.

* The app can make requests to

  :file:`/carenets/{{carenet_id}}/documents/{...}`

  without using the ``record_id`` at all. It doesn't need to know the 
  ``record_id``.

* When the app is later activated by a Physician, who does have access to Alice's 
  history of depression, the app gets a different ``carenet_id``, and from that 
  carenet has access to the documents including mental health.

* This is not fool-proof: we still probably need to give the app access to some 
  record information that will yield a unique identifier using the name, DoB, 
  etc... but at least the default behavior for the app will not allow error-prone 
  tracking across carenets.

oAuth Mechanics
"""""""""""""""

We start with:

* A CarenetAccount row that shares a record's carenet with another account

* A Share rowthat indicates that an app has access to the record

* A CarenetPHA row that makes the app available in the carenet.

The oAuth process is then:

* PHA requests a request token with a ``carenet_id`` instead of a ``record_id`` 
  as parameter.

* PHA needs to have a share into the record or into the specific carenet for this 
  to succeed.

* The request token needs to keep track of the carenet, because the Share might be 
  for the whole record.

* The user approving the request token should be in the carenet in question.

* The access token already stores the account of the person it's proxying for, so 
  that should be enough.

Auditing
--------

:http:get:`/records/{RECORD_ID}/audits/query/`

ADD_QUERY_STRING: ?{QUERY_PARAMETERS}

::

  <Audits></Audits>

ADD_DESCRIPTION: This call, valid as of Beta3, allows for general queries over the 
audit logs. The query is specified in the parameters via the :doc:`query-api`, 
and returns results in the style of Medical Reports.

All subsequent calls are deprecated, but maintained (for now) for backwards 
compatibility.

:http:get:`/records/{RECORD_ID}/audits/`

.. deprecated:: 1.0.0

::

  <Audits></Audits>

:http:get:`/records/{RECORD_ID}/audits/documents/{DOCUMENT_ID}/`

.. deprecated:: 1.0.0

::

   <Audits></Audits>

:http:get:`/records/{RECORD_ID}/audits/documents/{DOCUMENT_ID}/functions/{FUNCTION_NAME}/`

.. deprecated:: 1.0.0

::

  <Audits></Audits>

.. COMING SOON!!

   Data Usage Intent and Share Tracking
   ------------------------------------