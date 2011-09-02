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
where the `@` sign turns into `%40`.

Paging/Filtering Results
^^^^^^^^^^^^^^^^^^^^^^^^

When a list of results are returned, the URL ends in a `/` and the HTTP method is a `GET`, as is typical of 
REST design. In that case, Indivo X supports a generic query string that determines paging and ordering of 
the results::

  ?offset={offset}&limit={limit}&order_by={order_by}&status={document_status}&modified_since={modified_since}

* `offset` indicates which item number to start with, e.g. when getting a second batch of items.

* `limit` indicates the maximum number of items to return. This is used in combination with offset to 
  accomplish paging.

* `order_by` is dependent on the fields returned in the list of items, and each call must thus define which 
  fields are valid. Using an invalid field in order_by results in no effect on the output, as if order_by 
  were absent.

* `status` can be used where applicable. It pertains to the status of documents and can currently be set to 
  one of three options: 'void', 'archived' or 'active'

* `modified_since` allows an application to look at items that have been modified since a given timestamp, 
  so that incremental downloads may be possible.

Querying Results
^^^^^^^^^^^^^^^^

As of the Beta3 release, calls that implement the basic paging operations above may also implement a more 
powerful :doc:`query interface <query-api>`, also represented in the query string. In these cases (currently 
all of the minimal medical reports and the auditing calls), the following values may occur in the query string::

  ?offset={offset}&limit={limit}&order_by={order_by}&status={document_status}

These values function as before. ::

  ?group_by={group_field}&aggregate_by={aggregation_operator}*{aggregation_field}

`group_by` groups results by the specified field. It must be used in conjunction with `aggregate_by`, which 
aggregates the results by group, using the specified operation. If `aggregate_by` is passed without a 
`group_by` parameter, the aggregation is performed over the entire result set. Results that have been 
aggregated are returned in an aggregated format, not the typical reporting format. ::

  ?date_range={date_field}*{start_date}*{end_date}

`date_range` filters results and leaves only those with the specified field falling between `start_date` 
and `end_date`. ::

  ?date_group={date_field}*{time_increment}&?aggregate_by={aggregation_operator}*{aggregation_field}

`date_group` functions equivalently to `group_by`, except the groups are formed based on the values of the 
specified date field. For example, if the date field was 'date_measured', and the time increment was 'month', 
results would be returned grouped by the month of the date_measured field for each item. As with `group_by`, 
`date_group` must be used with an aggregator, and results are returned in an aggregated format. ::

  ?{FIELD}={VALUE}

This syntax adds additional filters to the query, returning only results having whose value for the property 
specified by 'field' matches 'value'.

For each of these parameters, acceptable values for `{field}` are specified individually by the calls. A 
full listing of the minimal reporting fields, along with valid aggregation operators and date increments, 
may be found :doc:`here <query-api>`.

External IDs
^^^^^^^^^^^^

When a resource is created, the Indivo API offers the ability to create this resource using a `PUT` with an 
`external_id` in the URL, so that the call is idempotent: if a failure occurs, the call can be repeated safely 
and only the resource will not be created on the second call if it was already created successfully during 
the first call.

An `external_id` is only valid within a particular PHA scope. Other PHAs cannot see the external_id of a given 
document if they didn't create the document, and certainly cannot access the document by external_id.

Managing Records and Documents
------------------------------

Data stored in Indivo cannot by permanently deleted by default: the API enforces only appending data, not fully 
replacing it or removing it.

Available Records
^^^^^^^^^^^^^^^^^

.. http:get:: /accounts/{ACCOUNT_EMAIL}/records/

::

  <Records account="joe@smith.org">
    <Record id="b43810b8-1ff0-11de-b090-001b63948875" label="Joe Smith" />
    <Record id="c002aa8e-1ff0-11de-b090-001b63948875" label="Jill Smith" />
  </Records>

supports paging, order by: label.

Record
^^^^^^

.. http:get:: /records/{RECORD_ID}


::

  <Record id="c002aa8e-1ff0-11de-b090-001b63948875" label="Jill Smith">
    <contact document_id="83nvb-038xcc-98xcv-234234325235" />
    <demographics document_id="646937a0-1ff1-11de-b090-001b63948875" />
  </Record>





.. http:get:: /accounts/

.. http:get:: /apps/
