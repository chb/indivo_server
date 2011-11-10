
API Reference
=============

This page contains a full list of valid Indivo API calls, generated from the code.
For a more detailed walkthrough of individual calls, see :doc:`api`


--------

.. http:post:: /accounts/

   Create a new account.
   
       request.POST holds the creation arguments. 
   
       Required Parameters:
   
       * *account_id*: an identifier for the new address. Must be formatted
         as an email address.
   
       Optional Parameters:
   
       * *full_name*: The full name to associate with the account. Defaults
         to the empty string.
   
       * *contact_email*: A valid email at which the account holder can 
         be reached. Defaults to the *account_id* parameter.
   
       * *primary_secret_p*: ``0`` or ``1``. Whether or not to associate 
         a primary secret with the account. Defaults to ``0``.
   
       * *secondary_secret_p*: ``0`` or ``1``. Whether or not to associate
         a secondary secret with the account. Defaults to ``1``.
   
       After creating the new account, this call generates secrets for it,
       and then emails the user (at *contact_email*) with their activation
       link, which contains the primary secret.
   
       This call will return :http:statuscode:`200` with info about the new
       account on success, :http:statuscode:`400` if *account_id* isn't 
       provided or isn't a valid email address, or if an account already
       exists with an id matching *account_id*.

   :shortname: account_create
   :accesscontrol: Any admin app.
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /accounts/search

   Search for accounts by name or email.
   
       request.GET must contain the query parameters, any of:
       
       * *fullname*: The full name of the account
       
       * *contact_email*: The contact email for the account.
   
       This call returns only accounts matching all passed 
       query parameters exactly: there is no partial matching
       or text-search.
   
       Will return :http:statuscode:`200` with XML describing
       matching accounts on success, :http:statuscode:`400` if
       no query parameters are passed.

   :shortname: account_search
   :accesscontrol: Any admin app.
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}

   Display information about an account.
   
       Return information includes the account's secondary-secret,
       full name, contact email, login counts, state, and auth 
       systems.
   
       Will return :http:statuscode:`200` on success, with account info
       XML.

   :shortname: account_info
   :accesscontrol: Any admin app, or the Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/authsystems/

   Add a new method of authentication to an account.
   
       Accounts cannot be logged into unless there exists a
       mechanism for authenticating them. Indivo supports one
       built-in mechanism, password auth, but is extensible with
       other mechanisms (i.e., LDAP, etc.). If an external mechanism 
       is used, a UI app is responsible for user authentication, and 
       this call merely registers with indivo server the fact that 
       the UI can handle auth. If password auth is used, this call 
       additionally registers the password with indivo server.
       Thus, this call can be used to add internal or external auth 
       systems.
   
       request.POST must contain:
   
       * *system*: The identifier (a short slug) associated with the
         desired auth system. ``password`` identifies the internal
         password system, and external auth systems will define their
         own identifiers.
   
       * *username*: The username that this account will use to 
         authenticate against the new authsystem
         
       * *password*: The password to pair with the username.
         **ONLY REQUIRED IF THE AUTH SYSTEM IS THE INTERNAL
         PASSWORD SYSTEM**.
   
       Will return :http:statuscode:`200` on success, 
       :http:statuscode:`403` if the indicated auth system doesn't exist,
       and :http:statuscode:`400` if the POST data didn't contain a system
       and a username (and a password if system was ``password``), or if
       the account is already registered for the given authsystem, or a 
       different account is already registered for the given authsystem with
       the same username.

   :shortname: account_authsystem_add
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/authsystems/password/change

   Change a account's password.
   
       request.POST must contain:
       
       * *old*: The existing account password.
       * *new*: The desired new password.
   
       Will return :http:statuscode:`200` on success,
       :http:statuscode:`403` if the old password didn't
       validate, :http:statuscode:`400` if the POST data
       didn't contain both an old password and a new one.

   :shortname: account_password_change
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/authsystems/password/set

   Force the password of an account to a given value.
   
       This differs from 
       :py:meth:`~indivo_server.indivo.views.account.account_password_change`
       in that it does not require validation of the old password. This
       function is therefore admin-facing, whereas 
       :py:meth:`~indivo_server.indivo.views.account.acount_password_change` 
       is user-facing.
   
       request.POST must contain:
       
       * *password*: The new password to set.
   
       Will return :http:statuscode:`200` on success, :http:statuscode:`400`
       if the passed POST data didn't contain a new password.

   :shortname: account_password_set
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/authsystems/password/set-username

   Force the username of an account to a given value.
   
       request.POST must contain:
   
       * *username*: The new username to set.
   
       Will return :http:statuscode:`200` on success, 
       :http:statuscode:`400` if the POST data doesn't conatain
       a new username.

   :shortname: account_username_set
   :accesscontrol: Any admin app, or the Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/check-secrets/{PRIMARY_SECRET}

   Validate an account's primary and secondary secrets.
   
       If the secondary secret is to be validated, request.GET must
       contain:
   
       * *secondary_secret*: The account's secondary secret.
   
       This call will validate the prmary secret, and the secondary
       secret if passed.
   
       Will return :http:statuscode:`200` on success, 
       :http:statuscode:`403` if either validation fails.

   :shortname: account_check_secrets
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :parameter PRIMARY_SECRET: A confirmation string sent securely to the patient from Indivo
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/forgot-password

   Resets an account if the user has forgotten its password.
   
       This is a convenience call which encapsulates
       :py:meth:`~indivo_server.indivo.views.account.account_reset`, 
       :py:meth:`~indivo_server.indivo.views.account.account_resend_secret`, and
       :py:meth:`~indivo_server.indivo.views.account.account_secret`. In summary,
       it resets the account to an uninitialized state, emails
       the user with a new primary-secret, and returns the
       secondary secret for display.
   
       Will return :http:statuscode:`200` with the secondary secret
       on success, :http:statuscode:`400` if the account hasn't yet
       been initialized and couldn't possibly need a reset. If the
       account has no associated secondary secret, the return XML
       will be empty.

   :shortname: account_forgot_password
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/inbox/

   

   :shortname: account_inbox
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/inbox/

   account messages have no attachments for now

   :shortname: account_send_message
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}

   

   :shortname: account_inbox_message
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :parameter MESSAGE_ID: The unique identifier of the Indivo Message
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}/archive

   set a message's archival date as now, unless it's already set

   :shortname: account_message_archive
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :parameter MESSAGE_ID: The unique identifier of the Indivo Message
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}/accept

   

   :shortname: account_inbox_message_attachment_accept
   :accesscontrol: The Account owner.
   :parameter ATTACHMENT_NUM: The 1-indexed number corresponding to the message attachment
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :parameter MESSAGE_ID: The unique identifier of the Indivo Message
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/info-set

   Set basic information about an account.
   
       request.POST can contain any of:
   
       * *contact_email*: A new contact email for the account.
   
       * *full_name*: A new full name for the account.
   
       Each passed parameter will be updated for the account.
   
       Will return :http:statuscode:`200` on success, 
       :http:statuscode:`400` if the POST data contains none of
       the settable parameters.

   :shortname: account_info_set
   :accesscontrol: Any admin app, or the Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/initialize/{PRIMARY_SECRET}

   Initialize an account, activating it.
   
       After validating primary and secondary secrets, changes the 
       account's state from ``uninitialized`` to ``active`` and sends
       a welcome email to the user.
   
       If the account has an associated secondary secret, request.POST 
       must contain:
   
       * *secondary_secret*: The secondary_secret generated for the account.
   
       Will return :http:statuscode:`200` on success, :http:statuscode:`403`
       if the account has already been initialized or if either of the account
       secrets didn't validate, and :http:statuscode:`400` if a secondary secret
       was required, but didn't appear in the POST data.

   :shortname: account_initialize
   :accesscontrol: Any Indivo UI app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :parameter PRIMARY_SECRET: A confirmation string sent securely to the patient from Indivo
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/notifications/

   

   :shortname: account_notifications
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/permissions/

   Retrieve the permissions of a given account across all carenets

   :shortname: account_permissions
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/primary-secret

   Display an account's primary secret.
   
       This is an admin-facing call, and should be used sparingly,
       as we would like to avoid sending primary-secrets over the
       wire. If possible, use 
       :py:meth:`~indivo_server.indivo.views.account.account_check_secrets`
       instead.
   
       Will return :http:statuscode:`200` with the primary secret on success.

   :shortname: account_primary_secret
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/records/

   A list of records available for a given account

   :shortname: record_list
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/reset

   Reset an account to an ``uninitialized`` state.
   
       Just calls into :py:meth:`~indivo_server.indivo.models.accounts.Account.reset`.
   
       Will return :http:statuscode:`200` on success.

   :shortname: account_reset
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/secret

   Return the secondary secret of an account.
   
       Will always return :http:statuscode:`200`. If the account 
       has no associated secondary secret, the return XML will
       be empty.

   :shortname: account_secret
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/secret-resend

   Sends an account user their primary secret in case they lost it.
   
       Will return :http:statuscode:`200` on success.

   :shortname: account_resend_secret
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/set-state

   Set the state of an account. 
   
       request.POST must contain:
       
       * *state*: The desired new state of the account.
   
       Options are: 
       
       * ``active``: The account is ready for use.
       
       * ``disabled``: The account has been disabled,
         and cannot be logged into.
         
       * ``retired``: The account has been permanently
         disabled, and will never allow login again.
         Retired accounts cannot be set to any other 
         state.
   
       Will return :http:statuscode:`200` on success,
       :http:statuscode:`403` if the account has been
       retired.

   :shortname: account_set_state
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /apps/

   A list of the PHAs as JSON

   :shortname: all_phas
   :accesscontrol: Any principal in Indivo.
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:delete:: /apps/{PHA_EMAIL}

   

   :shortname: pha_delete
   :accesscontrol: The user app itself.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /apps/{PHA_EMAIL}

   

   :shortname: pha
   :accesscontrol: Any principal in Indivo.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /apps/{PHA_EMAIL}/documents/

   For 1:1 mapping of URLs to views. Calls document_list

   :shortname: app_document_list
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /apps/{PHA_EMAIL}/documents/

   For 1:1 mapping from views: calls document_create_or_update()

   :shortname: app_document_create
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}

   For 1:1 mapping from views: calls document_create_or_update()

   :shortname: app_document_create_or_update_ext
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}/meta

   For 1:1 mapping of URLs to views. Calls _document_meta

   :shortname: app_document_meta_ext
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:delete:: /apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}

   Delete an application specific document: no restrictions, since this storage is 
     managed by the app.

   :shortname: app_document_delete
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}

   Retrive an app-specific document: calls document()

   :shortname: app_specific_document
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}

   For 1:1 mapping from views: calls document_create_or_update()

   :shortname: app_document_create_or_update
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/label

   For a 1:1 mapping of URLs to views: calls document_label

   :shortname: app_document_label
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/meta

   For 1:1 mapping of URLs to views. Calls _document_meta

   :shortname: app_document_meta
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:delete:: /carenets/{CARENET_ID}

   

   :shortname: carenet_delete
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/accounts/

   List the accounts of a given carenet

   :shortname: carenet_account_list
   :accesscontrol: A principal in the carenet, in full control of the carenet's record, or any admin app.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /carenets/{CARENET_ID}/accounts/

   Link an account to a given carenet
     write=false or write=true

   :shortname: carenet_account_create
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:delete:: /carenets/{CARENET_ID}/accounts/{ACCOUNT_ID}

   Unlink an account from a given carenet

   :shortname: carenet_account_delete
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter ACCOUNT_ID: The email identifier of the Indivo account
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/accounts/{ACCOUNT_ID}/permissions

   Retrieve the permissions of a given account within a given carenet

   :shortname: carenet_account_permissions
   :accesscontrol: A user app with access to the carenet and proxying the account, a principal in full control of the carenet's record, or any admin app.
   :parameter ACCOUNT_ID: The email identifier of the Indivo account
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/apps/

   List Apps within a given carenet

   :shortname: carenet_apps_list
   :accesscontrol: A principal in the carenet, in full control of the carenet's record, or any admin app.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:delete:: /carenets/{CARENET_ID}/apps/{PHA_EMAIL}

   Add app to a given carenet
     read/write ability is determined by the user who uses the app, not by the app itself.

   :shortname: carenet_apps_delete
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /carenets/{CARENET_ID}/apps/{PHA_EMAIL}

   Add app to a given carenet
     read/write ability is determined by the user who uses the app, not by the app itself.

   :shortname: carenet_apps_create
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/apps/{PHA_EMAIL}/permissions

   Retrieve the permissions for an app within a carenet

   :shortname: carenet_app_permissions
   :accesscontrol: 
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/documents/

   List documents from a given carenet
   
       Return both documents in the given carenet and 
       documents with the same types as in the record's autoshare

   :shortname: carenet_document_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/documents/special/{SPECIAL_DOCUMENT}

   Read a special document from a carenet

   :shortname: read_special_document_carenet
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, an account in the carenet or in control of the record, or the admin app that created the carenet's record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :parameter SPECIAL_DOCUMENT: The type of special document to access. Options are ``demographics``, ``contact``
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/documents/{DOCUMENT_ID}

   Return a document given a record and carenet id
   
       Return the document if it is in the given carenet or 
       its type is in the record's autoshare

   :shortname: carenet_document
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/documents/{DOCUMENT_ID}/meta

   For 1:1 mapping of URLs to views. Calls _document_meta

   :shortname: carenet_document_meta
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/record

   Basic record information within a carenet
   
     For now, just the record label

   :shortname: carenet_record
   :accesscontrol: 
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /carenets/{CARENET_ID}/rename

   

   :shortname: carenet_rename
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/allergies/

   For 1:1 mapping of URLs to views. Calls _allergy_list

   :shortname: carenet_allergy_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/equipment/

   For 1:1 mapping of URLs to views. Calls _equipment_list

   :shortname: carenet_equipment_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/immunizations/

   For 1:1 mapping of URLs to views: calls _immunization_list

   :shortname: carenet_immunization_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/labs/

   For 1:1 mapping of URLs to views. Calls _lab_list

   :shortname: carenet_lab_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/measurements/{LAB_CODE}/

   For 1:1 mapping of URLs to views: calls _measurement_list

   :shortname: carenet_measurement_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :parameter LAB_CODE: The identifier corresponding to the measurement being made.
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/medications/

   For 1:1 mapping of URLs to views: calls _medication_list

   :shortname: carenet_medication_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/problems/

   For 1:1 mapping of URLs to views: calls _problem_list

   :shortname: carenet_problem_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/procedures/

   For 1:1 mapping of URLs to views: calls _procedure_list

   :shortname: carenet_procedure_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/simple-clinical-notes/

   For 1:1 mapping of URLs to views. Calls _simple_clinical_notes_list

   :shortname: carenet_simple_clinical_notes_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/vitals/

   For 1:1 mapping from URLs to views: calls _vitals_list

   :shortname: carenet_vitals_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/vitals/{CATEGORY}

   For 1:1 mapping from URLs to views: calls _vitals_list

   :shortname: carenet_vitals_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CATEGORY: The category of vital sign, i.e. ``weight``, ``Blood_Pressure_Systolic``
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /codes/systems/

   

   :shortname: coding_systems_list
   :accesscontrol: 
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /codes/systems/{SYSTEM_SHORT_NAME}/query

   

   :shortname: coding_system_query
   :accesscontrol: 
   :parameter SYSTEM_SHORT_NAME: 
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /oauth/access_token

   

   :shortname: exchange_token
   :accesscontrol: A request signed by a RequestToken.
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /oauth/internal/request_tokens/{REQTOKEN_ID}/approve

   

   :shortname: request_token_approve
   :accesscontrol: A principal in the carenet to which the request token is restricted (if the token is restricted), or a principal with full control over the record (if the token is not restricted).
   :parameter REQTOKEN_ID: 
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /oauth/internal/request_tokens/{REQTOKEN_ID}/claim

   

   :shortname: request_token_claim
   :accesscontrol: Any Account.
   :parameter REQTOKEN_ID: 
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /oauth/internal/request_tokens/{REQTOKEN_ID}/info

   get info about the request token

   :shortname: request_token_info
   :accesscontrol: Any Account.
   :parameter REQTOKEN_ID: 
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /oauth/internal/session_create

   

   :shortname: session_create
   :accesscontrol: Any Indivo UI app.
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /oauth/internal/surl-verify

   Verifies a signed URL
     
     The URL should contain a bunch of GET parameters, including
     - surl_timestamp
     - surl_token
     - surl_sig
     which are used to verify the rest of the URL

   :shortname: surl_verify
   :accesscontrol: Any Account.
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /oauth/request_token

   the request-token request URL

   :shortname: request_token
   :accesscontrol: Any user app.
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/

   For 1:1 mapping of URLs to views: calls _record_create

   :shortname: record_create
   :accesscontrol: Any admin app.
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /records/external/{PRINCIPAL_EMAIL}/{EXTERNAL_ID}

   For 1:1 mapping of URLs to views: calls _record_create

   :shortname: record_create_ext
   :accesscontrol: An admin app with an id matching the principal_email in the URL.
   :parameter PRINCIPAL_EMAIL: 
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}

   

   :shortname: record
   :accesscontrol: A principal in full control of the record, the admin app that created the record, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/apps/

   

   :shortname: record_phas
   :accesscontrol: A principal in full control of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:delete:: /records/{RECORD_ID}/apps/{PHA_EMAIL}

   

   :shortname: pha_record_delete
   :accesscontrol: Any admin app, or a principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}

   

   :shortname: record_pha
   :accesscontrol: A principal in full control of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/

   For 1:1 mapping of URLs to views. Calls document_list

   :shortname: record_app_document_list
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/

   For 1:1 mapping from views: calls document_create_or_update()

   :shortname: record_app_document_create
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}

   For 1:1 mapping from views: calls document_create_or_update()

   :shortname: record_app_document_create_or_update_ext
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}

   For 1:1 mapping from views: calls document_create_or_update()

   :shortname: record_app_document_create_or_update_ext
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}/meta

   For 1:1 mapping of URLs to views. Calls _document_meta

   :shortname: record_app_document_meta_ext
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:delete:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}

   Delete a record-application specific document: no restrictions, since this storage is 
     managed by the app.

   :shortname: record_app_document_delete
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}

   Retrieve a record-app-specific document: calls document()

   :shortname: record_app_specific_document
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/label

   For a 1:1 mapping of URLs to views: calls document_label

   :shortname: record_app_document_label
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/meta

   For 1:1 mapping of URLs to views. Calls _document_meta

   :shortname: record_app_document_meta
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/setup

   Set up a PHA in a record ahead of time
   
     FIXME: eventually, when there are permission restrictions on a PHA, make sure that
     any permission restrictions on the current PHA are transitioned accordingly

   :shortname: record_pha_setup
   :accesscontrol: Any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/audits/

   

   :shortname: audit_record_view
   :accesscontrol: A principal in full control of the record, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/audits/documents/{DOCUMENT_ID}/

   

   :shortname: audit_document_view
   :accesscontrol: A principal in full control of the record, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/audits/documents/{DOCUMENT_ID}/functions/{FUNCTION_NAME}/

   

   :shortname: audit_function_view
   :accesscontrol: A principal in full control of the record, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter FUNCTION_NAME: The internal Indivo function name called by the API request
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/audits/query/

   Select Audit Objects via the Query API Interface

   :shortname: audit_query
   :accesscontrol: A principal in full control of the record, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/autoshare/bytype/

   

   :shortname: autoshare_list
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/autoshare/bytype/all

   provide all of the autoshares, grouped by type

   :shortname: autoshare_list_bytype_all
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/autoshare/carenets/{CARENET_ID}/bytype/set

   

   :shortname: autoshare_create
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/autoshare/carenets/{CARENET_ID}/bytype/unset

   

   :shortname: autoshare_delete
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/carenets/

   

   :shortname: carenet_list
   :accesscontrol: A principal in full control of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/carenets/

   POST to /records/{record_id}/carenets/
       Must have a 'name' key/value pair and the name must not yet be used by this record

   :shortname: carenet_create
   :accesscontrol: A principal in full control of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:delete:: /records/{RECORD_ID}/documents/

   

   :shortname: documents_delete
   :accesscontrol: 
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/documents/

   For 1:1 mapping of URLs to views. Calls document_list

   :shortname: record_document_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/documents/

   Create a document, possibly with the given external_id
     This call is ONLY made on NON-app-specific data,
     so the PHA argument is non-null only for specifying an external_id

   :shortname: document_create
   :accesscontrol: A user app with access to the record, a principal in full control of the record, or the admin app that created the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}

   Create a document with the given external_id
     Same as document_create: this function exists
     to preserve the 1:1 mapping from functions to views

   :shortname: document_create_by_ext_id
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}/label

   For a 1:1 mapping of URLs to views: calls document_label

   :shortname: record_document_label_ext
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}/meta

   For 1:1 mapping of URLs to views. Calls _document_meta

   :shortname: record_document_meta_ext
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}

   Read a special document from a record.

   :shortname: read_special_document
   :accesscontrol: A user app with access to the record, a principal in full control of the record, or the admin app that created the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter SPECIAL_DOCUMENT: The type of special document to access. Options are ``demographics``, ``contact``
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}

   Save a new special document

   :shortname: save_special_document
   :accesscontrol: A user app with access to the record, a principal in full control of the record, or the admin app that created the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter SPECIAL_DOCUMENT: The type of special document to access. Options are ``demographics``, ``contact``
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}

   Save a new special document

   :shortname: save_special_document
   :accesscontrol: A user app with access to the record, a principal in full control of the record, or the admin app that created the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter SPECIAL_DOCUMENT: The type of special document to access. Options are ``demographics``, ``contact``
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID_0}/rels/{REL}/{DOCUMENT_ID_1}

   create a new document relationship between existing docs.
     2010-08-15: removed external_id and pha parameters as they are never set.
     That's for create_by_rel

   :shortname: document_rels
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID_1: The id of the document that is the subject of the relationship, i.e. DOCUMENT_ID_1 *annotates* DOCUMENT_ID_0
   :parameter DOCUMENT_ID_0: The id of the document that is the object of the relationship, i.e. DOCUMENT_ID_0 *is annotated by* DOCUMENT_ID_1
   :parameter REL: The type of relationship between the documents, i.e. ``annotation``, ``interpretation``
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}

   Retrieve a record-specific document: calls document()

   :shortname: record_specific_document
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/

   List all the carenets for a given document
   
       This view retrieves all the carenets in which  a given 
       document has been placed

   :shortname: document_carenets
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:delete:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}

   Delete a document into a given carenet

   :shortname: carenet_document_delete
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}

   Place a document into a given carenet

   :shortname: carenet_document_placement
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}/autoshare-revert

   

   :shortname: autoshare_revert
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/label

   For a 1:1 mapping of URLs to views: calls document_label

   :shortname: record_document_label
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/meta

   For 1:1 mapping of URLs to views. Calls _document_meta

   :shortname: record_document_meta
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/meta

   

   :shortname: update_document_meta
   :accesscontrol: 
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:delete:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/nevershare

   Remove nevershare flag

   :shortname: document_remove_nevershare
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/nevershare

   Flag a document as nevershare

   :shortname: document_set_nevershare
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/

   get all documents related to argument-document by rel-type defined by rel
     includes relationships to other versions of the argument-document
     (also limit, offset and status)

   :shortname: get_documents_by_rel
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter REL: The type of relationship between the documents, i.e. ``annotation``, ``interpretation``
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/

   Calls _document_create_by_rel: exists for 1:1 mapping of URLs to views

   :shortname: document_create_by_rel
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter REL: The type of relationship between the documents, i.e. ``annotation``, ``interpretation``
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/external/{PHA_EMAIL}/{EXTERNAL_ID}

   Calls _document_create_by_rel: exists for 1:1 mapping of URLs to views

   :shortname: document_create_by_rel_with_ext_id
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter REL: The type of relationship between the documents, i.e. ``annotation``, ``interpretation``
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/external/{PHA_EMAIL}/{EXTERNAL_ID}

   Calls _document_create_by_rel: exists for 1:1 mapping of URLs to views

   :shortname: document_create_by_rel_with_ext_id
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter REL: The type of relationship between the documents, i.e. ``annotation``, ``interpretation``
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/replace

   Version a document without external_id: just calls _document_version

   :shortname: document_version
   :accesscontrol: A user app with access to the record, a principal in full control of the record, or the admin app that created the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/replace/external/{PHA_EMAIL}/{EXTERNAL_ID}

   Version a document with an external_id: just calls _document_version

   :shortname: document_version_by_ext_id
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/set-status

   

   :shortname: document_set_status
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/status-history

   

   :shortname: document_status_history
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/versions/

   Retrieve the versions of a document

   :shortname: document_versions
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/inbox/

   

   :shortname: record_inbox
   :accesscontrol: 
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/inbox/{MESSAGE_ID}

   

   :shortname: record_send_message
   :accesscontrol: Any admin app, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter MESSAGE_ID: The unique identifier of the Indivo Message
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}

   

   :shortname: record_message_attach
   :accesscontrol: Any admin app, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter ATTACHMENT_NUM: The 1-indexed number corresponding to the message attachment
   :parameter MESSAGE_ID: The unique identifier of the Indivo Message
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/notifications/

   

   :shortname: record_notify
   :accesscontrol: Any admin app, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/notify

   

   :shortname: record_notify
   :accesscontrol: Any admin app, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/owner

   

   :shortname: record_get_owner
   :accesscontrol: A principal in full control of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/owner

   

   :shortname: record_set_owner
   :accesscontrol: Any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:put:: /records/{RECORD_ID}/owner

   

   :shortname: record_set_owner
   :accesscontrol: Any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/reports/experimental/ccr

   

   :shortname: report_ccr
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/allergies/

   For 1:1 mapping of URLs to views. Calls _allergy_list

   :shortname: allergy_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/equipment/

   For 1:1 mapping of URLs to views. Calls _equipment_list

   :shortname: equipment_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/immunizations/

   For 1:1 mapping of URLs to views: calls _immunization_list

   :shortname: immunization_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/labs/

   For 1:1 mapping of URLs to views. Calls _lab_list

   :shortname: lab_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/measurements/{LAB_CODE}/

   For 1:1 mapping of URLs to views: calls _measurement_list

   :shortname: measurement_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter LAB_CODE: The identifier corresponding to the measurement being made.
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/medications/

   For 1:1 mapping of URLs to views: calls _medication_list

   :shortname: medication_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/problems/

   For 1:1 mapping of URLs to views: calls _problem_list

   :shortname: problem_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/procedures/

   For 1:1 mapping of URLs to views: calls _procedure_list

   :shortname: procedure_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/simple-clinical-notes/

   For 1:1 mapping of URLs to views. Calls _simple_clinical_notes_list

   :shortname: simple_clinical_notes_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/vitals/

   For 1:1 mapping from URLs to views: calls _vitals_list

   :shortname: vitals_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/vitals/{CATEGORY}/

   For 1:1 mapping from URLs to views: calls _vitals_list

   :shortname: vitals_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter CATEGORY: The category of vital sign, i.e. ``weight``, ``Blood_Pressure_Systolic``
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /records/{RECORD_ID}/shares/

   List the shares of a record

   :shortname: record_shares
   :accesscontrol: The owner of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/shares/

   Add a share
     FIXME: add label

   :shortname: record_share_add
   :accesscontrol: The owner of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:delete:: /records/{RECORD_ID}/shares/{OTHER_ACCOUNT_ID}

   Remove a share

   :shortname: record_share_delete
   :accesscontrol: The owner of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter OTHER_ACCOUNT_ID: The email identifier of the Indivo account to share with
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:post:: /records/{RECORD_ID}/shares/{OTHER_ACCOUNT_ID}/delete

   Remove a share

   :shortname: record_share_delete
   :accesscontrol: The owner of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter OTHER_ACCOUNT_ID: The email identifier of the Indivo account to share with
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /static/{PATH}

   Serve static files below a given point in the directory structure.
   
       To use, put a URL pattern such as::
   
           (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root' : '/path/to/my/files/'})
   
       in your URLconf. You must provide the ``document_root`` param. You may
       also set ``show_indexes`` to ``True`` if you'd like to serve a basic index
       of the directory.  This index view will use the template hardcoded below,
       but if you'd like to override it, you can create a template called
       ``static/directory_index.html``.

   :shortname: serve
   :accesscontrol: 
   :parameter PATH: The path to a static resource. Relative to the indivo_server static directory.
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   


--------

.. http:get:: /version

   Return the current version of Indivo.

   :shortname: get_version
   :accesscontrol: Any principal in Indivo.
   :returns: DESCRIBE THE VALUES THAT THE CALL RETURNS

Example Return Value::
   
   GIVE AN EXAMPLE OF A RETURN VALUE
   
