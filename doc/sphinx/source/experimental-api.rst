Indivo Experimental APIs
========================

The Indivo experimental APIs are used to evaluate new potential features. They are not guaranteed to be supported, 
consistent, or used in production. When an API is experimental, it is under the ``/experimental/`` URL base. An 
API graduates to full support by being moved into the normal tree of API URLs, which requires a change in all clients 
that implement it. This is done on purpose: to ensure that experimental APIs cannot be depended upon, ever, until they 
graduate to full support.

PubSub
------

*Status*: first design, **no implementation**

Applications may want to be notified of changes that occur in the record, so they can take action without having to 
constantly poll the Indivo server. We call these subscriptions.

Add a subscription
^^^^^^^^^^^^^^^^^^
::

  POST /experimental/records/{record_id}/apps/{pha_email}/subscriptions/
  url={url}&
  callback={callback_url}

  <Subscription id="..." />

A subscription is created by an app on a specific URL, within a record. The URL is relative to the record, i.e. ``/reports/medication/``. For now only report URLs are supported.

The callback URL is the URL that Indivo should connect to when an update pertaining to that subscription occurs. 

View subscriptions
^^^^^^^^^^^^^^^^^^
::

  GET /experimental/records/{record_id}/apps/{pha_email}/subscriptions/

  <Subscriptions>
    <Subscription id="..">
      <expires_at>...</expires_at>
      <url>...</url>
    </Subscription>
  </Subscriptions>


A subscription lasts 3 months by default, and then automatically expires and must be renewed.

Remove subscription
^^^^^^^^^^^^^^^^^^^
::

  DELETE /experimental/records/{record_id}/apps/{pha_email}/subscriptions/{subscription_id}

Behavior of a subscription ping
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When an app is to be notified of a change, if, for example, that app subscribes to medications, then a new medication 
would trigger::

  POST <callback_url>
  record_id={record_id}&
  url={url}

Pings based on a subscription are expect a 200 successful HTTP code. If they receive a 500 or other error code, 
the ping will be tried again with exponential backoff, using 1 minute as initial retry interval, and a factor of 2 
between retries.
