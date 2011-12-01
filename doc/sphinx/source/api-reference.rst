
API Reference
=============

This page contains a full list of valid Indivo API calls, generated from the code.
For a more detailed walkthrough of individual calls, see :doc:`api`


--------

.. http:post:: /accounts/

   Create a new account, and send out initialization emails.

   :shortname: account_create
   :accesscontrol: Any admin app.
   :formparameter primary_secret_p: 0 or 1: Does this account require a primary secret?
   :formparameter secondary_secret_p: 0 or 1: Does this account require a secondary secret?
   :formparameter contact_email: A valid email at which to reach the account holder.
   :formparameter account_id: An identifier for the new account. Must be a valid email address. **REQUIRED**
   :formparameter full_name: The full name to associate with the account.
   :returns: :http:statuscode:`200` with information about the new account on success, :http:statuscode:`400` if ``ACCOUNT_ID`` isn't passed or is already used.

Example Return Value::
   
   <Account id="joeuser@indivo.example.org">
     <fullName>Joe User</fullName>
     <contactEmail>joeuser@gmail.com</contactEmail>
     <lastLoginAt>2010-05-04T15:34:23Z</lastLoginAt>
     <totalLoginCount>43</totalLoginCount>
     <failedLoginCount>0</failedLoginCount>
     <state>active</state>
     <lastStateChange>2009-04-03T13:12:12Z</lastStateChange>
   
     <authSystem name="password" username="joeuser" />
     <authSystem name="hospital_sso" username="Joe_User" />
   </Account>
   


--------

.. http:get:: /accounts/search

   Search for accounts by name or email.

   :shortname: account_search
   :accesscontrol: Any admin app.
   :queryparameter fullname: The full name of the account to search for
   :queryparameter contact_email: The contact email of the account to search for
   :returns: :http:statuscode:`200` with information about matching accounts, or :http:statuscode:`400` if no search parameters are passed.

Example Return Value::
   
   <Accounts>
     <Account id="joeuser@indivo.example.org">
       <fullName>Joe User</fullName>
       <contactEmail>joeuser@gmail.com</contactEmail>
       <lastLoginAt>2010-05-04T15:34:23Z</lastLoginAt>
       <totalLoginCount>43</totalLoginCount>
       <failedLoginCount>0</failedLoginCount>
       <state>active</state>
       <lastStateChange>2009-04-03T13:12:12Z</lastStateChange>
   
       <authSystem name="password" username="joeuser" />
       <authSystem name="hospital_sso" username="Joe_User" />
     </Account>
   
     ...
   
   </Accounts>
   
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}

   Display information about an account.

   :shortname: account_info
   :accesscontrol: Any admin app, or the Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: :http:statuscode:`200` with information about the account

Example Return Value::
   
   <Account id="joeuser@indivo.example.org">
     <fullName>Joe User</fullName>
     <contactEmail>joeuser@gmail.com</contactEmail>
     <lastLoginAt>2010-05-04T15:34:23Z</lastLoginAt>
     <totalLoginCount>43</totalLoginCount>
     <failedLoginCount>0</failedLoginCount>
     <state>active</state>
     <lastStateChange>2009-04-03T13:12:12Z</lastStateChange>
   
     <authSystem name="password" username="joeuser" />
     <authSystem name="hospital_sso" username="Joe_User" />
   </Account>
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/authsystems/

   Add a new method of authentication to an account.

   :shortname: account_authsystem_add
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :formparameter username: The username for this account
   :formparameter password: The password for this account
   :formparameter system: The identifier of the desired authsystem. ``password`` indicates the              internal password system.
   :returns: :http:statuscode:`200 Success`, :http:statuscode:`403` if the indicated auth system doesn't exist, and :http:statuscode:`400` if a system and a username weren't passed, or if the account is already registered with the passed system, or if the username is already taken for the passed authsystem.

Example Return Value::
   
   <ok/>
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/authsystems/password/change

   Change a account's password.

   :shortname: account_password_change
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :formparameter new: The desired new password.
   :formparameter old: The existing account password.
   :returns: :http:statuscode:`200 Success`, :http:statuscode:`403` if the old password didn't validate, or :http:statuscode:`400` if both a new and old password weren't passed.

Example Return Value::
   
   <ok/>
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/authsystems/password/set

   Force the password of an account to a given value.

   :shortname: account_password_set
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :formparameter password: The new password to set.
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`400` if a new password wasn't passed.

Example Return Value::
   
   <ok/>
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/authsystems/password/set-username

   Force the username of an account to a given value.

   :shortname: account_username_set
   :accesscontrol: Any admin app, or the Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :formparameter username: The new username to set.
   :returns: :http:statuscode:`200 Success`, :http:statuscode:`400` if a username wasn't passed.

Example Return Value::
   
   <ok/>
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/check-secrets/{PRIMARY_SECRET}

   Validate an account's primary and secondary secrets.

   :shortname: account_check_secrets
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :parameter PRIMARY_SECRET: A confirmation string sent securely to the patient from Indivo
   :queryparameter secondary_secret: The secondary secret of the account to check.
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`403` if validation fails.

Example Return Value::
   
   <ok/>
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/forgot-password

   Resets an account if the user has forgotten its password.

   :shortname: account_forgot_password
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: :http:statuscode`200` with the account's new secondary secret, or :http:statuscode:`400` if the account hasn't yet been initialized.

Example Return Value::
   
   <secret>123456</secret>
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/inbox/

   List messages in an account's inbox.

   :shortname: account_inbox
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :queryparameter status: The account or document status to filter by
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter include_archive: 0 or 1: whether or not to include archived messages in the result set.
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200`, with a list of inbox messages.

Example Return Value::
   
   <Messages>
     <Message id="879">
       <sender>doctor@example.indivo.org</sender>
       <received_at>2010-09-04T14:12:12Z</received_at>
       <read_at>2010-09-04T17:13:24Z</read_at>
       <subject>your test results are looking good</subject>
       <severity>normal</severity>
       <record id="123" />
       <attachment num="1" type="http://indivo.org/vocab/xml/documents#Lab" size="12546" />
     </Message>
   
     ...
   
   </Messages>
   
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/inbox/

   Send a message to an account.

   :shortname: account_send_message
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :formparameter body: The message body. Defaults to ``[no body]``.
   :formparameter severity: The importance of the message. Options are ``low``, ``medium``, ``high``. Defaults to ``low``.
   :formparameter message_id: An external identifier for the message.
   :formparameter subject: The message subject. Defaults to ``[no subject]``.
   :returns: :http:statuscode:`200 Success`, or http:statuscode:`400` if the passed message_id is a duplicate. Also emails account to alert them that a new message has arrived.

Example Return Value::
   
   <ok/>
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}

   Retrieve an individual message from an account's inbox.

   :shortname: account_inbox_message
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :parameter MESSAGE_ID: The unique identifier of the Indivo Message
   :returns: :http:statuscode:`200`, with XML describing the message.

Example Return Value::
   
   <Message id="879">
     <sender>doctor@example.indivo.org</sender>
     <received_at>2010-09-04T14:12:12Z</received_at>
     <read_at>2010-09-04T17:13:24Z</read_at>
     <archived_at>2010-09-04T17:15:24Z</archived_at>
     <subject>your test results are looking good</subject>
     <body>Great results!
    It seems you'll live forever!</body>
     <severity>normal</severity>
     <record id="123" />
     <attachment num="1" type="http://indivo.org/vocab/xml/documents#Lab" size="12546" />
   </Message>
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}/archive

   Archive a message.

   :shortname: account_message_archive
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :parameter MESSAGE_ID: The unique identifier of the Indivo Message
   :returns: :http:statuscode:`200 Success`.

Example Return Value::
   
   <ok/>
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}/accept

   Accept a message attachment into the record it corresponds to.

   :shortname: account_inbox_message_attachment_accept
   :accesscontrol: The Account owner.
   :parameter ATTACHMENT_NUM: The 1-indexed number corresponding to the message attachment
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :parameter MESSAGE_ID: The unique identifier of the Indivo Message
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`410` if the attachment has already been saved.

Example Return Value::
   
   <ok/>
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/info-set

   Set basic information about an account.

   :shortname: account_info_set
   :accesscontrol: Any admin app, or the Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :formparameter contact_email: A valid email at which to reach the account holder.
   :formparameter full_name: The full name of the account.
   :returns: :http:statuscode:`200`, or :http:statuscode:`400` if no parameters are passed in.

Example Return Value::
   
   <ok/>
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/initialize/{PRIMARY_SECRET}

   Initialize an account, activating it.

   :shortname: account_initialize
   :accesscontrol: Any Indivo UI app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :parameter PRIMARY_SECRET: A confirmation string sent securely to the patient from Indivo
   :formparameter secondary_secret: 
   :returns: :http:statuscode:`200 Success`, :http:statuscode:`403` if the account has already been initialized or if secrets didn't validate, and :http:statuscode:`400` if a secondary secret was required but missing.

Example Return Value::
   
   <ok/>
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/notifications/

   List an account's notifications.

   :shortname: account_notifications
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :queryparameter status: The account or document status to filter by
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of the account's notifications.

Example Return Value::
   
   <Notifications>
     <Notification id="468">
       <sender>labs@apps.indivo.org</sender>
       <received_at>2010-09-03T15:12:12Z</received_at>
       <content>A new lab result has been delivered to your account</content>
       <record id="123" label="Joe User" />
       <document id="579" label="Lab Test 2" />
     </Notification>
   
     ...
   
   </Notifications>
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/permissions/

   List the carenets that an account has access to.

   :shortname: account_permissions
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: :http:statuscode:`200` with a list of carenets.

Example Return Value::
   
   <Carenets record_id="01234">
       <Carenet id="456" name="family" mode="explicit" />
       <Carenet id="567" name="school" mode="explicit" />
   </Carenets>
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/primary-secret

   Display an account's primary secret.

   :shortname: account_primary_secret
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: :http:statuscode:`200`, with the primary secret.

Example Return Value::
   
   <secret>123absxzyasdg13b</secret>
   

.. deprecated:: 1.0.0
   Avoid sending primary secrets over the wire. Instead, use :http:get:`/accounts/{ACCOUNT_EMAIL}/check-secrets/{PRIMARY_SECRET}`.


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/records/

   List all available records for an account.

   :shortname: record_list
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :queryparameter status: The account or document status to filter by
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200`, with a list of records owned or shared with the account.

Example Return Value::
   
   <Records>
     <Record id="123" label="John R. Smith" />
     <Record id="234" label="John R. Smith Jr. (shared)" shared="true" role_label="Guardian" />
     <Record id="345" label="Juanita R. Smith (carenet)" shared="true" carenet_id="678" carenet_name="family" />
   
     ...
   
   </Records>
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/reset

   Reset an account to an ``uninitialized`` state.

   :shortname: account_reset
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: :http:statuscode:`200 Success`.

Example Return Value::
   
   <ok/>
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/secret

   Return the secondary secret of an account.

   :shortname: account_secret
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: :http:statuscode:`200`, with the secondary secret.

Example Return Value::
   
   <secret>123456</secret>
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/secret-resend

   Sends an account user their primary secret in case they lost it.

   :shortname: account_resend_secret
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: :http:statuscode:`200 Success`. Also emails the account with their new secret.

Example Return Value::
   
   <ok/>
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/set-state

   Set the state of an account.

   :shortname: account_set_state
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :formparameter state: The desired state of the account. Options are ``active``, ``disabled``, ``retired``.
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`403` if the account has been retired and can no longer change state.

Example Return Value::
   
   <ok/>
   


--------

.. http:get:: /apps/

   List all available userapps.

   :shortname: all_phas
   :accesscontrol: Any principal in Indivo.
   :returns: :http:statuscode:`200`, with a list of userapps.

Example Return Value::
   
   <Apps>
     <App id="problems@apps.indivo.org">
       <startURLTemplate>http://problems.indivo.org/auth/start?record_id={record_id}&amp;carenet_id={carenet_id}</startURLTemplate>
       <name>Problem List</name>
       <description>Managing your problem list</description>
       <autonomous>false</autonomous>
       <frameable>true</frameable>
       <ui>true</ui>
     </App>
   
     ...
   
   </Apps>
   


--------

.. http:delete:: /apps/{PHA_EMAIL}

   Delete a userapp from Indivo.

   :shortname: pha_delete
   :accesscontrol: The user app itself.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: :http:statuscode:`200 Success`.

Example Return Value::
   
   <ok/>
   


--------

.. http:get:: /apps/{PHA_EMAIL}

   Return a description of a single userapp.

   :shortname: pha
   :accesscontrol: Any principal in Indivo.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: :http:statuscode:`200`, with information about the userapp.

Example Return Value::
   
   <App id="problems@apps.indivo.org">
     <startURLTemplate>http://problems.indivo.org/auth/start?record_id={record_id}&amp;carenet_id={carenet_id}</startURLTemplate>
     <name>Problem List</name>
     <description>Managing your problem list</description>
     <autonomous>false</autonomous>
     <frameable>true</frameable>
     <ui>true</ui>
   </App>
   


--------

.. http:get:: /apps/{PHA_EMAIL}/documents/

   List app-specific documents.

   :shortname: app_document_list
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :queryparameter status: The account or document status to filter by
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter type: The Indivo document type to filter by
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with A list of documents, or http:statuscode:`404` if an invalid type was passed in the querystring.

Example Return Value::
   
   <Documents record_id="" total_document_count="4" pha="problems@apps.indivo.org">
     <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
       <createdAt>2009-05-04T17:05:33</createdAt>
       <creator id="steve@indivo.org" type="account">
         <fullname>Steve Zabak</fullname>
       </creator>
       <suppressedAt>2009-05-06T17:05:33</suppressedAt>
       <suppressor id="steve@indivo.org" type="account">
         <fullname>Steve Zabak</fullname>
       </suppressor>
       <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
       <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
       <label>HBA1C reading</label>
       <status>active</status>
       <nevershare>false</nevershare>
       <relatesTo>
         <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
         <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
       </relatesTo>
       <isRelatedFrom>
         <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
       </isRelatedFrom>
     </Document>
   
     ...
   
   </Documents>
   


--------

.. http:post:: /apps/{PHA_EMAIL}/documents/

   Create an app-specific Indivo document.

   :shortname: app_document_create
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :rawdata: The raw content of the document to create.
   :returns: :http:statuscode:`200` with the metadata of the created document, or :http:statuscode:`400` if the new document failed validation.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading</label>
     <status>active</status>
     <nevershare>false</nevershare>
     <relatesTo>
       <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
       <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
     </relatesTo>
     <isRelatedFrom>
       <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
     </isRelatedFrom>
   </Document>
   


--------

.. http:put:: /apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}

   Create an app-specific Indivo document with an associated external id.

   :shortname: app_document_create_or_update_ext
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :rawdata: The raw content of the document to create.
   :returns: :http:statuscode:`200` with the metadata of the created or updated document, or :http:statuscode:`400` if the passed content didn't validate.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading</label>
     <status>active</status>
     <nevershare>false</nevershare>
   </Document>
   


--------

.. http:get:: /apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}/meta

   Fetch the metadata of an app-specific document identified by external id.

   :shortname: app_document_meta_ext
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: :http:statuscode:`200` with metadata describing the specified document, or http:statuscode:`404` if the external_id is invalid.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="problems@apps.indivo.org" type="pha">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading</label>
     <status>active</status>
     <nevershare>false</nevershare>
   </Document>
   


--------

.. http:delete:: /apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}

   Delete an app-specific document.

   :shortname: app_document_delete
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.

Example Return Value::
   
   </ok>
   


--------

.. http:get:: /apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}

   Retrive an app-specific document.

   :shortname: app_specific_document
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: :http:statuscode:`200` with the raw content of the document, or :http:statuscode:`404` if the document could not be found.

Example Return Value::
   
   <DefaultProblemsPreferences record_id="123">
     <Preference name="hide_void" value="true" />
     <Preference name="show_rels" value="false" />
   </DefaultProblemsPreferences>
   


--------

.. http:put:: /apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}

   Create or Overwrite an app-specific Indivo document.

   :shortname: app_document_create_or_update
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :rawdata: The raw content of the document to create.
   :returns: :http:statuscode:`200` with metadata describing the created or updated document, or :http:statuscode:`400` if the passed content didn't validate.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="problems@apps.indivo.org" type="pha">
     </creator>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading preferences</label>
     <status>active</status>
     <nevershare>false</nevershare>
   </Document>
   


--------

.. http:put:: /apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/label

   Set the label of an app-specific document.

   :shortname: app_document_label
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :rawdata: The new label for the document
   :returns: :http:statuscode:`200` with metadata describing the re-labeled document, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>RELABELED: New HBA1C reading</label>
     <status>active</status>
     <nevershare>false</nevershare>
     <relatesTo>
       <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
       <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
     </relatesTo>
     <isRelatedFrom>
       <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
     </isRelatedFrom>
   </Document>
   


--------

.. http:get:: /apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/meta

   Fetch the metadata of an app-specific document.

   :shortname: app_document_meta
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: :http:statuscode:`200` with the document metadata, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading</label>
     <status>active</status>
     <nevershare>false</nevershare>
     <relatesTo>
       <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
       <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
     </relatesTo>
     <isRelatedFrom>
       <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
     </isRelatedFrom>
   </Document>
   


--------

.. http:delete:: /carenets/{CARENET_ID}

   Delete a carenet.

   :shortname: carenet_delete
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: :http:statuscode:`200 Success`.

Example Return Value::
   
   <ok/>
   


--------

.. http:get:: /carenets/{CARENET_ID}/accounts/

   List the accounts in a carenet.

   :shortname: carenet_account_list
   :accesscontrol: A principal in the carenet, in full control of the carenet's record, or any admin app.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: :http:statuscode:`200` with a list of accounts in the specified carenet.

Example Return Value::
   
   <CarenetAccounts>
     <CarenetAccount id="johndoe@indivo.org" fullName="John Doe" write="true" />
   
     ...
   
   </CarenetAccounts>
   


--------

.. http:post:: /carenets/{CARENET_ID}/accounts/

   Add an account to a carenet.

   :shortname: carenet_account_create
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :formparameter write: ``true`` or ``false``. Whether this account can write to the carenet.
   :formparameter account_id: An identifier for the account. Must be a valid email address.
   :returns: :http:statuscode;`200 Success`, :http:statuscode:`404` if the specified account or carenet don't exist, or :http:statuscode:`400` if an account_id isn't passed.

Example Return Value::
   
   <ok/>
   


--------

.. http:delete:: /carenets/{CARENET_ID}/accounts/{ACCOUNT_ID}

   Remove an account from a carenet.

   :shortname: carenet_account_delete
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter ACCOUNT_ID: The email identifier of the Indivo account
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`404` if either the passed account or the passed carenet doesn't exist.

Example Return Value::
   
   <ok/>
   


--------

.. http:get:: /carenets/{CARENET_ID}/accounts/{ACCOUNT_ID}/permissions

   List the permissions of an account within a carenet.

   :shortname: carenet_account_permissions
   :accesscontrol: A user app with access to the carenet and proxying the account, a principal in full control of the carenet's record, or any admin app.
   :parameter ACCOUNT_ID: The email identifier of the Indivo account
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: :http:statuscode:`200` with a list of document types that the account can access within a carenet. Currently always returns all document types.

Example Return Value::
   
   <Permissions>
     <DocumentType type="*" write="true" />
   </Permissions>
   


--------

.. http:get:: /carenets/{CARENET_ID}/apps/

   List Apps within a given carenet.

   :shortname: carenet_apps_list
   :accesscontrol: A principal in the carenet, in full control of the carenet's record, or any admin app.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: :http:statuscode:`200` with a list of applications in the carenet.

Example Return Value::
   
   <Apps>
     <App id="problems@apps.indivo.org">
       <startURLTemplate>http://problems.indivo.org/auth/start?record_id={record_id}&amp;carenet_id={carenet_id}</startURLTemplate>
       <name>Problem List</name>
       <description>Managing your problem list</description>
       <autonomous>false</autonomous>
       <frameable>true</frameable>
       <ui>true</ui>
     </App>
   
     ...
   
   </Apps>
   


--------

.. http:delete:: /carenets/{CARENET_ID}/apps/{PHA_EMAIL}

   Remove an app from a given carenet.

   :shortname: carenet_apps_delete
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: :http:statuscode:`200 Success`.

Example Return Value::
   
   <ok/>
   


--------

.. http:put:: /carenets/{CARENET_ID}/apps/{PHA_EMAIL}

   Add an app to a carenet

   :shortname: carenet_apps_create
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`400` if the passed PHA is autonomous (autonomous apps can't be scoped to carenets).

Example Return Value::
   
   <ok/>
   


--------

.. http:get:: /carenets/{CARENET_ID}/apps/{PHA_EMAIL}/permissions

   Retrieve the permissions for an app within a carenet. NOT IMPLEMENTED.

   :shortname: carenet_app_permissions
   :accesscontrol: Nobody
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: :http:statuscode:`200`. This call is unimplemented, and has no effect.

Example Return Value::
   
   <ok/>
   

.. todo:: 

   The API Call 'GET /carenets/{0}/apps/{1}/permissions' is not yet implemented.


--------

.. http:get:: /carenets/{CARENET_ID}/documents/

   List documents from a given carenet.

   :shortname: carenet_document_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :queryparameter type: The Indivo document type to filter by
   :returns: :http:statuscode:`200` with a document list on success, :http:statuscode:`404` if *type* doesn't exist.

Example Return Value::
   
   <Documents record_id="123" total_document_count="3" pha="" >
     <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
       <createdAt>2009-05-04T17:05:33</createdAt>
       <creator id="steve@indivo.org" type="account">
         <fullname>Steve Zabak</fullname>
       </creator>
       <suppressedAt>2009-05-06T17:05:33</suppressedAt>
       <suppressor id="steve@indivo.org" type="account">
         <fullname>Steve Zabak</fullname>
       </suppressor>
       <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
       <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
       <label>HBA1C reading</label>
       <status>active</status>
       <nevershare>false</nevershare>
       <relatesTo>
         <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
         <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
       </relatesTo>
       <isRelatedFrom>
         <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
       </isRelatedFrom>
     </Document>
   
     ...
   
   </Documents>
   


--------

.. http:get:: /carenets/{CARENET_ID}/documents/special/{SPECIAL_DOCUMENT}

   Read a special document from a carenet.

   :shortname: read_special_document_carenet
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, an account in the carenet or in control of the record, or the admin app that created the carenet's record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :parameter SPECIAL_DOCUMENT: The type of special document to access. Options are ``demographics``, ``contact``
   :returns: :http:statuscode:`200` with the special document's raw content, or :http:statuscode:`404` if the document hasn't been created yet.

Example Return Value::
   
   <Contact xmlns="http://indivo.org/vocab/xml/documents#">
       <name>
           <fullName>Sebastian Rockwell Cotour</fullName>
           <givenName>Sebastian</givenName>
           <familyName>Cotour</familyName>
       </name>
       <email type="personal">
           scotour@hotmail.com
       </email>
   
       <email type="work">
           sebastian.cotour@childrens.harvard.edu
       </email>
       <address type="home">
           <streetAddress>15 Waterhill Ct.</streetAddress>
           <postalCode>53326</postalCode>
           <locality>New Brinswick</locality>
           <region>Montana</region>
   
           <country>US</country>
           <timeZone>-7GMT</timeZone>
       </address>
       <location type="home">
           <latitude>47N</latitude>
           <longitude>110W</longitude>
       </location>
       <phoneNumber type="home">5212532532</phoneNumber>
       <phoneNumber type="work">6217233734</phoneNumber>
       <instantMessengerName protocol="aim">scotour</instantMessengerName>
   </Contact>
   


--------

.. http:get:: /carenets/{CARENET_ID}/documents/{DOCUMENT_ID}

   Return a document from a carenet.

   :shortname: carenet_document
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: :http:statuscode:`200` with the document content on success, :http:statuscode:`404` if document_id is invalid or if the document is not shared in the carenet.

Example Return Value::
   
   <ExampleDocument>
     <content>That's my content</content>
     <otherField attr="val" />
   </ExampleDocument>
   


--------

.. http:get:: /carenets/{CARENET_ID}/documents/{DOCUMENT_ID}/meta

   Fetch the metadata of a record-specific document via a carenet.

   :shortname: carenet_document_meta
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: :http:statuscode:`200` with the document's metadata, or :http:statuscode:`404` if ``document_id`` doesn't identify an existing document in the carenet.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading</label>
     <status>active</status>
     <nevershare>false</nevershare>
     <relatesTo>
       <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
       <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
     </relatesTo>
     <isRelatedFrom>
       <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
     </isRelatedFrom>
   </Document>
   


--------

.. http:get:: /carenets/{CARENET_ID}/record

   Get basic information about the record to which a carenet belongs.

   :shortname: carenet_record
   :accesscontrol: Nobody
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: :http:statuscode:`200` with XML describing the record.

Example Return Value::
   
   <Record id="123" label="Joe User">
     <contact document_id="790" />
     <demographics document_id="467" />
     <created at="2010-10-23T10:23:34Z" by="indivoconnector@apps.indivo.org" />
   </Record>
   


--------

.. http:post:: /carenets/{CARENET_ID}/rename

   Change a carenet's name.

   :shortname: carenet_rename
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :formparameter name: The new name for the carenet.
   :returns: :http:statuscode:`200` with XML describing the renamed carenet on success, :http:statuscode:`400` if ``name`` wasn't passed or if a carenet named ``name`` already exists on this record.

Example Return Value::
   
   <Carenets record_id="123">
       <Carenet id="789" name="Work/School" mode="explicit" />
   </Carenets>
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/allergies/

   List the allergy data for a given carenet.

   :shortname: carenet_allergy_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of allergies, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
         <Filter name="allergen_name" value="penicillin"/>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#Lab" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <Allergy xmlns="http://indivo.org/vocab/xml/documents#">
           <dateDiagnosed>2009-05-16</dateDiagnosed>
           <diagnosedBy>Children's Hospital Boston</diagnosedBy>
           <allergen>
             <type type="http://codes.indivo.org/codes/allergentypes/" value="drugs">Drugs</type>
             <name type="http://codes.indivo.org/codes/allergens/" value="penicillin">Penicillin</name>
           </allergen>
           <reaction>blue rash</reaction>
           <specifics>this only happens on weekends</specifics>
         </Allergy>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/equipment/

   List the equipment data for a given carenet.

   :shortname: carenet_equipment_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of equipment, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
         <Filter name="allergen_name" value="penicillin"/>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#Lab" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <Equipment xmlns="http://indivo.org/vocab/xml/documents#">
           <dateStarted>2009-02-05</dateStarted>
           <dateStopped>2010-06-12</dateStopped>
           <type>cardiac</type>
           <name>Pacemaker</name>
           <vendor>Acme Medical Devices</vendor>
           <id>167-ABC-23</id>
           <description>it works</description>
           <specification>blah blah blah</specification>
         </Equipment>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/immunizations/

   List the immunization data for a given carenet.

   :shortname: carenet_immunization_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of immunizations, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
         <Filter name="allergen_name" value="penicillin"/>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#Lab" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <Immunization xmlns="http://indivo.org/vocab/xml/documents#">
           <dateAdministered>2009-05-16T12:00:00</dateAdministered>
           <administeredBy>Children's Hospital Boston</administeredBy>
           <vaccine>
             <type type="http://codes.indivo.org/vaccines#" value="hep-B">Hepatitis B</type>
             <manufacturer>Oolong Pharmaceuticals</manufacturer>
             <lot>AZ1234567</lot>
             <expiration>2009-06-01</expiration>
           </vaccine>
           <sequence>2</sequence>
           <anatomicSurface type="http://codes.indivo.org/anatomy/surfaces#" value="shoulder">Shoulder</anatomicSurface>
           <adverseEvent>pain and rash</adverseEvent>
         </Immunization>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/labs/

   List the lab data for a given carenet.

   :shortname: carenet_lab_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of labs, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
         <Filter name="lab_type" value="hematology"/>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#Lab" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <LabReport xmlns="http://indivo.org/vocab/xml/documents#">
           <dateMeasured>1998-07-16T12:00:00Z</dateMeasured>
           <labType>hematology</labType>
           <laboratory>
             <name>Quest</name>
             <address>300 Longwood Ave, Boston MA 02215</address>
           </laboratory>
           <comments>was looking pretty sick</comments>
           <firstPanelName>CBC</firstPanelName>
         </LabReport>
       </Item>
     </Report>
     <Report>
       <Meta>
         <Document id="1b7270a6-5925-450c-9273-5a74386cef63" type="http://indivo.org/vocab/xml/documents#Lab" size="1653" digest="c1be22813ab83f6b3858878a802f372eef754fcdd285e44a5fdb7387d6ee3667" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="1b7270a6-5925-450c-9273-5a74386cef63"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <LabReport xmlns="http://indivo.org/vocab/xml/documents#">
           <dateMeasured>2009-07-16T12:00:00Z</dateMeasured>
           <labType>hematology</labType>
           <laboratory>
             <name>Quest</name>
             <address>300 Longwood Ave, Boston MA 02215</address>
           </laboratory>
           <comments>was looking pretty sick</comments>
           <firstPanelName>CBC</firstPanelName>
         </LabReport>
       </Item>
     </Report>
   </Reports>
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/measurements/{LAB_CODE}/

   List the measurement data for a given carenet.

   :shortname: carenet_measurement_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :parameter LAB_CODE: The identifier corresponding to the measurement being made.
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of measurements, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
         <Filter name="lab_type" value="hematology"/>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#Measurement" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <Measurement id="1234" value="120" type="blood pressure systolic" datetime="2011-03-02T00:00:00Z" unit="mmHg" source_doc="3456" />
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/medications/

   List the medication data for a given carenet.

   :shortname: carenet_medication_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of medications, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#Medication" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <Medication xmlns="http://indivo.org/vocab/xml/documents#">
           <dateStarted>2009-02-05</dateStarted>
           <name type="http://indivo.org/codes/meds#" abbrev="c2i" value="COX2 Inhibitor" />    
           <brandName type="http://indivo.org/codes/meds#" abbrev="vioxx" value="Vioxx" />
           <dose>
             <value>3</value>
             <unit type="http://indivo.org/codes/units#" value="pills" abbrev="p" />
           </dose>
           <route type="http://indivo.org/codes/routes#" value="PO">By Mouth</route>
           <strength>
             <value>100</value>
             <unit type="http://indivo.org/codes/units#" value="mg" abbrev="mg">Milligrams</unit>
           </strength>
           <frequency type="http://indivo.org/codes/frequency#" value="daily">daily</frequency>
   
           <prescription>
             <by>
               <name>Dr. Ken Mandl</name>
               <institution>Children's Hospital Boston</institution>
             </by>
   
             <on>2009-02-01</on>
             <stopOn>2010-01-31</stopOn>
   
             <dispenseAsWritten>true</dispenseAsWritten>
       
             <!-- this duration means 2 months -->
             <duration>P2M</duration>
       
             <!-- does this need more structure? -->
             <refillInfo>once a month for 3 months</refillInfo>
       
             <instructions>don't take them all at once!</instructions>
       
           </prescription>
         </Medication>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/problems/

   List the problem data for a given carenet.

   :shortname: carenet_problem_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of problems, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#Problem" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <Problem xmlns="http://indivo.org/vocab/xml/documents#">
           <dateOnset>2009-05-16T12:00:00</dateOnset>
           <dateResolution>2009-05-16T16:00:00</dateResolution>
           <name type="http://codes.indivo.org/problems/" value="123" abbrev="MI">Myocardial Infarction</name>
           <comments>mild heart attack</comments>
           <diagnosedBy>Dr. Mandl</diagnosedBy>
         </Problem>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/procedures/

   List the procedure data for a given carenet.

   :shortname: carenet_procedure_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of procedures, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#Procedure" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <Procedure xmlns="http://indivo.org/vocab/xml/documents#">
           <datePerformed>2009-05-16T12:00:00</datePerformed>
           <name type="http://codes.indivo.org/procedures#" value="85" abbrev="append">Appendectomy</name>
           <provider>
             <name>Kenneth Mandl</name>
             <institution>Children's Hospital Boston</institution>
           </provider>
         </Procedure>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/simple-clinical-notes/

   List the simple_clinical_notes data for a given carenet.

   :shortname: carenet_simple_clinical_notes_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of notes, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#SimpleClinicalNote" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <SimpleClinicalNote xmlns="http://indivo.org/vocab/xml/documents#">
           <dateOfVisit>2010-02-02T12:00:00Z</dateOfVisit>
           <finalizedAt>2010-02-03T13:12:00Z</finalizedAt>
           <visitType type="http://codes.indivo.org/visit-types#" value="acute">Acute Care</visitType>
           <visitLocation>Longfellow Medical</visitLocation>
           <specialty type="http://codes.indivo.org/specialties#" value="hem-onc">Hematology/Oncology</specialty>
   
           <signature>
             <at>2010-02-03T13:12:00Z</at>    
             <provider>
               <name>Kenneth Mandl</name>
               <institution>Children's Hospital Boston</institution>
             </provider>
           </signature>
   
           <signature>
             <provider>
               <name>Isaac Kohane</name>
               <institution>Children's Hospital Boston</institution>
             </provider>
           </signature>
   
           <chiefComplaint>stomach ache</chiefComplaint>
           <content>Patient presents with ... </content>
         </SimpleClinicalNote>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/vitals/

   List the vitals data for a given carenet.

   :shortname: carenet_vitals_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of notes, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#VitalSign" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <VitalSign xmlns="http://indivo.org/vocab/xml/documents#">
           <dateMeasured>2009-05-16T15:23:21</dateMeasured>
           <name type="http://codes.indivo.org/vitalsigns/" value="123" abbrev="BPsys">Blood Pressure Systolic</name>
           <value>145</value>
           <unit type="http://codes.indivo.org/units/" value="31" abbrev="mmHg">millimeters of mercury</unit>
           <site>left arm</site>
           <position>sitting down</position>
         </VitalSign>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/vitals/{CATEGORY}

   List the vitals data for a given carenet.

   :shortname: carenet_vitals_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CATEGORY: The category of vital sign, i.e. ``weight``, ``Blood_Pressure_Systolic``
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of notes, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#VitalSign" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <VitalSign xmlns="http://indivo.org/vocab/xml/documents#">
           <dateMeasured>2009-05-16T15:23:21</dateMeasured>
           <name type="http://codes.indivo.org/vitalsigns/" value="123" abbrev="BPsys">Blood Pressure Systolic</name>
           <value>145</value>
           <unit type="http://codes.indivo.org/units/" value="31" abbrev="mmHg">millimeters of mercury</unit>
           <site>left arm</site>
           <position>sitting down</position>
         </VitalSign>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /codes/systems/

   List available codingsystems. NOT IMPLEMENTED.

   :shortname: coding_systems_list
   :accesscontrol: Anybody
   :returns: :http:statuscode:`500`, as the system cannot process the call.

Example Return Value::
   
   [{"short_name": "umls-snomed", "name": "UMLS SNOMED", "description" : "..."},
    {..},
    {..}]
   

.. todo:: 

   The API Call 'GET /codes/systems/' is not yet implemented.


--------

.. http:get:: /codes/systems/{SYSTEM_SHORT_NAME}/query

   Query a codingsystem for a value.

   :shortname: coding_system_query
   :accesscontrol: Anybody
   :parameter SYSTEM_SHORT_NAME: 
   :queryparameter q: The query string to search for
   :returns: :http:statuscode:`200` with JSON describing codingsystems entries that matched *q*, or :http:statuscode:`404` if ``SYSTEM_SHORT_NAME`` is invalid.

Example Return Value::
   
   [{"abbreviation": null, "code": "38341003", "consumer_value": null,
     "umls_code": "C0020538",
     "full_value": "Hypertensive disorder, systemic arterial (disorder)"},
    {"abbreviation": null, "code": "55822004", "consumer_value": null,
     "umls_code": "C0020473", "full_value": "Hyperlipidemia (disorder)"}]
   


--------

.. http:post:: /oauth/access_token

   Exchange a request token for a valid access token.

   :shortname: exchange_token
   :accesscontrol: A request signed by a RequestToken.
   :returns: :http:statuscode:`200` with an access token, or :http:statuscode:`403` if the request token didn't validate.

Example Return Value::
   
   oauth_token=abcd1fw3gasdgh3&oauth_token_secret=jgrlhre4291hfjas&xoauth_indivo_record_id=123
   


--------

.. http:post:: /oauth/internal/request_tokens/{REQTOKEN_ID}/approve

   Indicate a user's consent to bind an app to a record or carenet.

   :shortname: request_token_approve
   :accesscontrol: A principal in the carenet to which the request token is restricted (if the token is restricted), or a principal with full control over the record (if the token is not restricted).
   :parameter REQTOKEN_ID: 
   :formparameter record_id: The record to bind to. Either *record_id* or *carenet_id* is required.
   :formparameter carenet_id: The carenet to bind to. Either *record_id* or *carenet_id* is required.
   :returns: :http:statuscode:`200` with a redirect url to the app on success, :http:statuscode:`403` if *record_id*/*carenet_id* don't match *reqtoken*.

Example Return Value::
   
   location=http%3A%2F%2Fapps.indivo.org%2Fproblems%2Fafter_auth%3Foauth_token%3Dabc123%26oauth_verifier%3Dabc123
   
   (which is the urlencoded form of:
   
   http://apps.indivo.org/problems/after_auth?oauth_token=abc123&oauth_verifier=abc123 )
   


--------

.. http:post:: /oauth/internal/request_tokens/{REQTOKEN_ID}/claim

   Claim a request token on behalf of an account.

   :shortname: request_token_claim
   :accesscontrol: Any Account.
   :parameter REQTOKEN_ID: 
   :returns: :http:statuscode:`200` with the email of the claiming principal, or :http:statuscode:`403` if the token has already been claimed.

Example Return Value::
   
   joeuser@indivo.org
   


--------

.. http:get:: /oauth/internal/request_tokens/{REQTOKEN_ID}/info

   Get information about a request token.

   :shortname: request_token_info
   :accesscontrol: Any Account.
   :parameter REQTOKEN_ID: 
   :returns: :http:statuscode:`200` with information about the token.

Example Return Value::
   
   <RequestToken token="XYZ">
     <record id="123" />
     <carenet />
     <kind>new</kind>
     <App id="problems@apps.indivo.org">
       <name>Problem List</name>
       <description>Managing your list of problems</description>
       <autonomous>false</autonomous>
       <frameable>true</frameable>
       <ui>true</ui>
     </App>
   </RequestToken>
   


--------

.. http:post:: /oauth/internal/session_create

   Authenticate a user and register a web session for them.

   :shortname: session_create
   :accesscontrol: Any Indivo UI app.
   :formparameter username: The username of the user to authenticate.
   :formparameter password: The password to use with *username* against the internal password auth system. EITHER *password* or *system* is **Required**.
   :formparameter system: An external auth system to authenticate the user with. EITHER *password* or *system* is **Required**.
   :returns: :http:statuscode:`200` with a valid session token, or :http:statuscode:`403` if the passed credentials were invalid.

Example Return Value::
   
   oauth_token=XYZ&oauth_token_secret=ABC&account_id=joeuser%40indivo.org
   


--------

.. http:get:: /oauth/internal/surl-verify

   Verify a signed URL.

   :shortname: surl_verify
   :accesscontrol: Any Account.
   :queryparameter surl_sig: The computed signature (base-64 encoded sha1) of the url.
   :queryparameter surl_timestamp: when the url was generated. Must be within the past hour.
   :queryparameter surl_token: The access token used to sign the url.
   :returns: :http:statuscode:`200` with XML describing whether the surl validated.

Example Return Value::
   
   If the surl validated:
   
   <result>ok</result>
   
   If the surl was too old:
   
   <result>old</result>
   
   If the surl's signature was invalid:
   
   <result>mismatch</result>
   


--------

.. http:post:: /oauth/request_token

   Get a new request token, bound to a record or carenet if desired.

   :shortname: request_token
   :accesscontrol: Any user app.
   :formparameter indivo_record_id: The record to which to bind the request token. EITHER *indivo_record_id* or *indivo_carenet_id* is **REQUIRED**.
   :formparameter indivo_carenet_id: The carenet to which to bind the request token. EITHER *indivo_record_id* or *indivo_carenet_id* is **REQUIRED**.
   :returns: :http:statuscode:`200` with the request token on success, :http:statuscode:`403` if the oauth signature on the request of missing or faulty.

Example Return Value::
   
   oauth_token=abcd1fw3gasdgh3&oauth_token_secret=jgrlhre4291hfjas&xoauth_indivo_record_id=123
   


--------

.. http:post:: /records/

   Create a new record.

   :shortname: record_create
   :accesscontrol: Any admin app.
   :rawdata: A valid Indivo Contact Document (see :doc:`/schemas/contact-schema`).
   :returns: :http:statuscode:`200` with information about the record on success, :http:statuscode:`400` if the contact XML was empty or invalid.

Example Return Value::
   
   <Record id="123" label="Joe Smith">
     <contact document_id="234" />
     <demographics document_id="" />
   </Record>
   


--------

.. http:put:: /records/external/{PRINCIPAL_EMAIL}/{EXTERNAL_ID}

   Create a new record with an associated external id.

   :shortname: record_create_ext
   :accesscontrol: An admin app with an id matching the principal_email in the URL.
   :parameter PRINCIPAL_EMAIL: The email with which to scope an external id.
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :rawdata: A valid Indivo Contact Document (see :doc:`/schemas/contact-schema`).
   :returns: :http:statuscode:`200` with information about the record on success, :http:statuscode:`400` if the contact XML was empty or invalid.

Example Return Value::
   
   <Record id="123" label="Joe Smith">
     <contact document_id="234" />
     <demographics document_id="" />
   </Record>
   


--------

.. http:get:: /records/{RECORD_ID}

   Get information about an individual record.

   :shortname: record
   :accesscontrol: A principal in full control of the record, the admin app that created the record, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: :http:statuscode:`200` with information about the record.

Example Return Value::
   
   <Record id="123" label="Joe Smith">
     <contact document_id="234" />
     <demographics document_id="346" />
   </Record>
   


--------

.. http:get:: /records/{RECORD_ID}/apps/

   List userapps bound to a given record.

   :shortname: record_phas
   :accesscontrol: A principal in full control of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :queryparameter type: A namespaced document type. If specified, only apps which explicitly declare themselves as supporting that document type will be returned.
   :returns: :http:statuscode:`200` with a list of userapps.

Example Return Value::
   
   <Apps>
     <App id="problems@apps.indivo.org">
       <startURLTemplate>http://problems.indivo.org/auth/start?record_id={record_id}&amp;carenet_id={carenet_id}</startURLTemplate>
       <name>Problem List</name>
       <description>Managing your problem list</description>
       <autonomous>false</autonomous>
       <frameable>true</frameable>
       <ui>true</ui>
     </App>
   
     ...
   
   </Apps>
   


--------

.. http:delete:: /records/{RECORD_ID}/apps/{PHA_EMAIL}

   Remove a userapp from a record.

   :shortname: pha_record_delete
   :accesscontrol: Any admin app, or a principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: :http:statuscode:`200 Success`.

Example Return Value::
   
   <ok/>
   


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}

   Get information about a given userapp bound to a record.

   :shortname: record_pha
   :accesscontrol: A principal in full control of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: :http:statuscode:`200` with information about the app, or :http:statuscode:`404` if the app isn't bound to the record.

Example Return Value::
   
   <App id="problems@apps.indivo.org">
     <startURLTemplate>http://problems.indivo.org/auth/start?record_id={record_id}&amp;carenet_id={carenet_id}</startURLTemplate>
     <name>Problem List</name>
     <description>Managing your problem list</description>
     <autonomous>false</autonomous>
     <frameable>true</frameable>
     <ui>true</ui>
   </App>
   


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/

   List record-app-specific documents.

   :shortname: record_app_document_list
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :queryparameter status: The account or document status to filter by
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter type: The Indivo document type to filter by
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of documents, or :http:statuscode:`404` if an invalid type was passed in the querystring.

Example Return Value::
   
   <Documents record_id="123" total_document_count="4" pha="problems@apps.indivo.org">
     <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
       <createdAt>2009-05-04T17:05:33</createdAt>
       <creator id="steve@indivo.org" type="account">
         <fullname>Steve Zabak</fullname>
       </creator>
       <suppressedAt>2009-05-06T17:05:33</suppressedAt>
       <suppressor id="steve@indivo.org" type="account">
         <fullname>Steve Zabak</fullname>
       </suppressor>
       <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
       <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
       <label>HBA1C reading Preferences</label>
       <status>active</status>
       <nevershare>false</nevershare>
       <relatesTo>
         <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
         <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
       </relatesTo>
       <isRelatedFrom>
         <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
       </isRelatedFrom>
     </Document>
   
     ...
   
   </Documents>
   


--------

.. http:post:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/

   Create a record-app-specific Indivo document.

   :shortname: record_app_document_create
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :rawdata: The raw content of the document to create.
   :returns: :http:statuscode:`200` with the metadata of the created document, or :http:statuscode:`400` if the new document failed validation.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading Preferences</label>
     <status>active</status>
     <nevershare>false</nevershare>
     <relatesTo>
       <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
       <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
     </relatesTo>
     <isRelatedFrom>
       <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
     </isRelatedFrom>
   </Document>
   


--------

.. http:post:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}

   Create or Overwrite a record-app-specific Indivo document with an associated external id.

   :shortname: record_app_document_create_or_update_ext
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :rawdata: The raw content of the document to create/update.
   :returns: :http:statuscode:`200` with metadata describing the created or updated document, or :http:statuscode:`400` if the passed content didn't validate.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="problems@apps.indivo.org" type="pha">
     </creator>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading preferences</label>
     <status>active</status>
     <nevershare>false</nevershare>
   </Document>
   


--------

.. http:put:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}

   Create or Overwrite a record-app-specific Indivo document with an associated external id.

   :shortname: record_app_document_create_or_update_ext
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :rawdata: The raw content of the document to create/update.
   :returns: :http:statuscode:`200` with metadata describing the created or updated document, or :http:statuscode:`400` if the passed content didn't validate.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="problems@apps.indivo.org" type="pha">
     </creator>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading preferences</label>
     <status>active</status>
     <nevershare>false</nevershare>
   </Document>
   


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}/meta

   Fetch the metadata of a record-app-specific document identified by external id.

   :shortname: record_app_document_meta_ext
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: :http:statuscode:`200` with metadata describing the specified document, or http:statuscode:`404` if the external_id is invalid.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="problems@apps.indivo.org" type="pha">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading Preferences</label>
     <status>active</status>
     <nevershare>false</nevershare>
   </Document>
   


--------

.. http:delete:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}

   Delete a record-app-specific document.

   :shortname: record_app_document_delete
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.

Example Return Value::
   
   <ok/>
   


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}

   Retrieve a record-app-specific document.

   :shortname: record_app_specific_document
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: :http:statuscode:`200` with the raw content of the document, or :http:statuscode:`404` if the document could not be found.

Example Return Value::
   
   <ProblemsPreferences record_id="123">
     <Preference name="hide_void" value="true" />
     <Preference name="show_rels" value="false" />
   </ProblemsPreferences>
   


--------

.. http:put:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/label

   Set the label of a record-app-specific document.

   :shortname: record_app_document_label
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :rawdata: The new label for the document
   :returns: :http:statuscode:`200` with metadata describing the re-labeled document, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>RELABELED: New HBA1C reading Preferences</label>
     <status>active</status>
     <nevershare>false</nevershare>
     <relatesTo>
       <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
       <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
     </relatesTo>
     <isRelatedFrom>
       <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
     </isRelatedFrom>
   </Document>
   


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/meta

   Fetch the metadata of a record-app-specific document.

   :shortname: record_app_document_meta
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: :http:statuscode:`200` with the document metadata, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading Preferences</label>
     <status>active</status>
     <nevershare>false</nevershare>
     <relatesTo>
       <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
       <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
     </relatesTo>
     <isRelatedFrom>
       <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
     </isRelatedFrom>
   </Document>
   


--------

.. http:post:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/setup

   Bind an app to a record without user authorization.

   :shortname: record_pha_setup
   :accesscontrol: Any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :rawdata: Raw content that will be used as a setup document for the record. **OPTIONAL**.
   :returns: :http:statuscode:`200` with a valid access token for the newly set up app.

Example Return Value::
   
   oauth_token=abcd1fw3gasdgh3&oauth_token_secret=jgrlhre4291hfjas&xoauth_indivo_record_id=123
   


--------

.. http:get:: /records/{RECORD_ID}/audits/

   Return audits of calls touching *record*.

   :shortname: audit_record_view
   :accesscontrol: A principal in full control of the record, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200`, with a list of Audit Reports.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <Filters>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
       </Meta>
       <Item>
         <AuditEntry>
           <BasicInfo datetime="2011-04-27T17:32:23Z" view_func="get_document" request_successful="true" />
           <PrincipalInfo effective_principal="myapp@apps.indivoheatlh.org" proxied_principal="me@indivohealth.org" />
           <Resources carenet_id="" record_id="123" pha_id="" document_id="234" external_id="" message_id="" />
           <RequestInfo req_url="/records/123/documents/acd/" req_ip_address="127.0.0.1" req_domain="localhost"  req_method="GET" />
           <ResponseInfo resp_code="200" />
         </AuditEntry>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   

.. deprecated:: 0.9.3
   Use :http:get:`/records/{RECORD_ID}/audits/query/` instead.


--------

.. http:get:: /records/{RECORD_ID}/audits/documents/{DOCUMENT_ID}/

   Return audits of calls touching *record* and *document_id*.

   :shortname: audit_document_view
   :accesscontrol: A principal in full control of the record, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200`, with a list of Audit Reports.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <Filters>
         <Filter name="document_id" value="234"/>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
       </Meta>
       <Item>
         <AuditEntry>
           <BasicInfo datetime="2011-04-27T17:32:23Z" view_func="get_document" request_successful="true" />
           <PrincipalInfo effective_principal="myapp@apps.indivoheatlh.org" proxied_principal="me@indivohealth.org" />
           <Resources carenet_id="" record_id="123" pha_id="" document_id="234" external_id="" message_id="" />
           <RequestInfo req_url="/records/123/documents/acd/" req_ip_address="127.0.0.1" req_domain="localhost"  req_method="GET" />
           <ResponseInfo resp_code="200" />
         </AuditEntry>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   

.. deprecated:: 0.9.3
   Use :http:get:`/records/{RECORD_ID}/audits/query/` instead.


--------

.. http:get:: /records/{RECORD_ID}/audits/documents/{DOCUMENT_ID}/functions/{FUNCTION_NAME}/

   Return audits of calls to *function_name* touching *record* and *document_id*.

   :shortname: audit_function_view
   :accesscontrol: A principal in full control of the record, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter FUNCTION_NAME: The internal Indivo function name called by the API request
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200`, with a list of Audit Reports.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <Filters>
         <Filter name="document_id" value="234"/>
         <Filter name="req_view_func" value="record_specific_document"/>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
       </Meta>
       <Item>
         <AuditEntry>
           <BasicInfo datetime="2011-04-27T17:32:23Z" view_func="get_document" request_successful="true" />
           <PrincipalInfo effective_principal="myapp@apps.indivoheatlh.org" proxied_principal="me@indivohealth.org" />
           <Resources carenet_id="" record_id="123" pha_id="" document_id="234" external_id="" message_id="" />
           <RequestInfo req_url="/records/123/documents/acd/" req_ip_address="127.0.0.1" req_domain="localhost"  req_method="GET" />
           <ResponseInfo resp_code="200" />
         </AuditEntry>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   

.. deprecated:: 0.9.3
   Use :http:get:`/records/{RECORD_ID}/audits/query/` instead.


--------

.. http:get:: /records/{RECORD_ID}/audits/query/

   Select Audit Objects via the Query API Interface.

   :shortname: audit_query
   :accesscontrol: A principal in full control of the record, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="created_at*1995-03-10T00:00:00Z*" />
       <Filters>
         <Filter name="document_id" value="234"/>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
       </Meta>
       <Item>
         <AuditEntry>
           <BasicInfo datetime="2011-04-27T17:32:23Z" view_func="get_document" request_successful="true" />
           <PrincipalInfo effective_principal="myapp@apps.indivoheatlh.org" proxied_principal="me@indivohealth.org" />
           <Resources carenet_id="" record_id="123" pha_id="" document_id="234" external_id="" message_id="" />
           <RequestInfo req_url="/records/123/documents/acd/" req_ip_address="127.0.0.1" req_domain="localhost"  req_method="GET" />
           <ResponseInfo resp_code="200" />
         </AuditEntry>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   

.. versionadded:: 0.9.3


--------

.. http:get:: /records/{RECORD_ID}/autoshare/bytype/

   For a single record, list all carenets that a given doctype is autoshared with.

   :shortname: autoshare_list
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :queryparameter type: The document schema type to check autoshares for. **REQUIRED**.
   :returns: :http:statuscode:`200` with a list of carenets, or :http:statuscode:`404` if the passed document type is invalid.

Example Return Value::
   
   <Carenets record_id="123">
     <Carenet id="789" name="Work/School" mode="explicit" />
   
     ...
   
   </Carenets>
   


--------

.. http:get:: /records/{RECORD_ID}/autoshare/bytype/all

   For a single record, list all doctypes autoshared into carenets.

   :shortname: autoshare_list_bytype_all
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: :http:statuscode:`200` with a list of doctypes and their shared carenets.

Example Return Value::
   
   <DocumentSchemas>
     <DocumentSchema type="http://indivo.org/vocab/xml/documents#Medication">
       <Carenet id="123" name="Family" mode="explicit" />
   
       ...
   
     </DocumentSchema>
   
     ...
   
   </DocumentSchemas>
   


--------

.. http:post:: /records/{RECORD_ID}/autoshare/carenets/{CARENET_ID}/bytype/set

   Automatically share all documents of a certain type into a carenet.

   :shortname: autoshare_create
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :formparameter type: the document schema type to create an autoshare for
   :returns: :http:statuscode:`200`, or :http:statuscode:`404` if the passed document type doesn't exist.

Example Return Value::
   
   <ok/>
   


--------

.. http:post:: /records/{RECORD_ID}/autoshare/carenets/{CARENET_ID}/bytype/unset

   Remove an autoshare from a carenet.

   :shortname: autoshare_delete
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :formparameter type: the document schema type to remove an autoshare for
   :returns: :http:statuscode:`200`, or :http:statuscode:`404` if the passed document type doesn't exist.

Example Return Value::
   
   <ok/>
   


--------

.. http:get:: /records/{RECORD_ID}/carenets/

   List all carenets for a record.

   :shortname: carenet_list
   :accesscontrol: A principal in full control of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: :http:statuscode:`200`, with a list of carenets.

Example Return Value::
   
   <Carenets record_id="123">
     <Carenet id="789" name="Work/School" mode="explicit" />
   
     ...
   
   </Carenets>
   


--------

.. http:post:: /records/{RECORD_ID}/carenets/

   Create a new carenet for a record.

   :shortname: carenet_create
   :accesscontrol: A principal in full control of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :formparameter name: The label for the new carenet.
   :returns: :http:statuscode:`200` with a description of the new carenet, or :http:statuscode:`400` if the name of the carenet wasn't passed or already exists.

Example Return Value::
   
   <Carenets record_id="123">
     <Carenet id="789" name="Work/School" mode="explicit" />
   </Carenets>
   


--------

.. http:delete:: /records/{RECORD_ID}/documents/

   Delete all documents associated with a record.

   :shortname: documents_delete
   :accesscontrol: Nobody
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: :http:statuscode:`200 Success`

Example Return Value::
   
   <ok/>
   


--------

.. http:get:: /records/{RECORD_ID}/documents/

   List record-specific documents.

   :shortname: record_document_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :queryparameter status: The account or document status to filter by
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter type: The Indivo document type to filter by
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of documents, or :http:statuscode:`404` if an invalid type was passed in the querystring.

Example Return Value::
   
   <Documents record_id="123" total_document_count="4">
     <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
       <createdAt>2009-05-04T17:05:33</createdAt>
       <creator id="steve@indivo.org" type="account">
         <fullname>Steve Zabak</fullname>
       </creator>
       <suppressedAt>2009-05-06T17:05:33</suppressedAt>
       <suppressor id="steve@indivo.org" type="account">
         <fullname>Steve Zabak</fullname>
       </suppressor>
       <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
       <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
       <label>HBA1C reading</label>
       <status>active</status>
       <nevershare>false</nevershare>
       <relatesTo>
         <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
         <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
       </relatesTo>
       <isRelatedFrom>
         <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
       </isRelatedFrom>
     </Document>
   
     ...
   
   </Documents>
   


--------

.. http:post:: /records/{RECORD_ID}/documents/

   Create a record-specific Indivo Document.

   :shortname: document_create
   :accesscontrol: A user app with access to the record, a principal in full control of the record, or the admin app that created the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :rawdata: The raw content of the document to create.
   :returns: :http:statuscode:`200` with the metadata of the created document, or :http:statuscode:`400` if the new document failed validation.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading</label>
     <status>active</status>
     <nevershare>false</nevershare>
     <relatesTo>
       <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
       <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
     </relatesTo>
     <isRelatedFrom>
       <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
     </isRelatedFrom>
   </Document>
   


--------

.. http:put:: /records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}

   Create a record-specific Indivo Document with an associated external id.

   :shortname: document_create_by_ext_id
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :rawdata: The raw content of the document to create.
   :returns: :http:statuscode:`200` with the metadata of the created document, or :http:statuscode:`400` if the new document failed validation, or if the external id was taken.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading</label>
     <status>active</status>
     <nevershare>false</nevershare>
     <relatesTo>
       <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
       <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
     </relatesTo>
     <isRelatedFrom>
       <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
     </isRelatedFrom>
   </Document>
   


--------

.. http:put:: /records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}/label

   Set the label of a record-specific document, specified by external id.

   :shortname: record_document_label_ext
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :rawdata: The new label for the document
   :returns: :http:statuscode:`200` with metadata describing the re-labeled document, or :http:statuscode:`404` if ``EXTERNAL_ID`` is invalid.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>RELABELED: New HBA1C reading</label>
     <status>active</status>
     <nevershare>false</nevershare>
     <relatesTo>
       <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
       <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
     </relatesTo>
     <isRelatedFrom>
       <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
     </isRelatedFrom>
   </Document>
   


--------

.. http:get:: /records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}/meta

   Fetch the metadata of a record-specific document identified by external id.

   :shortname: record_document_meta_ext
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: :http:statuscode:`200` with the document metadata, or :http:statuscode:`404` if ``EXTERNAL_ID`` is invalid.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading</label>
     <status>active</status>
     <nevershare>false</nevershare>
     <relatesTo>
       <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
       <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
     </relatesTo>
     <isRelatedFrom>
       <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
     </isRelatedFrom>
   </Document>
   


--------

.. http:get:: /records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}

   Read a special document from a record.

   :shortname: read_special_document
   :accesscontrol: A user app with access to the record, a principal in full control of the record, or the admin app that created the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter SPECIAL_DOCUMENT: The type of special document to access. Options are ``demographics``, ``contact``
   :returns: :http:statuscode:`200` with the special document's raw content, or :http:statuscode:`404` if the document hasn't been created yet.

Example Return Value::
   
   <Contact xmlns="http://indivo.org/vocab/xml/documents#">
       <name>
           <fullName>Sebastian Rockwell Cotour</fullName>
           <givenName>Sebastian</givenName>
           <familyName>Cotour</familyName>
       </name>
       <email type="personal">
           scotour@hotmail.com
       </email>
   
       <email type="work">
           sebastian.cotour@childrens.harvard.edu
       </email>
       <address type="home">
           <streetAddress>15 Waterhill Ct.</streetAddress>
           <postalCode>53326</postalCode>
           <locality>New Brinswick</locality>
           <region>Montana</region>
   
           <country>US</country>
           <timeZone>-7GMT</timeZone>
       </address>
       <location type="home">
           <latitude>47N</latitude>
           <longitude>110W</longitude>
       </location>
       <phoneNumber type="home">5212532532</phoneNumber>
       <phoneNumber type="work">6217233734</phoneNumber>
       <instantMessengerName protocol="aim">scotour</instantMessengerName>
   </Contact>
   


--------

.. http:post:: /records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}

   Create or update a special document on a record.

   :shortname: save_special_document
   :accesscontrol: A user app with access to the record, a principal in full control of the record, or the admin app that created the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter SPECIAL_DOCUMENT: The type of special document to access. Options are ``demographics``, ``contact``
   :rawdata: The raw content of the document to create.
   :returns: :http:statuscode:`200` with metadata on the updated document, or :http:statuscode:`400` if the new content didn't validate.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="http://indivo.org/vocab/xml/documents#Contact" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>Contacts</label>
     <status>active</status>
     <nevershare>false</nevershare>
   </Document>
   


--------

.. http:put:: /records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}

   Create or update a special document on a record.

   :shortname: save_special_document
   :accesscontrol: A user app with access to the record, a principal in full control of the record, or the admin app that created the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter SPECIAL_DOCUMENT: The type of special document to access. Options are ``demographics``, ``contact``
   :rawdata: The raw content of the document to create.
   :returns: :http:statuscode:`200` with metadata on the updated document, or :http:statuscode:`400` if the new content didn't validate.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="http://indivo.org/vocab/xml/documents#Contact" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>Contacts</label>
     <status>active</status>
     <nevershare>false</nevershare>
   </Document>
   


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID_0}/rels/{REL}/{DOCUMENT_ID_1}

   Create a new relationship between two existing documents.

   :shortname: document_rels
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID_1: The id of the document that is the subject of the relationship, i.e. DOCUMENT_ID_1 *annotates* DOCUMENT_ID_0
   :parameter DOCUMENT_ID_0: The id of the document that is the object of the relationship, i.e. DOCUMENT_ID_0 *is annotated by* DOCUMENT_ID_1
   :parameter REL: The type of relationship between the documents, i.e. ``annotation``, ``interpretation``
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`404` if ``DOCUMENT_ID_0``, ``DOCUMENT_ID_1``, or ``REL`` don't exist.

Example Return Value::
   
   <ok/>
   


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}

   Retrieve a record-specific document.

   :shortname: record_specific_document
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: :http:statuscode:`200` with the raw content of the document, or :http:statuscode:`404` if the document could not be found.

Example Return Value::
   
   <HBA1C xmlns="http://indivo.org/vocab#" value="5.3" unit="percent" datetime="2011-01-15T17:00:00.000Z" />
   


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/

   List all the carenets into which a document has been shared.

   :shortname: document_carenets
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: :http:statuscode:`200` with a list of carenets.

Example Return Value::
   
   <Carenets record_id="123">
     <Carenet id="789" name="Work/School" mode="explicit" />
   
     ...
   
   </Carenets>
   


--------

.. http:delete:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}

   Unshare a document from a given carenet.

   :shortname: carenet_document_delete
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid or if either the passed carenet or document do not belong to the passed record.

Example Return Value::
   
   <ok/>
   


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}

   Place a document into a given carenet.

   :shortname: carenet_document_placement
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid or nevershared.

Example Return Value::
   
   <ok/>
   


--------

.. http:post:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}/autoshare-revert

   Revert the document-sharing of a document in a carent to whatever rules are specified by autoshares. NOT IMPLEMENTED.

   :shortname: autoshare_revert
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: :http:statuscode:`200 Success`.

Example Return Value::
   
   <ok/>
   

.. todo:: 

   The API Call 'POST /records/{0}/documents/{1}/carenets/{2}/autoshare-revert' is not yet implemented.


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/label

   Set the label of a record-specific document.

   :shortname: record_document_label
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :rawdata: The new label for the document
   :returns: :http:statuscode:`200` with metadata describing the re-labeled document, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>RELABELED: New HBA1C reading</label>
     <status>active</status>
     <nevershare>false</nevershare>
     <relatesTo>
       <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
       <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
     </relatesTo>
     <isRelatedFrom>
       <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
     </isRelatedFrom>
   </Document>
   


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/meta

   Fetch the metadata of a record-specific document.

   :shortname: record_document_meta
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: :http:statuscode:`200` with the document metadata, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading</label>
     <status>active</status>
     <nevershare>false</nevershare>
     <relatesTo>
       <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
       <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
     </relatesTo>
     <isRelatedFrom>
       <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
     </isRelatedFrom>
   </Document>
   


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/meta

   Set metadata fields on a document. NOT IMPLEMENTED.

   :shortname: update_document_meta
   :accesscontrol: Nobody
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: :http:statuscode:`200 Success`.

Example Return Value::
   
   <ok/>
   

.. todo:: 

   The API Call 'PUT /records/{0}/documents/{1}/meta' is not yet implemented.


--------

.. http:delete:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/nevershare

   Remove the nevershare flag from a document.

   :shortname: document_remove_nevershare
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.

Example Return Value::
   
   <ok/>
   


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/nevershare

   Flag a document to never be shared, anywhere.

   :shortname: document_set_nevershare
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.

Example Return Value::
   
   <ok/>
   


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/

   Get all documents related to the passed document_id by a relation of the passed relation-type.

   :shortname: get_documents_by_rel
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter REL: The type of relationship between the documents, i.e. ``annotation``, ``interpretation``
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :queryparameter status: The account or document status to filter by.
   :queryparameter limit: See :ref:`query-operators`. **CURRENTLY UNIMPLEMENTED**.
   :queryparameter order_by: See :ref:`query-operators`. **CURRENTLY UNIMPLEMENTED**.
   :queryparameter offset: See :ref:`query-operators`. **CURRENTLY UNIMPLEMENTED**
   :returns: :http:statuscode:`200` with a list of related documents, or :http:statuscode:`400` if ``DOCUMENT_ID`` is invalid.

Example Return Value::
   
   <Documents record_id="123" total_document_count="4">
     <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
       <createdAt>2009-05-04T17:05:33</createdAt>
       <creator id="steve@indivo.org" type="account">
         <fullname>Steve Zabak</fullname>
       </creator>
       <suppressedAt>2009-05-06T17:05:33</suppressedAt>
       <suppressor id="steve@indivo.org" type="account">
         <fullname>Steve Zabak</fullname>
       </suppressor>
       <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
       <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
       <label>HBA1C reading</label>
       <status>active</status>
       <nevershare>false</nevershare>
       <relatesTo>
         <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
         <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
       </relatesTo>
       <isRelatedFrom>
         <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
       </isRelatedFrom>
     </Document>
   
     ...
   
   </Documents>
   


--------

.. http:post:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/

   Create a document and relate it to an existing document.

   :shortname: document_create_by_rel
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter REL: The type of relationship between the documents, i.e. ``annotation``, ``interpretation``
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :rawdata: The raw content of the document to create.
   :returns: :http:statuscode:`200 Success`, :http:statuscode:`400` if the new content was invalid, or :http:statuscode:`404` if ``DOCUMENT_ID`` or ``REL`` are invalid.

Example Return Value::
   
   <ok/>
   


--------

.. http:post:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/external/{PHA_EMAIL}/{EXTERNAL_ID}

   Create a document, assign it an external id, and relate it to an existing document.

   :shortname: document_create_by_rel_with_ext_id
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter REL: The type of relationship between the documents, i.e. ``annotation``, ``interpretation``
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :rawdata: The raw content of the document to create.
   :returns: :http:statuscode:`200 Success`, :http:statuscode:`400` if the new content was invalid, or :http:statuscode:`404` if ``DOCUMENT_ID`` or ``REL`` are invalid.

Example Return Value::
   
   <ok/>
   


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/external/{PHA_EMAIL}/{EXTERNAL_ID}

   Create a document, assign it an external id, and relate it to an existing document.

   :shortname: document_create_by_rel_with_ext_id
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter REL: The type of relationship between the documents, i.e. ``annotation``, ``interpretation``
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :rawdata: The raw content of the document to create.
   :returns: :http:statuscode:`200 Success`, :http:statuscode:`400` if the new content was invalid, or :http:statuscode:`404` if ``DOCUMENT_ID`` or ``REL`` are invalid.

Example Return Value::
   
   <ok/>
   


--------

.. http:post:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/replace

   Create a new version of a record-specific document.

   :shortname: document_version
   :accesscontrol: A user app with access to the record, a principal in full control of the record, or the admin app that created the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :rawdata: The raw content of the document to create.
   :returns: :http:statuscode:`200` with metadata on the new document, :http:statuscode:`400` if the old document has already been replaced by a newer version, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid or if the new content is invalid.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <replaces id="abe8130e2-ba54-1234-eeef-45a3b6cd9a8e" />
     <original id="abe8130e2-ba54-1234-eeef-45a3b6cd9a8e" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading</label>
     <status>active</status>
     <nevershare>false</nevershare>
     <relatesTo>
       <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
       <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
     </relatesTo>
     <isRelatedFrom>
       <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
     </isRelatedFrom>
   </Document>
   


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/replace/external/{PHA_EMAIL}/{EXTERNAL_ID}

   Create a new version of a record-specific document and assign it an external id.

   :shortname: document_version_by_ext_id
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :rawdata: The raw content of the document to create.
   :returns: :http:statuscode:`200` with metadata on the new document, :http:statuscode:`400` if the old document has already been replaced by a newer version, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid or if the new content is invalid.

Example Return Value::
   
   <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
     <createdAt>2009-05-04T17:05:33</createdAt>
     <creator id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </creator>
     <suppressedAt>2009-05-06T17:05:33</suppressedAt>
     <suppressor id="steve@indivo.org" type="account">
       <fullname>Steve Zabak</fullname>
     </suppressor>
     <replaces id="abe8130e2-ba54-1234-eeef-45a3b6cd9a8e" />
     <original id="abe8130e2-ba54-1234-eeef-45a3b6cd9a8e" />
     <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
     <label>HBA1C reading</label>
     <status>active</status>
     <nevershare>false</nevershare>
     <relatesTo>
       <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
       <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
     </relatesTo>
     <isRelatedFrom>
       <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
     </isRelatedFrom>
   </Document>
   


--------

.. http:post:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/set-status

   Set the status of a record-specific document.

   :shortname: document_set_status
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :formparameter status: The new status for the document. Options are ``active``, ``void``, ``archived``.
   :formparameter reason: The reason for the status change.
   :returns: :http:statuscode:`200 Success`, :http:statuscode:`400` if *status* or *reason* are missing, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.

Example Return Value::
   
   <ok/>
   


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/status-history

   List all changes to a document's status over time.

   :shortname: document_status_history
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: :http:statuscode:`200` with a the document's status history, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.

Example Return Value::
   
   <DocumentStatusHistory document_id="456">
     <DocumentStatus by="joeuser@indivo.example.org" at="2010-09-03T12:45:12Z" status="archived">
       <reason>no longer relevant</reason>
     </DocumentStatus>
   
     ...
   
   </DocumentStatusHistory>
   


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/versions/

   Retrieve the versions of a document.

   :shortname: document_versions
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :queryparameter status: The account or document status to filter by.
   :queryparameter limit: See :ref:`query-operators`.
   :queryparameter order_by: See :ref:`query-operators`.
   :queryparameter offset: See :ref:`query-operators`.
   :returns: :http:statuscode:`200` with a list of document versions, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.

Example Return Value::
   
   <Documents record_id="123" total_document_count="4">
     <Document id="14c81023-c84f-496d-8b8e-9438280441d3" type="" digest="7e9bc09276e0829374fd810f96ed98d544649703db3a9bc231550a0b0e5bcb1c" size="77">
       <createdAt>2009-05-04T17:05:33</createdAt>
       <creator id="steve@indivo.org" type="account">
         <fullname>Steve Zabak</fullname>
       </creator>
       <suppressedAt>2009-05-06T17:05:33</suppressedAt>
       <suppressor id="steve@indivo.org" type="account">
         <fullname>Steve Zabak</fullname>
       </suppressor>
       <original id="14c81023-c84f-496d-8b8e-9438280441d3" />
       <latest id="14c81023-c84f-496d-8b8e-9438280441d3" createdAt="2009-05-05T17:05:33" createdBy="steve@indivo.org" />
       <label>HBA1C reading</label>
       <status>active</status>
       <nevershare>false</nevershare>
       <relatesTo>
         <relation type="http://indivo.org/vocab/documentrels#attachment" count="1" />
         <relation type="http://indivo.org/vocab/documentrels#annotation" count="5" />
       </relatesTo>
       <isRelatedFrom>
         <relation type="http://indivo.org/vocab/documentrels#interpretation" count="1" />
       </isRelatedFrom>
     </Document>
   
     ...
   
   </Documents>
   


--------

.. http:post:: /records/{RECORD_ID}/inbox/{MESSAGE_ID}

   Send a message to a record.

   :shortname: record_send_message
   :accesscontrol: Any admin app, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter MESSAGE_ID: The unique identifier of the Indivo Message
   :formparameter body: The message body. Defaults to ``[no body]``.
   :formparameter body_type: The formatting for the message body. Options are ``plaintext``, ``markdown``. Defaults to ``plaintext``.
   :formparameter num_attachments: The number of attachments this message requires. Attachments are uploaded with calls to :http:post:`/records/{RECORD_ID}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}`. Defaults to 0.
   :formparameter severity: The importance of the message. Options are ``low``, ``medium``, ``high``. Defaults to ``low``.
   :formparameter subject: The message subject. Defaults to ``[no subject]``.
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`400` if ``MESSAGE_ID`` was a duplicate. Also triggers notification emails to accounts authorized to view messages for the passed record.

Example Return Value::
   
   <ok/>
   


--------

.. http:post:: /records/{RECORD_ID}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}

   Attach a document to an Indivo message.

   :shortname: record_message_attach
   :accesscontrol: Any admin app, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter ATTACHMENT_NUM: The 1-indexed number corresponding to the message attachment
   :parameter MESSAGE_ID: The unique identifier of the Indivo Message
   :rawdata: The raw XML attachment data.
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`400` if ``ATTACHMENT_NUM`` has already been uploaded.

Example Return Value::
   
   <ok/>
   


--------

.. http:post:: /records/{RECORD_ID}/notifications/

   Send a notification about a record to all accounts authorized to be notified.

   :shortname: record_notify
   :accesscontrol: Any admin app, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :formparameter content: The plaintext content of the notification.
   :formparameter app_url: A callback url to the app for more information. **OPTIONAL**.
   :formparameter document_id: The id of the document to which this notification pertains. **OPTIONAL**.
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`400` if *content* wasn't passed.

Example Return Value::
   
   <ok/>
   


--------

.. http:post:: /records/{RECORD_ID}/notify

   Send a notification about a record to all accounts authorized to be notified.

   :shortname: record_notify
   :accesscontrol: Any admin app, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :formparameter content: The plaintext content of the notification.
   :formparameter app_url: A callback url to the app for more information. **OPTIONAL**.
   :formparameter document_id: The id of the document to which this notification pertains. **OPTIONAL**.
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`400` if *content* wasn't passed.

Example Return Value::
   
   <ok/>
   

.. deprecated:: 1.0
   Use :http:post:`/records/{RECORD_ID}/notifications/` instead.


--------

.. http:get:: /records/{RECORD_ID}/owner

   Get the owner of a record.

   :shortname: record_get_owner
   :accesscontrol: A principal in full control of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: :http:statuscode:`200 Success.`

Example Return Value::
   
   <Account id='joeuser@example.com' />
   


--------

.. http:post:: /records/{RECORD_ID}/owner

   Set the owner of a record.

   :shortname: record_set_owner
   :accesscontrol: Any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :rawdata: The email address of the new account owner.
   :returns: :http:statuscode:`200` with information about the account, or :http:statuscode:`400` if the passed email address is invalid.

Example Return Value::
   
   <Account id="joeuser@indivo.example.org">
     <fullName>Joe User</fullName>
     <contactEmail>joeuser@gmail.com</contactEmail>
     <lastLoginAt>2010-05-04T15:34:23Z</lastLoginAt>
     <totalLoginCount>43</totalLoginCount>
     <failedLoginCount>0</failedLoginCount>
     <state>active</state>
     <lastStateChange>2009-04-03T13:12:12Z</lastStateChange>
   
     <authSystem name="password" username="joeuser" />
     <authSystem name="hospital_sso" username="Joe_User" />
   </Account>
   


--------

.. http:put:: /records/{RECORD_ID}/owner

   Set the owner of a record.

   :shortname: record_set_owner
   :accesscontrol: Any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :rawdata: The email address of the new account owner.
   :returns: :http:statuscode:`200` with information about the account, or :http:statuscode:`400` if the passed email address is invalid.

Example Return Value::
   
   <Account id="joeuser@indivo.example.org">
     <fullName>Joe User</fullName>
     <contactEmail>joeuser@gmail.com</contactEmail>
     <lastLoginAt>2010-05-04T15:34:23Z</lastLoginAt>
     <totalLoginCount>43</totalLoginCount>
     <failedLoginCount>0</failedLoginCount>
     <state>active</state>
     <lastStateChange>2009-04-03T13:12:12Z</lastStateChange>
   
     <authSystem name="password" username="joeuser" />
     <authSystem name="hospital_sso" username="Joe_User" />
   </Account>
   


--------

.. http:get:: /records/{RECORD_ID}/reports/experimental/ccr

   Export patient data as a Continuity of Care Record (CCR) document.

   :shortname: report_ccr
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: :http:statuscode:`200` with an **EXPERIMENTAL** CCR document.

Example Return Value::
   
   <ContinuityOfCareRecord xmlns="urn:astm-org:CCR">
     <CCRDocumentObjectID>0</CCRDocumentObjectID>
     <Language>
       <Text>ENGLISH</Text>
     </Language>
     <Version>V1.0</Version>
     <DateTime>
       <Type>
         <Text>Create</Text>
         <ObjectAttribute>
           <Attribute>DisplayDate</Attribute>
           <AttributeValue>
             <Value>09/30/10</Value>
           </AttributeValue>
         </ObjectAttribute>
       </Type>
       <ExactDateTime>2010-05-04T15:34:23Z</ExactDateTime>
     </DateTime>
     <Patient>
       <ActorID>123</ActorID>
     </Patient>
     <From>
       <ActorLink/>
     </From>
     <Body>
       <Medications>
         <Medication>
   	<CCRDataObjectID>789</CCRDataObjectID>
   	<DateTime>
   	  <Type>
   	    <Text>Dispense date</Text>
   	  </Type>
   	  <ExactDateTime>2010-05-04T15:34:23Z</ExactDateTime>
   	</DateTime>
   	<Status>
   	  <Text>Active</Text>
   	</Status>
   	<Product>
   	  <ProductName>
   	    <Text>Vioxx</Text>
   	    <Code>
   	      <Value>C1234</Value>
   	      <CodingSystem>RxNorm</CodingSystem>
   	    </Code>
   	  </ProductName>
   	  <Strength>
   	    <Value>20</Value>
   	    <Units>
   	      <Unit>mg</Unit>
   	    </Units>
   	  </Strength>
   	</Product>
   	<Directions>
             <Direction>
               <Dose>
                 <Value>1</Value>
                 <Units>
   		<Unit>Pills</Unit>
                 </Units>
               </Dose>
               <Route>
                 <Text>Oral</Text>
               </Route>
               <Frequency>
                 <Value>1QR</Value>
               </Frequency>
             </Direction>
   	</Directions>
         </Medication>
   
         ...
   
       </Medications>
       <Immunizations>
         <Immunization>
           <CCRDataObjectID>567</CCRDataObjectID>
   	<DateTime>
             <Type>
               <Text>Start date</Text>
             </Type>
   	  <ExactDateTime>2010-05-04T15:34:23Z</ExactDateTime>
   	</DateTime>
         <Product>
           <ProductName>
             <Text>Rubella</Text>
             <Code>
               <Value>C1345</Value>
               <CodingSystem>HL7 Vaccines</CodingSystem>
             </Code>
           </ProductName>
         </Product>
         </Immunization>
   
         ...
   
       </Immunizations>
       <VitalSigns>
   
       ...
   
       </VitalSigns>
   
       ...
   
     </Body>
     <Actors>
     </Actors>
   </ContinuityOfCareRecord>
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/allergies/

   List the allergy data for a given record.

   :shortname: allergy_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of allergies, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
         <Filter name="allergen_name" value="penicillin"/>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#Lab" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <Allergy xmlns="http://indivo.org/vocab/xml/documents#">
           <dateDiagnosed>2009-05-16</dateDiagnosed>
           <diagnosedBy>Children's Hospital Boston</diagnosedBy>
           <allergen>
             <type type="http://codes.indivo.org/codes/allergentypes/" value="drugs">Drugs</type>
             <name type="http://codes.indivo.org/codes/allergens/" value="penicillin">Penicillin</name>
           </allergen>
           <reaction>blue rash</reaction>
           <specifics>this only happens on weekends</specifics>
         </Allergy>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/equipment/

   List the equipment data for a given record.

   :shortname: equipment_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of equipment, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
         <Filter name="allergen_name" value="penicillin"/>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#Lab" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <Equipment xmlns="http://indivo.org/vocab/xml/documents#">
           <dateStarted>2009-02-05</dateStarted>
           <dateStopped>2010-06-12</dateStopped>
           <type>cardiac</type>
           <name>Pacemaker</name>
           <vendor>Acme Medical Devices</vendor>
           <id>167-ABC-23</id>
           <description>it works</description>
           <specification>blah blah blah</specification>
         </Equipment>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/immunizations/

   List the immunization data for a given record.

   :shortname: immunization_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of immunizations, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
         <Filter name="allergen_name" value="penicillin"/>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#Lab" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <Immunization xmlns="http://indivo.org/vocab/xml/documents#">
           <dateAdministered>2009-05-16T12:00:00</dateAdministered>
           <administeredBy>Children's Hospital Boston</administeredBy>
           <vaccine>
             <type type="http://codes.indivo.org/vaccines#" value="hep-B">Hepatitis B</type>
             <manufacturer>Oolong Pharmaceuticals</manufacturer>
             <lot>AZ1234567</lot>
             <expiration>2009-06-01</expiration>
           </vaccine>
           <sequence>2</sequence>
           <anatomicSurface type="http://codes.indivo.org/anatomy/surfaces#" value="shoulder">Shoulder</anatomicSurface>
           <adverseEvent>pain and rash</adverseEvent>
         </Immunization>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/labs/

   List the lab data for a given record.

   :shortname: lab_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of labs, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
         <Filter name="lab_type" value="hematology"/>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#Lab" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <LabReport xmlns="http://indivo.org/vocab/xml/documents#">
           <dateMeasured>1998-07-16T12:00:00Z</dateMeasured>
           <labType>hematology</labType>
           <laboratory>
             <name>Quest</name>
             <address>300 Longwood Ave, Boston MA 02215</address>
           </laboratory>
           <comments>was looking pretty sick</comments>
           <firstPanelName>CBC</firstPanelName>
         </LabReport>
       </Item>
     </Report>
     <Report>
       <Meta>
         <Document id="1b7270a6-5925-450c-9273-5a74386cef63" type="http://indivo.org/vocab/xml/documents#Lab" size="1653" digest="c1be22813ab83f6b3858878a802f372eef754fcdd285e44a5fdb7387d6ee3667" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="1b7270a6-5925-450c-9273-5a74386cef63"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <LabReport xmlns="http://indivo.org/vocab/xml/documents#">
           <dateMeasured>2009-07-16T12:00:00Z</dateMeasured>
           <labType>hematology</labType>
           <laboratory>
             <name>Quest</name>
             <address>300 Longwood Ave, Boston MA 02215</address>
           </laboratory>
           <comments>was looking pretty sick</comments>
           <firstPanelName>CBC</firstPanelName>
         </LabReport>
       </Item>
     </Report>
   </Reports>
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/measurements/{LAB_CODE}/

   List the measurement data for a given record.

   :shortname: measurement_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter LAB_CODE: The identifier corresponding to the measurement being made.
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of measurements, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
         <Filter name="lab_type" value="hematology"/>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#Measurement" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <Measurement id="1234" value="120" type="blood pressure systolic" datetime="2011-03-02T00:00:00Z" unit="mmHg" source_doc="3456" />
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/medications/

   List the medication data for a given record.

   :shortname: medication_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of medications, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#Medication" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <Medication xmlns="http://indivo.org/vocab/xml/documents#">
           <dateStarted>2009-02-05</dateStarted>
           <name type="http://indivo.org/codes/meds#" abbrev="c2i" value="COX2 Inhibitor" />    
           <brandName type="http://indivo.org/codes/meds#" abbrev="vioxx" value="Vioxx" />
           <dose>
             <value>3</value>
             <unit type="http://indivo.org/codes/units#" value="pills" abbrev="p" />
           </dose>
           <route type="http://indivo.org/codes/routes#" value="PO">By Mouth</route>
           <strength>
             <value>100</value>
             <unit type="http://indivo.org/codes/units#" value="mg" abbrev="mg">Milligrams</unit>
           </strength>
           <frequency type="http://indivo.org/codes/frequency#" value="daily">daily</frequency>
   
           <prescription>
             <by>
               <name>Dr. Ken Mandl</name>
               <institution>Children's Hospital Boston</institution>
             </by>
   
             <on>2009-02-01</on>
             <stopOn>2010-01-31</stopOn>
   
             <dispenseAsWritten>true</dispenseAsWritten>
       
             <!-- this duration means 2 months -->
             <duration>P2M</duration>
       
             <!-- does this need more structure? -->
             <refillInfo>once a month for 3 months</refillInfo>
       
             <instructions>don't take them all at once!</instructions>
       
           </prescription>
         </Medication>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/problems/

   List the problem data for a given record.

   :shortname: problem_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of problems, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#Problem" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <Problem xmlns="http://indivo.org/vocab/xml/documents#">
           <dateOnset>2009-05-16T12:00:00</dateOnset>
           <dateResolution>2009-05-16T16:00:00</dateResolution>
           <name type="http://codes.indivo.org/problems/" value="123" abbrev="MI">Myocardial Infarction</name>
           <comments>mild heart attack</comments>
           <diagnosedBy>Dr. Mandl</diagnosedBy>
         </Problem>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/procedures/

   List the procedure data for a given record.

   :shortname: procedure_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of procedures, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#Procedure" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <Procedure xmlns="http://indivo.org/vocab/xml/documents#">
           <datePerformed>2009-05-16T12:00:00</datePerformed>
           <name type="http://codes.indivo.org/procedures#" value="85" abbrev="append">Appendectomy</name>
           <provider>
             <name>Kenneth Mandl</name>
             <institution>Children's Hospital Boston</institution>
           </provider>
         </Procedure>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/simple-clinical-notes/

   List the simple_clinical_notes data for a given record.

   :shortname: simple_clinical_notes_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of notes, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#SimpleClinicalNote" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <SimpleClinicalNote xmlns="http://indivo.org/vocab/xml/documents#">
           <dateOfVisit>2010-02-02T12:00:00Z</dateOfVisit>
           <finalizedAt>2010-02-03T13:12:00Z</finalizedAt>
           <visitType type="http://codes.indivo.org/visit-types#" value="acute">Acute Care</visitType>
           <visitLocation>Longfellow Medical</visitLocation>
           <specialty type="http://codes.indivo.org/specialties#" value="hem-onc">Hematology/Oncology</specialty>
   
           <signature>
             <at>2010-02-03T13:12:00Z</at>    
             <provider>
               <name>Kenneth Mandl</name>
               <institution>Children's Hospital Boston</institution>
             </provider>
           </signature>
   
           <signature>
             <provider>
               <name>Isaac Kohane</name>
               <institution>Children's Hospital Boston</institution>
             </provider>
           </signature>
   
           <chiefComplaint>stomach ache</chiefComplaint>
           <content>Patient presents with ... </content>
         </SimpleClinicalNote>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/vitals/

   List the vitals data for a given record.

   :shortname: vitals_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of notes, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#VitalSign" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <VitalSign xmlns="http://indivo.org/vocab/xml/documents#">
           <dateMeasured>2009-05-16T15:23:21</dateMeasured>
           <name type="http://codes.indivo.org/vitalsigns/" value="123" abbrev="BPsys">Blood Pressure Systolic</name>
           <value>145</value>
           <unit type="http://codes.indivo.org/units/" value="31" abbrev="mmHg">millimeters of mercury</unit>
           <site>left arm</site>
           <position>sitting down</position>
         </VitalSign>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/vitals/{CATEGORY}/

   List the vitals data for a given record.

   :shortname: vitals_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter CATEGORY: The category of vital sign, i.e. ``weight``, ``Blood_Pressure_Systolic``
   :queryparameter status: The account or document status to filter by
   :queryparameter {FIELD}: See :ref:`query-operators`
   :queryparameter date_group: See :ref:`query-operators`
   :queryparameter group_by: See :ref:`query-operators`
   :queryparameter order_by: See :ref:`query-operators`
   :queryparameter aggregate_by: See :ref:`query-operators`
   :queryparameter date_range: See :ref:`query-operators`
   :queryparameter limit: See :ref:`query-operators`
   :queryparameter offset: See :ref:`query-operators`
   :returns: :http:statuscode:`200` with a list of notes, or :http:statuscode:`400` if any invalid query parameters were passed.

Example Return Value::
   
   <Reports xmlns="http://indivo.org/vocab/xml/documents#">
     <Summary total_document_count="2" limit="100" offset="0" order_by="date_measured" />
     <QueryParams>
       <DateRange value="date_measured*1995-03-10T00:00:00Z*" />
       <Filters>
       </Filters>
     </QueryParams>
     <Report>
       <Meta>
         <Document id="261ca370-927f-41af-b001-7b615c7a468e" type="http://indivo.org/vocab/xml/documents#VitalSign" size="1653" digest="0799971784e5a2d199cd6585415a8cd57f7bf9e4f8c8f74ef67a1009a1481cd6" record_id="">
           <createdAt>2011-05-02T17:48:13Z</createdAt>
           <creator id="mymail@mail.ma" type="Account">
             <fullname>full name</fullname>
           </creator>
           <original id="261ca370-927f-41af-b001-7b615c7a468e"/>
           <label>testing</label>
           <status>active</status>
           <nevershare>false</nevershare>
         </Document>
       </Meta>
       <Item>
         <VitalSign xmlns="http://indivo.org/vocab/xml/documents#">
           <dateMeasured>2009-05-16T15:23:21</dateMeasured>
           <name type="http://codes.indivo.org/vitalsigns/" value="123" abbrev="BPsys">Blood Pressure Systolic</name>
           <value>145</value>
           <unit type="http://codes.indivo.org/units/" value="31" abbrev="mmHg">millimeters of mercury</unit>
           <site>left arm</site>
           <position>sitting down</position>
         </VitalSign>
       </Item>
     </Report>
   
     ...
   
   </Reports>
   


--------

.. http:get:: /records/{RECORD_ID}/shares/

   List the shares of a record.

   :shortname: record_shares
   :accesscontrol: The owner of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: :http:statuscode:`200` with a list of shares.

Example Return Value::
   
   <Shares record="123">
     <Share id="678" account="joeuser@example.com" />
     <Share id="789" pha="problems@apps.indivo.org" />
   
     ...
   
   </Shares>
   


--------

.. http:post:: /records/{RECORD_ID}/shares/

   Fully share a record with another account.

   :shortname: record_share_add
   :accesscontrol: The owner of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :formparameter account_id: The email address of the recipient account. **REQUIRED**.
   :formparameter role_label: A label for the share, usually the relationship between the owner and the recipient (i.e. ``Guardian``). **OPTIONAL**.
   :returns: :http:statuscode:`200 Success`, :http:statuscode:`400` if *account_id* was not passed, or :http:statuscode:`404` if the passed *account_id* was invalid.

Example Return Value::
   
   <ok/>
   


--------

.. http:delete:: /records/{RECORD_ID}/shares/{OTHER_ACCOUNT_ID}

   Undo a full record share with an account.

   :shortname: record_share_delete
   :accesscontrol: The owner of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter OTHER_ACCOUNT_ID: The email identifier of the Indivo account to share with
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`404` if ``OTHER_ACCOUNT_ID`` is invalid.

Example Return Value::
   
   <ok/>
   


--------

.. http:post:: /records/{RECORD_ID}/shares/{OTHER_ACCOUNT_ID}/delete

   Undo a full record share with an account.

   :shortname: record_share_delete
   :accesscontrol: The owner of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter OTHER_ACCOUNT_ID: The email identifier of the Indivo account to share with
   :returns: :http:statuscode:`200 Success`, or :http:statuscode:`404` if ``OTHER_ACCOUNT_ID`` is invalid.

Example Return Value::
   
   <ok/>
   

.. deprecated:: 1.0
   Use :http:delete:`/records/{RECORD_ID}/shares/{OTHER_ACCOUNT_ID}` instead.


--------

.. http:get:: /version

   Return the current version of Indivo.

   :shortname: get_version
   :accesscontrol: Any principal in Indivo.
   :returns: :http:statuscode:`200` with the current version of Indivo.

Example Return Value::
   
   1.0.0.0
   
