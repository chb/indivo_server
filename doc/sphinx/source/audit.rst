The Audit System
================

Auditing will live in a middleware that is called after the Authentication and 
Authorization middleware.

The ordering is so that auditing will know the principal and view_func/view_(kw)args 
during processing.

When no principal is present we will not audit.

If principal is not None then we will record relevant information related to the 
request.

The amount of information audited and which calls to audit will be configurable in 
the top-level settings.py file

Data to Audit
-------------
Redundancy is built into the audit table so that as few assumptions are made when 
investigating a req/resp. as possible. The proposed table will be broken down into five sections:

Basic Info
^^^^^^^^^^^^^^^^
This information will always be audited, and contains basic information about the request.

* ``datetime``: When the request was made
* ``view_func``: Which Indivo View Function was called by the request
* ``request_successful``: Was the request successful, or were there errors in its execution

Principal Info
^^^^^^^^^^^^^^
Information about the principal of the request.

* ``effective_principal_email``: The email of the principal making the request
* ``proxied_by_email``: The email of the principal proxied by the principal making the request 
  (i.e., the email of the Account being proxied by a PHA)

Resources
^^^^^^^^^
Information about the resources being accessed by a request

* ``carenet_id``: Identifies the carenet a request is made through
* ``record_id``: Identifies the record a request is made through
* ``pha_id``: Identifies the PHA a request modifies
* ``document_id``: Identifies the document accessed by a request
* ``external_id``: Identifies the external identifier used to represent a resource in a request
* ``message_id``: Identifies the message accessed by a request

Request Info
^^^^^^^^^^^^
Information carried in by the request

* ``req_url``: The URL to which the request was made
* ``req_ip_address``: The ip adress from which the request originated
* ``req_domain``: The domain from which the request originated
* ``req_headers``: Headers associated with the request, including Oauth credentials
* ``req_method``: The HTTP method with which the request was sent (GET, PUT, POST, DELETE)

Response Info
^^^^^^^^^^^^^
Information about the response being returned

* ``resp_code``: The HTTP response code returned by the request
* ``resp_headers``: Headers sent out with the response, including content type

Configuring the Audit System
----------------------------
The following fields in settings.py may be altered to configure the system:

* ``AUDIT_LEVEL``: Values are HIGH, MED, LOW, NONE. Controls the amount of information recorded 
  for each call. See :ref:`audit-levels` below for details.

* ``AUDIT_OAUTH``: Values are True, False. Controls whether or not calls related to the oauth dance 
  are audited.

* ``AUDIT_FAILURE``: Values are True, False. Controls whether or not calls which exited with failure 
  (HTTP Response Code of 400 or greater) are audited.

Default Values
^^^^^^^^^^^^^^
Defaults for the audit settings record as much information as possible. They are:

* ``AUDIT_LEVEL``: HIGH
* ``AUDIT_OAUTH``: True
* ``AUDIT_FAILURE``: True

.. _audit-levels:

Audit Levels
^^^^^^^^^^^^
The information recorded at each audit level is also configurable. Defaults are:

* ``NONE``: no information is recorded.
* ``LOW``:  Basic Information and Principal Information are recorded.
* ``MED``: Basic Information, Principal Information, and Resources are recorded.
* ``HIGH``: Basic Information, Principal Information, Resources, Request Information, and Response information are recorded.

.. _audit-query-fields:

Querying the Audit System
-------------------------
There will be a new API call that implements the :doc:`API Query Interface <query-api>`.
Calls to::

  GET /records/{record_id}/audits/query/

May retrieve audit entries filtered and grouped by the following fields:

* ``document_id``: The document modified by the request. **String**
* ``external_id``: The external id used to reference a resource in the request. **String**
* ``request_date``: The date on which the request was made. **Date**
* ``function_name``: The internal Indivo X view function called by the request. **String**
* ``principal_email``: The email of the principal making the request. **String**
* ``proxied_by_email``: The email of the principal proxied by the principal making the request 
  (i.e., the email of the Account being proxied by a PHA). **String**

The default ordering on results will be in descending order by ``request_date``.

Audit queries will be returned (like all data returned form the API Query Interface) according to the 
:doc:`Indivo Reporting Schema <schemas/reporting-schema>`. Individual items will validate against the 
:doc:`Indivo Audit Log Schema <schemas/audit-schema>`.

Compatibility Issues with old Audit System
------------------------------------------
The Beta1 interface calls will be preserved, although they are now deprecated.

However, in order to accommodate the new data being stored, the output schema for audit logs has changed. 
Audit logs will now be returned according to the :doc:`Indivo Reporting Schema <schemas/reporting-schema>` and 
new :doc:`Indivo Audit Log Schema <schemas/audit-schema>`, as with the new call above.
