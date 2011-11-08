Indivo Authentication
=====================

Calls to the :doc:`Indivo API <api>` are authenticated using `oAuth <http://oauth.net>`_. Here, we provide 
details of exactly how Indivo uses oAuth, in particular the options that are supported and those that aren't.

Specifics of our oAuth implementation
-------------------------------------

OAuth Section 5.2 defines three possible approaches to sending OAuth Protocol Parameters. In Indivo, we use 
exclusively the `HTTP authorization header <http://oauth.net/core/1.0/#auth_header>`_, as defined by the 
OAuth specification, as the preferred method. We allow ``oauth_callback`` and ``oauth_verifier`` to be 
provided as POST parameters, only because some client libraries that are not oAuth 1.0a-compatible cannot 
otherwise connect.

We require all changes suggested by the oAuth 1.0a revision:

* When asking for a request_token, the PHA *must* provide ``oauth_callback`` as an extra oAuth parameter. 
  This can be a URL where Indivo X will send the user after token authorization, or it can be ``oob`` to use 
  the default URL specified by the PHA at registration time.

* When responding to a request token, Indivo X will include ``oauth_callback_confirmed=true``

* A PHA's callback URL should accept both ``oauth_token`` and ``oauth_verifier`` parameters.

* When exchanging a request token for an access token, the PHA must provide the corresponding ``oauth_verifier`` 
  parameter in addition to all existing parameters.

In addition, we implement the following constraints:

* As per the oAuth recommended approach, all oAuth token setup and exchange calls use the ``POST`` method. The 
  Indivo server will respond with a 405 Method Not Allowed error code to any GET request against its OAuth 
  protocol URLs.

* The ``oauth_version`` parameter is mandatory. Every PHA request should include the ``oauth_version`` parameter. 
  The only supported value in Indivo at this point is ``oauth_version=1.0``.

* Given an Indivo Server running at ``https://INDIVO_SERVER``, the OAuth URLs are defined as follows:

  * Request Token URL: ``https://INDIVO_SERVER/oauth/request_token``

  * User Authorization URL: Since there is a UI component to enabling User Authorization
    (i.e., we have to obtain their consent), Indivo_Server does not explicitly offer a
    User Authorization URL via its API. Individual UI apps can (with a valid user session)
    authorize tokens on behalf of users with a call to 
    :http:post:`internal/request_tokens/{TOKEN}/approve`, but each individual UI-app 
    implementation will provide a different app-facing User Authorization URL. We 
    recommend using ``https://UI_SERVER/oauth/authorize?oauth_token={token}``, which is
    the URL used by our reference UI-app implementation.

  * Access Token URL: ``https://INDIVO_SERVER/oauth/access_token``

* oAuth defines a number of default signature methods and leaves open the possibility of using other signature 
  methods. Indivo supports only one request signature method: **HMAC-SHA1**. Support for RSA-SHA1 may 
  eventually be added.

Body and Content-Type
---------------------

By default, oAuth only signs the body of HTTP requests that are form-url-encoded. Indivo uses the 
`oAuth Body Hash Extension <http://oauth.googlecode.com/svn/spec/ext/body_hash/1.0/drafts/4/spec.html>`_ to ensure 
that raw POSTs, e.g. to send XML documents, become part of the signature. When the body-hash extension is activated, 
Indivo also expects an additional parameter, ``oauth_content_type``, to certify the content type HTTP header 
(and prevent content-sniffing attacks.)

User Applications (PHAs)
------------------------

PHA Registration
^^^^^^^^^^^^^^^^

A PHA registers with Indivo using an Indivo-installation specific process, at the conclusion of which both Indivo and 
the PHA agree on:

* The name of the PHA, e.g. "Medical Surveys"

* An oAuth ``consumer_key`` and ``consumer_secret``.

* A ``start_url_template`` for the PHA, e.g. 
  ``http://acme.com/indivoapp?record_id={indivo_record_id}&document_id={document_id}``.

* A ``callback_url`` for the PHA, e.g. ``http://acme.com/success_after_indivo``, which should expect to receive query 
  parameters ``oauth_token`` and ``oauth_verifier``.

* Whether the PHA has a web user interface (certain applications that synchronize data have no UI), and whether that 
  PHA is frameable inside Indivo.

* Whether the PHA is :ref:`autonomous <autonomous_apps>` or not, and if it is, why it wants that kind of access to the 
  user's personal health record.

**IMPORTANTLY**, the ``callback_url`` is the only URL that Indivo will return the user to after a successful PHA attachment. 
Indivo does not support a custom oAuth callback URL.

.. _autonomous_apps:

Autonomous Apps
^^^^^^^^^^^^^^^

An autonomous app is one that wants to access the user's record while the user is not connected. PHAs that qualify 
include hospital data connectors, drug-interaction checkers, etc. There are very good reasons for PHAs to access a 
record while the user is not online, but we want to ensure that users understand the implications, and thus the 
Indivo authorization pathway looks different depending on whether an app is autonomous or not.

An app must choose to be autonomous at registration time. It must be autonomous for all users, or for none.

An autonomous app accesses the entire record by default, and the user must consent to this. This design choice is meant 
to prevent medical mistakes for automated apps that, for example, check for drug-drug interactions but may fail to notify 
the user if they have only partial data access. An autonomous app thus triggers the appropriate authorization screen that 
warns the user about the long-term, autonomous access, displays the app's reason for requesting this type of access, and 
simply gives the user a yes/no choice.

Autonomous apps can, in some circumstances, have no user-interface. This might happen if, for example, a hospital connector 
application sits behind the hospital firewall and connects autonomously to the Indivo record to upload hospital data into 
the PCHR, but never lets the user connect directly to the app itself. The only way, currently, to authorize such an 
application is via admin-based PHA setup, where an administrative app primes the Indivo record with this app. In the future, 
autonomous apps without a user interface may be permissioned by the user directly. In any case, these apps must declare their 
lack of UI at registration time, much like they declare their being autonomous or not. Only autonomous apps can choose 
to forgo a UI.

A non-autonomous app, on the other hand, is one that is meant to be used by whoever is logged in and has access to the record 
in question. Depending on which user has launched the app, the app's permissions might differ. For example, when Alice uses 
the Problems App within her record, she should see ''all'' of her problems. However, when Bob, her co-worker, uses the Problems 
App to view Alice's record, he should see only those problems which Alice has chosen to let him see. Thus, a non-autonomous 
app exists purely to proxy a human user's clicks and perform some visualization / data entry assistance functionality. 
Non-autonomous apps are thus constrained to a carenet at the time that the user clicks on the app name to launch it. 
When Bob launches the Problems App on Alice's record, the Problems App receives an access token that is constrained to 
Alice's "Work" carenet, and the app can only access the problems Alice has made available within her Work carenet. All 
access tokens for non-autonomous apps are valid only for the duration of a web session.

Connecting a PHA to a Record
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When a user opts to add a PHA to her Indivo record, she is sent to the PHA's ``start URL`` with the ``indivo_record_id`` 
filled in. The PHA may present informational content if it so desires, then is expected to begin the OAuth authorization 
process. When the PHA begins the oAuth process, it should do so with the indicated ``indivo_record_id`` that it received 
when its ``start_url`` was accessed.

Obtain a Request Token
""""""""""""""""""""""

A PHA begins its access request for a user when the user visits the PHA's ``start URL``. While the user's browser awaits 
a response, the PHA obtains from the Indivo Server a request token. This is accomplished by issuing a signed ``POST`` 
2-legged oAuth request to the Request Token URL::

  https://INDIVO_SERVER/oauth/request_token

with optional form parameter ``indivo_record_id``. Again, if the PHA was accessed via its ``start_url`` with the Indivo 
record ID filled in, it should use this record ID at this point in obtaining the request token. Otherwise, the user 
interface will be thoroughly confusing.

This call returns an oAuth token::

  oauth_token={token}&oauth_token_secret={secret}

The PHA is expected to store the Request Token and its correspondence to this specific user, likely in the web session.

Authorize the Request Token
"""""""""""""""""""""""""""

Once it has obtained a request token, with the user's browser still waiting for a response, the PHA responds by redirecting 
the user's browser to the User Authorization URL on an Indivo UI app, indicated in the request token response above, or by 
default::

  https://UI_SERVER/oauth/authorize?oauth_token=<REQUEST_TOKEN>

with the ``request_token`` as a URL query parameter named ``oauth_token``. Note how this URL is not a signed OAuth 
request. This step is simply a redirection of the user's browser to her Indivo account in order to prompt for and obtain 
authorization.

Indivo prompts the user to authenticate if she isn't already logged in. Indivo then associates the request token with this 
user, and only this user can proceed with this specific request token. It is an error for a PHA to attempt to reuse request 
tokens, and Indivo will prevent this from happening.

Indivo then presents the user with the details of the PHA's requested permissions.

The user can choose to cancel the process, in which case no further requests are issued, the PHA is not notified, and the 
request token is discarded.

Obtain an Access Token
""""""""""""""""""""""

If the user agrees to connect with the PHA, Indivo redirects the user browser to the PHA's ``callback_url``, as specified 
by the PHA at registration time. Appended to this ``callback_url`` are the ``oauth_token``, the request token that identifies 
this authorization dance, and the ``oauth_verifier``. The PHA is encouraged to check that the ``oauth_token`` matches the 
token stored in its web-session.

The PHA must now exchange the Request Token for an Access Token. This is accomplished using a 3-legged oAuth POST request, 
with the request token and secret, to::

  https://INDIVO_SERVER/oauth/access_token

In response to this request, the PHA obtains an Access Token, including one of two optional parameters::

  oauth_token=<TOKEN>&oauth_token_secret=<SECRET>&xoauth_indivo_record_id=<RECORD_ID>

or ::

  oauth_token=<TOKEN>&oauth_token_secret=<SECRET>&xoauth_indivo_carenet_id=<CARENET_ID>


This token can then be used by the PHA to make 3-legged oAuth calls to Indivo. The Indivo record ID parameter indicates 
which record this token is bound to, while the carenet indicates which portion of the system the PHA can access.

Interact and Re-Auth
""""""""""""""""""""

At this point, the PHA has an access token, an access secret, an Indivo record ID, and an Indivo privacy group. These 
credentials allow the PHA to make calls to the Indivo Server to obtain data from the given Indivo record. If the PHA 
provides a direct web interface to the user, this UI is delivered inside an IFRAME within the Indivo User Interface.

A few days later, when the user returns to his Indivo record, he can click on any of the PHAs he has already authorized. 
The PHA, however, does not know immediately who this user is. To communicate the user's identity to the PHA, Indivo simply 
re-performs the oAuth dance, setting the IFRAME's URL to the PHA's starting point with the prescribed Indivo Record ID. 
When the PHA redirects the IFRAME to the authorization page, Indivo notices that this record has already authorized the app, 
and simply redirects the IFRAME immediately to the PHA's ``callback_url``. Thus, a complete oAuth process is re-performed, 
and the PHA re-obtains an access token, access secret, Indivo record ID and privacy group.

The PHA should never assume that the access token and secret stay the same. The long-term identifier that the PHA should 
key its data against is the Indivo Record ID.

Admin Applications
------------------

Admin Applications contact the Indivo X server using 2-legged oAuth only, with just a consumer key and consumer secret.

Chrome Applications
-------------------

Most Indivo developers who only wish to write PHAs can safely ignore Chrome applications. Developers who wish to customize 
the entire Indivo experience need to understand Chrome apps.

The Indivo Chrome (User Interface) contacts the Indivo X server first using 2-legged oAuth to create a user-specific session 
using the user's username and password. Indivo X responds with a fresh oAuth token and secret valid for the length of a 
typical web session. Then all Indivo Chrome calls to the Indivo X server on behalf of a given user are made as 3-legged calls, 
using the Indivo Chrome's consumer key and secret, and the specific session token and secret.

