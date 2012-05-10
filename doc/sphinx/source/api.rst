Indivo API
==========

The Indivo API provides an interface for Personal Health Applications to extend the functionality of the 
Indivo PCHR. The Indivo API abides by the REST design pattern: it is stateless, re-uses existing HTTP 
constructs such as caching, compression and content negotiation, and generally uses URLs to represent 
hierarchical resources, e.g. documents within a medical record.

This document provides an introduction to the API, with in-depth explanations of
related core Indivo concepts where applicable. For a full listing of all 
available Indivo API calls, see :doc:`api-reference`.

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

Managing Documents
------------------

Data stored in Indivo cannot by permanently deleted by default: the API enforces 
only appending data, not fully replacing it or removing it.

.. _reading-documents-API:

Reading Documents
^^^^^^^^^^^^^^^^^

.. glossary::

   :http:get:`/records/{RECORD_ID}/documents/`
   :http:get:`/carenets/{CARENET_ID}/documents/`
     List documents within a record. Supports order by document metadata fields
     (see :doc:`Indivo Document Metadata Schema <schemas/metadata-schema>`).
       
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

   :http:get:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}`
   :http:get:`/carenets/{CARENET_ID}/documents/{DOCUMENT_ID}`
     Fetch a single document.

   :http:get:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/meta`
   :http:get:`/carenets/{CARENET_ID}/documents/{DOCUMENT_ID}/meta`
   :http:get:`/records/{RECORD_ID}/documents/external/{APP_ID}/{EXTERNAL_ID}/meta`
     Fetch metadata about a single document, using its internal or external id.

   :http:get:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/versions/`
     List versions of a single document.

.. _api-writing-documents:

Writing Documents
^^^^^^^^^^^^^^^^^

.. glossary::

   :http:put:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/label`
   :http:put:`/records/{RECORD_ID}/documents/external/{APP_ID}/{EXTERNAL_ID}/label`
     Update a single document's label.

   :http:post:`/records/{RECORD_ID}/documents/`
   :http:put:`/records/{RECORD_ID}/documents/external/{APP_ID}/{EXTERNAL_ID}`
     Create a new document, and possibly assign it an external id.

     Medical data cannot be replaced wholesale, only versioned. Thus, this call 
     will fail (with a :http:statuscode:`400` error code) if a document already 
     exists in the given record with the given external ID.

   :http:post:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/replace`
   :http:put:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/replace/external/{APP_ID}/{EXTERNAL_ID}`
     Replace one document with a new document content. The existing document 
     remains, but is marked suppressed and replaced by the new document.

     Medical data cannot be replaced wholesale, only versioned. Thus, this call 
     will fail (with a :http:statuscode:`400` error code) if a document already 
     exists in the given record with the given external ID.

Removing and Archiving Documents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generally, documents in Indivo cannot be removed, they can only be versioned. 
However, mistakes happen, and Indivo must deal with these somehow. Also, 
information eventually is out of date or no longer relevant.

All such changes are encoded in the Indivo API as changes to document 
status. 

.. glossary::

   :http:post:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/set-status`
     Change the status of a document. The passed status defines what happens to 
     the specified document:

     * ``void``: If a document is entered in error, it can be marked as voided to 
       indicate that the data is invalid.

       Only active documents can be voided. Voided documents are still reachable, 
       but their metadata indicates their status, and by default they are not 
       listed in typical document listings.

     * ``archived``: If a document is no longer relevant, it can be archived so 
       that it doesn't show up by default. Archival is different from voiding in 
       that an archived document is still considered medically correct, just not 
       particularly relevant anymore.

       Archived documents are still reachable, but their metadata indicates their 
       archival status, and by default they are not listed in typical document 
       listings.

     * ``active``: An active document is readily usable and will appear in search
       lisings by default. Setting a document to active status will unvoid a voided
       document, or unarchive an archived document.

   :http:get:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/status-history`
     A document can be voided, unvoided, archived, unarchived any number of times. 
     The status change applies to the entire version lineage of a document. The 
     history of statuses, in reverse chronological order, can be obtained using 
     this call.

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

.. glossary::

   :http:put:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL_TYPE}/{OTHER_DOCUMENT_ID}`
     Create a new relationship of type ``REL_TYPE`` between the two passed 
     documents.

   :http:post:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL_TYPE}/`
   :http:put:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL_TYPE}/external/{APP_ID}/{EXTERNAL_ID}`
     Create a new document and immediately relate it to an existing document, 
     possibly assigning an external id to the newly created document.

     Medical data cannot be replaced wholesale, only versioned. Thus, this call 
     will fail (with a :http:statuscode:`400` error code) if a document already 
     exists in the given record with the given external ID.

   :http:get:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL_TYPE}/`
     List all documents related to the passed document by the relationship
     ``REL_TYPE``.

     ``DOCUMENT_ID`` is the interpreted document, and the calls return all 
     interpretations (that are of type ``REL_TYPE``) of that document.

Special Documents
^^^^^^^^^^^^^^^^^

The Demographics and Contact documents are special in that there should only be 
one of each per record, and they should be easy to find.

.. seealso::

   :doc:`Indivo Document Demographics Schema<schemas/demographics-schema>`
     The XML Schema for Indivo Demographics Data

   :doc:`Indivo Document Contact Schema<schemas/contact-schema>`
     The XML Schema for Indivo Contact Data

.. glossary::

   :http:get:`/records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}`
   :http:get:`/carenets/{CARENET_ID}/documents/special/{SPECIAL_DOCUMENT}`
     Fetch a special document from a carenet or record.

   :http:put:`/records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}`
     Update a special document.

Messaging and Notifications
---------------------------

Indivo supports a lightweight notification framework as well as a heavier message
inbox. For more information, see :doc:`messaging`.

Messaging
^^^^^^^^^

.. glossary::

   :http:get:`/accounts/{ACCOUNT_ID}/inbox/`
     List available messages. By default, only non-archived messages are returned.

   :http:get:`/accounts/{ACCOUNT_ID}/inbox/{MESSAGE_ID}`
     Fetch a single message.

   :http:post:`/accounts/{ACCOUNT_ID}/inbox/{MESSAGE_ID}/archive`
     Archive a message.

   :http:post:`/accounts/{ACCOUNT_ID}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}/accept`
     Accept a message attachment. A user can accept an attachment from a message 
     into their medical record. This creates a new document on their record 
     containing the contents of the attachment.

   :http:post:`/accounts/{ACCOUNT_ID}/inbox/`
     Send a message to an account.

   :http:post:`/records/{RECORD_ID}/inbox/{MESSAGE_ID}`
     Send a message to a record. Messages to records can have attached documents 
     (specified by the ``num_attachements`` parameter) which then need to be 
     uploaded separately. The message isn't delivered until all of its attachments 
     are uploaded.

     Since Accounts, not Records, are the users who log into the system to view
     messages, there is no way to view messages in a record's inbox. Rather, when
     a message is sent to a record, every account authorized to view the message
     is sent a copy of the message, which they can retrieve via their account 
     inbox.

   :http:post:`/records/{RECORD_ID}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}`
     Upload an attachment to a message.

Notifications
^^^^^^^^^^^^^

Notifications are intended to be a lightweight system for applications to alert
users of activity in the application. This is especially relevant for apps that 
use sharing functionality: an app might want to notify other users of the app 
about a given user's activity in it. UI apps should display these notifications
in a twitter-feed like interface (our reference UI call it the 'healthfeed').

.. glossary::

   :http:post:`/records/{RECORD_ID}/notifications/`
     Send a notification to a record. As with inbox messages, notifications are
     propogated to the accounts that are authorized to view the record.

   :http:get:`/accounts/{ACCOUNT_EMAIL}/notifications/`
     List available notifications.

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

.. glossary::

   :http:get:`/apps/{APP_ID}/documents/`
     List application-specific documents. Supports order by document metadata 
     fields (see :doc:`Indivo Document Metadata Schema <schemas/metadata-schema>`).

   :http:get:`/apps/{APP_ID}/documents/{DOCUMENT_ID}`
     Fetch a single application-specific document.
     
   :http:get:`/apps/{APP_ID}/documents/{DOCUMENT_ID}/meta`
   :http:get:`/apps/{APP_ID}/documents/external/{EXTERNAL_ID}/meta`
     Fetch metadata about a single application-specific document, by its internal
     or external id.

   :http:post:`/apps/{APP_ID}/documents/`
   :http:put:`/apps/{APP_ID}/documents/external/{EXTERNAL_ID}`
     Create an application-specific document, possibly assigning it an external id.
     
     As this is application-level storage, making this call with an external id 
     will overwrite any existing document with the same external id.

   :http:put:`/apps/{APP_ID}/documents/{DOCUMENT_ID}/label`
     Update the label of an application-specific document.

   :http:delete:`/apps/{APP_ID}/documents/{DOCUMENT_ID}`
     Delete an application-specific document. Since these documents do not
     contain medical data, deleting them is acceptable.

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

.. glossary::

   :http:get:`/records/{RECORD_ID}/apps/{APP_ID}/documents/`
     List record-application-specific documents. Supports order by document 
     metadata fields (see 
     :doc:`Indivo Document Metadata Schema <schemas/metadata-schema>`).

   :http:get:`/records/{RECORD_ID}/apps/{APP_ID}/documents/{DOCUMENT_ID}`
     Fetch a single record-application-specific document.
     
   :http:get:`/records/{RECORD_ID}/apps/{APP_ID}/documents/{DOCUMENT_ID}/meta`
   :http:get:`/records/{RECORD_ID}/apps/{APP_ID}/documents/external/{EXTERNAL_ID}/meta`
     Fetch metadata about a single record-application-specific document, by its 
     internal or external id.

   :http:post:`/records/{RECORD_ID}/apps/{APP_ID}/documents/`
   :http:put:`/records/{RECORD_ID}/apps/{APP_ID}/documents/external/{EXTERNAL_ID}`
     Create a record-application-specific document, possibly assigning it an 
     external id.
     
     As this is record-application-level storage, making this call with an 
     external id will overwrite any existing document with the same external id.

   :http:put:`/records/{RECORD_ID}/apps/{APP_ID}/documents/{DOCUMENT_ID}/label`
     Update the label of a record-application-specific document.

   :http:delete:`/records/{RECORD_ID}/apps/{APP_ID}/documents/{DOCUMENT_ID}`
     Delete a record-application-specific document. Since these documents do not
     contain medical data, deleting them is acceptable.

.. _processed-reports:

Processed Medical Reports
-------------------------

Indivo processes documents into medical reports. Each report can be altered by the 
basic paging mechanism or the more complex query interface described above. Over 
time, new reports may be introduced. For now, we define these as the minimal set 
of reports. Fields supported by individual reports for the querying interface may 
be found :ref:`here <valid-query-fields>`. Response formats correspond to the 
:doc:`schemas/reporting-schema`, and individual reports fit their individual 
datatype's schema (see :ref:`medical-schemas`). If a report is accessed via a 
carenet, only documents that are shared into the carenet will appear in the
results.

.. glossary::

   :http:get:`/records/{RECORD_ID}/reports/minimal/equipment/`
   :http:get:`/carenets/{CARENET_ID}/reports/minimal/equipment/`
     List equipment for a given record.

   :http:get:`/records/{RECORD_ID}/reports/minimal/immunizations/`
   :http:get:`/carenets/{CARENET_ID}/reports/minimal/immunizations/`
     List immunizations for a given record.

   :http:get:`/records/{RECORD_ID}/reports/minimal/labs/`
   :http:get:`/carenets/{CARENET_ID}/reports/minimal/labs/`
     List lab results for a given record.

   :http:get:`/records/{RECORD_ID}/reports/minimal/measurements/{LAB_CODE}/`
   :http:get:`/carenets/{CARENET_ID}/reports/minimal/measurements/{LAB_CODE}/`
     List measurements for a given record.

   :http:get:`/records/{RECORD_ID}/reports/minimal/procedures/`
   :http:get:`/carenets/{CARENET_ID}/reports/minimal/procedures/`
     List procedures for a given record.

   :http:get:`/records/{RECORD_ID}/reports/minimal/simple-clinical-notes/`
   :http:get:`/carenets/{CARENET_ID}/reports/minimal/simple-clinical-notes/`
     List clinical notes for a given record.

   :http:get:`/records/{RECORD_ID}/reports/minimal/vitals/`
   :http:get:`/carenets/{CARENET_ID}/reports/minimal/vitals/`
   :http:get:`/records/{RECORD_ID}/reports/minimal/vitals/{CATEGORY}/`
   :http:get:`/carenets/{CARENET_ID}/reports/minimal/vitals/{CATEGORY}`
     List vital signs for a given record.

SMART API Calls
---------------

As Indivo now supports the `SMART API <http://dev.smartplatforms.org/>`_, the following
calls are now available:

.. glossary::

   :http:get:`/records/{RECORD_ID}/allergies/`
     List a patient's Allergies as SMART RDF

   :http:get:`/records/{RECORD_ID}/encounters/`
     List a patient's Encounters as SMART RDF

   :http:get:`/records/{RECORD_ID}/medications/`
     List a patient's Medications as SMART RDF

   :http:get:`/records/{RECORD_ID}/problems/`
     List a patient's Problems as SMART RDF

   :http:get:`/apps/{APP_ID}/manifest`
   :http:get:`/apps/manifests/`
     Get SMART-style JSON manifests for one or all apps registered with this 
     instance of Indivo.

   :http:get:`/ontology`
     Get the ontology used by a SMART container
     
   :http:get:`/capabilities/`
     Get the SMART capabilities for this instance of Indivo.

Coding Systems
--------------

A number of Indivo documents contain coded values. These can be based on UMLS, 
SNOMED, etc. Indivo provides a generic API for looking up coded values. This API 
is particularly built to support live autocomplete in JavaScript.

.. glossary::
   
   :http:get:`/codes/systems/`
     List available coding systems. Return data is in JSON format.

   :http:get:`/codes/systems/{SHORT_NAME}/query`
     Search a coding system for a value.

Autonomous Apps API
-------------------
Autonomous user applications are unlike standard user apps in that they may not 
have a user interface, and require access to records without an active user 
session. In order to authenticate against Indivo on behalf of records at any 
time, autonomous apps may make the following calls:

.. glossary::

   :http:get:`/apps/{APP_ID}/records/`
     Return a list of records which have enabled the app, and to which (therefore)
     the app can authenticate and acquire access.

   :http:post:`/apps/{APP_ID}/records/{RECORD_ID}/access_token`
     Retrieve a valid access token providing the app with access to a record. This
     call will only succeed if the app is autonomous, and if the record has enabled
     the app.

     Using this call, an autonomous app can retrive a valid access token for any 
     record on which it is enabled, without an active user session.

Administrative API
------------------

Admin applications have access to Indivo's administrative API, which enables
control and setup of records and accounts.

Account Administration
^^^^^^^^^^^^^^^^^^^^^^

.. glossary::

   :http:get:`/accounts/{ACCOUNT_ID}`
     Get information about an account. The account_id must be in the form of an 
     email address.

   :http:get:`/accounts/search`
     Search for accounts by name or contact email.

   :http:get:`/accounts/{ACCOUNT_EMAIL}/records/`	
     List available records on an account. Supports order by ``label``.

   :http:post:`/accounts/`
     Create an account.

     The primary and secondary secret arguments are optional and are used for 
     helping the user initialize their account securely. A primary secret is sent 
     directly by Indivo X server to the user at their ``ACCOUNT_ID`` email address 
     in the form of a URL with an embedded secret. A secondary secret is generated 
     by Indivo X and made available to the admin application using the 
     :http:get:`/accounts/{ACCOUNT_ID}/secret` call for the account. If it is 
     asked for in this call, it is required at account activation time right after 
     the user clicks on the activation URL (aka the primary secret). A secondary 
     secret makes sense only if a primary secret is also requested. That's why 
     it's called "secondary."

   :http:post:`/accounts/{ACCOUNT_ID}/authsystems/`
     Add an authentication system to an account.

     Accounts initially have no "authentication systems" attached to them. 
     Over time, Indivo accounts will be usable with OpenID and other 
     authentication systems. An account needs to enabled for each authentication 
     system that we want to use for that account. The default system is 
     "password". Thus, this call, when used with the "password" system, 
     will set up the password and username for a new user.

   :http:post:`/accounts/{ACCOUNT_ID}/secret-resend`
     Resend an account's initialization URL (which contains the primary secret
     for the account). This is useful if the account holder loses the original
     email.

   :http:post:`/accounts/{ACCOUNT_ID}/forgot-password`
     Reset an account when its password is forgotten.

     If a password is forgotten, the solution is to reset the account and 
     email the user as with their initialization email. This will prevent logins 
     until the new initialization URL is clicked, and the new password is entered.

     This could be accomplished with separate calls to 
     :http:post:`/accounts/{ACCOUNT_ID}/reset`, which sets the account state to
     ``uninitialized`` and resets the account secrets, and
     :http:post:`/accounts/{ACCOUNT_ID}/secret-resend`, but this call combines
     both actions.

     Note that this call resets both the primary and secondary secrets. The 
     user will need to be given this secondary secret in a channel other than 
     email. If a User Interface Application performed this reset, then the 
     secondary secret should display on screen while the primary secret is 
     automatically sent by email. The user interface could obtain the secondary 
     secret (which is short) by calling :http:get:`/accounts/{ACCOUNT_ID}/secret`, 
     but the call to :http:post:`/accounts/{ACCOUNT_ID}/forgot-password` returns 
     the secondary secret to avoid the extra call.

   :http:post:`/accounts/{ACCOUNT_ID}/initialize/{PRIMARY_SECRET}`
     Initialize a new account.

     Initializing an account that has been reset requires both the primary and 
     secondary secrets. The primary secret is sent in the URL, and the secondary 
     secret should be collected by the user interface. Specifically, the 
     recommended process is:

     * Indivo Backend server sends the reinitialization URL to the user as:
  
       :file:`{INDIVO_UI_APP_LOCATION}/account/initialize/{account_id}/{primary_secret}`

     * An Indivo UI App checks that the requested account is indeed in 
       uninitialized state and prompts the user for his secondary secret (which 
       the user knows simply as the "secret") and his desired username and
       password.

     * The Indivo UI App initializes the account using this call.

     * The Indivo UI app sets up the account with the built-in password authsystem
       using the username/password provided by the user and the API call 
       :http:post:`/accounts/{ACCOUNT_ID}/authsystems/`.

   :http:post:`/accounts/{ACCOUNT_ID}/set-state`
     Set an account's state. Possible account states are:

     * ``uninitialized``: an account that has been created by an administrative 
       application and has not been activated by the user yet (with their 
       confirmation URL and code).

     * ``active``: a normal active account.

     * ``disabled``: an account locked because of too many failed login attempts.

     * ``retired``: an account that is no longer in use.

   :http:post:`/accounts/{ACCOUNT_ID}/authsystems/password/set`
     Force an account's password to a new value. This should be used only in the 
     context of an account reinitialization.

   :http:post:`/accounts/{ACCOUNT_ID}/authsystems/password/change`
     Allow a user to change an account password. The given old password must
     be correct for this change to succeed. This is a 3-legged call, since the
     user is the one driving this interaction (unlike 
     :http:post:`/accounts/{ACCOUNT_ID}/authsystems/password/set`, wherein the 
     admin app is forcefully setting a password).

   :http:get:`/accounts/{ACCOUNT_ID}/primary-secret`
     Fetch an account's primary secret. This should be used very sparingly as the 
     primary secret should rarely be seen outside of the Indivo backend.

Record Administration
^^^^^^^^^^^^^^^^^^^^^

.. glossary::

   :http:get:`/records/{RECORD_ID}`
     Get info about a single record.

   :http:get:`/records/search`
     Search Indivo for existing records by record label.
   
   :http:get:`/records/{RECORD_ID}/owner`
     Get the owner of a record

   :http:get:`/records/{RECORD_ID}/apps/`
     List applications attached to a record. Supports order by ``name``.   

   :http:post:`/records/`
   :http:put:`/records/external/{APP_ID}/{EXTERNAL_ID}`
     Create a new record, possibly assigning it an external id. This call requires 
     a valid Indivo :doc:`Contact Document <schemas/contact-schema>` in order to 
     create the record.

   :http:put:`/records/{RECORD_ID}/owner`
     Set the owner of a record.

   :http:post:`/records/{RECORD_ID}/apps/{APP_ID}/setup`
     Prime a record with a user app. This sets up an app to run against a record
     without user consent. It should be used only in cases where obtaining 
     consent is impossible or unnecessary (i.e., at a hospital installation of
     Indivo, this call could be used to prime all new records with the syncer
     application that pulls data into Indivo from the hospital EMR).

   :http:put:`/records/{RECORD_ID}/apps/{APP_ID}`
     Enable an app to run against a record. This gives the app access to the entire
     record.

   :http:delete:`/records/{RECORD_ID}/apps/{APP_ID}`
     Remove a user app from a record.

Indivo Chrome / User Interface API
----------------------------------

These API calls are reserved for the UI server, which is deeply trusted to 
authorized other applications, proxy the user's credentials, etc. It's only a 
separate server for modularity, otherwise it has the same level of trust as the 
backend Indivo server.

.. glossary::

   :http:post:`/oauth/internal/session_create`
     Create a web-session for a user. This call returns a session token that
     can be used to authenticate 3-legged calls on behalf of the user for the
     duration of a standard web session (30 minutes by default)
     
   :http:post:`/oauth/internal/request_tokens/{REQUEST_TOKEN}/claim`
     Claim a request token on behalf of a user. Before a request token can be 
     viewed at all, it has to be claimed by a user. This ensures that a request 
     token can't be partially used by one user and completed by another.

     The session-based chrome authentication will indicate to the backend which 
     Account to associate with this request token. Once this call has been made 
     for a request token, a second call with different session authentication will 
     fail. (A second call with the same user authentication will be just fine, we 
     don't want a reload to cause a problem.)

     If the request token is bound to an Indivo record (because the PHA knew it 
     was authorizing for a given record), and the claimant does not have 
     administrative rights over the record, this call will fail and the request 
     token will be invalidated.

   :http:get:`/oauth/internal/request_tokens/{REQUEST_TOKEN}/info`
     Retrieve information about an oAuth request token.

     When authorizing a request token, the Indivo UI needs to know what that token 
     represents. Once the token is claimed, the request token yields information 
     via this call.

     This call can only be called with session authentication matching the Account 
     which claimed the request token earlier.

     If a ``record_id`` is present in the response data, then the kind element is 
     also present and indicates:

     * ``new``: a new request for a PHA that has not been authorized for this 
       record yet

     * ``same``: a request for a PHA that is already attached to the record and no 
       new permissions are requested

     * ``upgrade``: a request for a PHA that is already attached to the record but 
       that is asking for more permissions or more permissive usage of the data.

     In the ``same`` case, the Chrome UI is allowed to immediately approve the 
     request token. In other cases, the Chrome UI must explain to the user that 
     new permissions or rights are being granted and prompt the user for approval.

   :http:post:`/oauth/internal/request_tokens/{REQUEST_TOKEN}/approve`
     Approve a request token on behalf of a user.

     If a user approves an app addition, then the Chrome UI server needs to let 
     the backend know.

     This call, if it succeeds with a :http:statuscode:`200`, will return the 
     location to which the user's browser should be redirected::

       location={url_to_redirect_to}

     This call's session authentication must match that which claimed the request 
     token. The ``record_id`` is the record to which the user is attaching the 
     application (i.e. my child's record, not my own.) If the request token was 
     pre-bound to a record, this ``record_id`` parameter must match, or this will 
     throw an error.

   :http:post:`/accounts/{ACCOUNT_EMAIL}/apps/{PHA_EMAIL}/connect_credentials`
     Get credentials for :ref:`Connect-style Authentication <connect-auth>` for a
     user app, and authorize them on behalf of an account.

     This call will return tokens that can be used to sign future API calls by the
     user app, proxied by the UI.

   :http:get:`/accounts/{ACCOUNT_ID}/check-secrets/{PRIMARY_SECRET}`
     Check the primary and secondary secrets of an account.

   :http:get:`/oauth/internal/surl-verify`
     Verify a signed URL.
     
     In some cases, an Indivo app will sign a URL that directs the user to the 
     Indivo UI. A prime example is the use of Indivo Chrome widgets, i.e. the 
     Document Sharing widget, that apps can embed within their user interface to 
     reuse functionality from Indivo Chrome. A signed URL looks like this::

       /widgets/WidgetName?param1=foo&param2=bar&surl_timestamp={TIMESTAMP}&surl_token={TOKEN}&surl_sig={SIGNATURE}

     The signature contained in surl_sig is effectively a signature on the rest 
     of the URL. The signature algorithm is as follows:

     #. An app, with oAuth access token ``TOKEN`` and oAuth access token secret 
        ``SECRET``, wishes to sign a URL. 

     #. The app generates the SURL secret that corresponds to this access token as 
        follows::

     	  <SURL_SECRET> = HMAC(<TOKEN_SECRET>, "SURL-SECRET")

  	using base64 encoding, where the idea is to actually sign the string 
   	"SURL-SECRET" to obtain the SURL secret itself.

     #. this SURL secret is then used to sign the URL, first by appending a 
        timestamp, the SURL token, and then computing the signature::

 	<SURL_SIG> = HMAC(<SURL_SECRET>, "/widgets/WidgeName?...&surl_timestamp=<TIMESTAMP>&surl_token=<TOKEN>")

        in base 64, then appending it as a query parameter surl_sig.

Sharing
-------

Overview
^^^^^^^^

We want to simplify sharing. Indivo has two main mechanisms for sharing patient
records with other accounts: :dfn:`Full Shares` and :dfn:`Carenets`. 

.. _full-share:

.. glossary::

   Full Share
     A user may choose to share the entirety of their record with another account. 
     The recipient account will then have access to all data (past, present, and 
     future) contained in the record, and will be able to run any apps that have
     been bound to the record. The recipient of a full share will also be able to
     add new applications to the record and run them against data in the record.

     Similarly, a user may choose to add an application to their full record. This
     effectively creates a 'full share' of the record with that application: the 
     app has access to all data in the record.

     As an example, a teen user of Indivo might choose to set up a full share of 
     his / her record with a parent of guardian.

   Carenet
     Full shares are not very flexible: they are an all or nothing proposition. In 
     cases where sharing data appropriately requires more granularity or 
     complexity, Indivo provides **carenets**, which allow a record to specify 
     groups of *accounts* and *apps* that all have transparent access to whatever 
     *data* the record shares into the carenet.

     By default, each record will have 3 simple carenets: physicians, family, and 
     work/school.

     As an example, a patient might create an 'exercise' carenet, into which they 
     place:

     * *data*: blood-pressure readings, pedometer output, and other data associated
       with maintaining a healthy lifestyle.

     * *apps*: blood-pressure viewers, exercise-trackers, and other apps that help 
       the patient organize and interact with their exercise data.

     * *accounts*: The patient's Primary Care Physician, personal trainer, friends,
       or any other person with an interest in helping the patient develop healthy 
       exercise habits.

     Now anyone on the *accounts* list can log into Indivo and run any app on the 
     *apps* list against any data on the *data* list.

     Data can be placed into carenets individually, or autoshared by Document 
     type. Users can override the type-auto-sharing on a document-by-document 
     basis.

   Autoshare
     Documents of a certain type can be auto-shared, so that they are added to a 
     carenet automatically when they are added to the record. When auto-share 
     preferences are set for a type of document within a given carenet, these 
     preferences apply to all documents that do not have an explicit sharing 
     preference declared on them.

   Nevershare
     A user should be able to ask that a specific document be "never shared". This 
     flag prevents any sharing, no matter what the auto-share rules may be.


Authorization into a CareNet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When an app is added, it is normally given, along with its oAuth token, an 
``xoauth_indivo_record_id`` that the token corresponds to. If the app is added to
a carenet instead of a record, the app will receive instead an 
``xoauth_indivo_carenet_id``.

Carenet-aware API calls
^^^^^^^^^^^^^^^^^^^^^^^

Many of the document and reporting calls that can be made on 
:file:`/records/{{RECORD_ID}}` can be made on :file:`/carenets/{{CARENET_ID}}`.
Where applicable, such calls have been listed throughout this document.

Importantly, carenets are (at present) **READ-ONLY**. Accounts placed in carenets
may view any data in the carenets, but we have not implemented any calls for them
to modify or add to that data. In the future, carenets will be write-capable.

Sharing API
^^^^^^^^^^^

Full Shares
"""""""""""

.. glossary::

   :http:get:`/records/{RECORD_ID}/shares/`
     List accounts with which a record has created full shares. This call also
     lists user apps that have access to the full record, as such apps have the
     same access to data as an account with a full share.

   :http:post:`/records/{RECORD_ID}/shares/`
     Create a new full-record share with an account. The role_label is currently 
     nothing more than that: a label. The label will come back in a call to
     :http:get:`/records/{RECORD_ID}/shares/`.

   :http:delete:`/records/{RECORD_ID}/shares/{ACCOUNT_ID}`
     Delete a full share.

Basic Carenet Calls
"""""""""""""""""""

.. glossary::

   :http:get:`/records/{RECORD_ID}/carenets/`
     List existing carenets on a record.

   :http:get:`/carenets/{CARENET_ID}/record`
     Fetch basic information about the record that a carenet belongs to.

   :http:post:`/records/{RECORD_ID}/carenets/`
     Create a new carenet on a record.

   :http:post:`/carenets/{CARENET_ID}/rename`
     Rename a carenet.

   :http:delete:`/carenets/{CARENET_ID}`
     Delete a carenet. This will unshare all of the data in the carenet with
     all users and apps in the carenet.

Data in Carenets
""""""""""""""""

Carenets are useless until data has been shared into them. Data can be shared
explicitly at the granularity of individual documents, or implicitly at the 
granularity of document type.

.. glossary::

   :http:put:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}`
     Place a document in a carenet.

     When a document is explicitly shared with a carenet, it is no longer tied 
     to the auto-sharing rules for that carenet. However, auto-sharing rules with 
     other carenets still apply.

   :http:delete:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}`
     Remove a document from a carenet

     When a document is explicitly **UN**\ shared from a carenet, it is no longer 
     tied to the auto-sharing rules for that carenet. However, auto-sharing rules 
     with other carenets still apply.

   :http:get:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/`
     List carenets where a document is present

     The ``mode`` attribute indicates how this document is shared. ``explicit`` 
     means that the sharing preferences for this document are explicitly set. 
     ``bytype`` indicates that it was auto-shared by document type. Other modes 
     may be enabled in the future.

     The ``value`` attribute indicates a negative share with a carenet, meaning 
     that the user explicitly wants this document not shared with this carenet, 
     even if auto-share rules would otherwise share it. Obviously this only makes 
     sense for explicit carenet-shares.

   :http:post:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}/autoshare-revert`
     Revert a document to auto-share rules. This means that, for this carenet, 
     this document reverts to automatic sharing rules. This might mean a removal 
     of the share with this carenet, or an addition, or no effect. However, from 
     this point on, the record-wide rules apply.

     .. warning::
     
	This call has not yet been implemented.

   :http:get:`/records/{RECORD_ID}/autoshare/bytype/`
     List auto-sharing preferences for a given document type with a record. This 
     call returns a list of carenets into which the document type is auto-shared. 

   :http:get:`/records/{RECORD_ID}/autoshare/bytype/all`
     List all auto-sharing preferences for a record. This call returns a list
     of document types with the carenets into which each type is auto-shared.

   :http:post:`/records/{RECORD_ID}/autoshare/carenets/{CARENET_ID}/bytype/set`
     Add an auto-share of a given document type into a given carenet. This 
     share applies to all documents that do not have an explicit sharing 
     preference declared on them.

   :http:post:`/records/{RECORD_ID}/autoshare/carenets/{CARENET_ID}/bytype/unset`
     Remove an auto-share for a given document type from a given carenet.

   :http:put:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/nevershare`
     Set the never share flag on a document. A user should be able to ask that a 
     document be "never shared". This flag prevents any sharing, no matter what 
     the auto-share rules may be.

   :http:delete:`/records/{RECORD_ID}/documents/{DOCUMENT_ID}/nevershare`
     Remove the nevershare flag on a document.

Apps in Carenets
""""""""""""""""

Users needs to be able to place apps inside carenets in addition to
documents, so that other accounts can run the applications. There are no issues
with read/write premissions here, as permissions are associated with the accounts
in a carenet, not the apps.

.. glossary::

   :http:get:`/carenets/{CARENET_ID}/apps/`
     List all apps in a carenet.

   :http:put:`/carenets/{CARENET_ID}/apps/{PHA_EMAIL}`
     Add an app to a carenet.

   :http:delete:`/carenets/{CARENET_ID}/apps/{PHA_EMAIL}`
     Remove an app from a carenet.

   :http:get:`/carenets/{CARENET_ID}/apps/{APP_ID}/permissions`
     Check an app's permissions within a carenet. Since permissions are
     currently handled on accounts, not apps, this call will always indicate
     that the app has full permissions on the carenet.

     .. warning::
     
	This call has not yet been implemented.

Accounts in Carenets
""""""""""""""""""""

Users needs to be able to place other accounts inside carenets so that they can
share data and apps. When accounts are added to a carenet, they are assigned
read/write permissions, which define what actions they can take on data in the
carenet.

.. glossary::

   :http:get:`/carenets/{CARENET_ID}/accounts/`
     List all accounts in a carenet.

   :http:post:`/carenets/{CARENET_ID}/accounts/`
     Add an account to a carenet.

   :http:delete:`/carenets/{CARENET_ID}/accounts/{ACCOUNT_ID}`
     Remove an Account from a carenet.

   :http:get:`/carenets/{CARENET_ID}/accounts/{ACCOUNT_ID}/permissions`
     Check an acount's permissions within a given carenet. This call will return
     a list of document types, and whether the account may write to each one 
     within the given carenet.

    For now, the document type is always "*", since read/write permissioning is
    not currently more granular than at the carenet level. We may eventually
    permit permissioning by document types within a carenet, in which case this
    call will be more informative.

Building Carenet-aware Apps
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Indivo apps are given a ``record_id`` and an access token that matches that 
record to read and write documents, read reports, annotate, etc. In a sharing 
scenario, apps must become carenet-aware.

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

As Indivo will be installed at HIPAA-compliant hospital sites, it is important
that it be able to track system usage. The auditing system logs all incoming 
requests to Indivo that use the Indivo API. To learn more about auditing in Indivo,
see the :doc:`audit system's documentation <audit>`.

.. glossary::

   :http:get:`/records/{RECORD_ID}/audits/query/`
     Query the audit system. This call allows for general queries over the 
     audit logs. The query is specified in the parameters via the :doc:`query-api`,
     and returns results in the style of Medical Reports.

All subsequent calls are deprecated, but maintained (for now) for backwards 
compatibility.

.. glossary::

   :http:get:`/records/{RECORD_ID}/audits/`
     List all audit log entries where a given record was accessed.
     
     .. deprecated:: 1.0.0


   :http:get:`/records/{RECORD_ID}/audits/documents/{DOCUMENT_ID}/`
     List all audit log entries where a given document was accessed.

     .. deprecated:: 1.0.0

   :http:get:`/records/{RECORD_ID}/audits/documents/{DOCUMENT_ID}/functions/{FUNCTION_NAME}/`
     List all audit log entries where a given document was accessed via a given
     internal Django view function.

     .. deprecated:: 1.0.0

.. COMING SOON!!

   Data Usage Intent and Share Tracking
   ------------------------------------

