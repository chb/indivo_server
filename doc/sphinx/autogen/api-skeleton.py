

CALLS=[{
    "method":"POST",
    "path":"/accounts/",
    "view_func":"account_create",
    "access_doc":"Any admin app.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
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
      
    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/accounts/search",
    "view_func":"account_search",
    "access_doc":"Any admin app.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
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

    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}",
    "view_func":"account_info",
    "access_doc":"Any admin app, or the Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Display information about an account.

    Return information includes the account's secondary-secret,
    full name, contact email, login counts, state, and auth 
    systems.

    Will return :http:statuscode:`200` on success, with account info
    XML.

    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/authsystems/",
    "view_func":"account_authsystem_add",
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
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

    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/authsystems/password/change",
    "view_func":"account_password_change",
    "access_doc":"The Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Change a account's password.

    request.POST must contain:
    
    * *old*: The existing account password.
    * *new*: The desired new password.

    Will return :http:statuscode:`200` on success,
    :http:statuscode:`403` if the old password didn't
    validate, :http:statuscode:`400` if the POST data
    didn't contain both an old password and a new one.
    
    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/authsystems/password/set",
    "view_func":"account_password_set",
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Force the password of an account to a given value.

    This differs from 
    :py:meth:`~indivo_server.indivo.views.account.account_password_change`
    in that it does not require validation of the old password. This
    function is therefore admin-facing, whereas 
    :py:meth:`~indivo_server.indivo.views.account.account_password_change` 
    is user-facing.

    request.POST must contain:
    
    * *password*: The new password to set.

    Will return :http:statuscode:`200` on success, :http:statuscode:`400`
    if the passed POST data didn't contain a new password.

    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/authsystems/password/set-username",
    "view_func":"account_username_set",
    "access_doc":"Any admin app, or the Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Force the username of an account to a given value.

    request.POST must contain:

    * *username*: The new username to set.

    Will return :http:statuscode:`200` on success, 
    :http:statuscode:`400` if the POST data doesn't conatain
    a new username.

    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/check-secrets/{PRIMARY_SECRET}",
    "view_func":"account_check_secrets",
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        'PRIMARY_SECRET':'A confirmation string sent securely to the patient from Indivo',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Validate an account's primary and secondary secrets.

    If the secondary secret is to be validated, request.GET must
    contain:

    * *secondary_secret*: The account's secondary secret.

    This call will validate the prmary secret, and the secondary
    secret if passed.

    Will return :http:statuscode:`200` on success, 
    :http:statuscode:`403` if either validation fails.

    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/forgot-password",
    "view_func":"account_forgot_password",
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
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
    
    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/inbox/",
    "view_func":"account_inbox",
    "access_doc":"The Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List messages in an account's inbox.

  Messages will be ordered by *order_by* and paged by *limit* and
  *offset*. request.GET may additionally contain:

  * *include_archive*: Adds messages that have been archived (which are
    normally omitted) to the listing. Any value will be interpreted as ``True``. 
    Defaults to ``False``, as if it weren't passed.

  Will return :http:statuscode:`200` with a list of messages on success.

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/inbox/",
    "view_func":"account_send_message",
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Send a message to an account.

  Account messages have no attachments for now, as we wouldn't know
  which record to store them on.

  request.POST may contain any of:

  * *message_id*: An external identifier for the message, used for later
    retrieval. Defaults to ``None``.

  * *body*: The message body. Defaults to ``[no body]``.

  * *severity*: The importance of the message. Options are ``low``, ``medium``,
    ``high``. Defaults to ``low``.

  After delivering the message to Indivo's inbox, this call will send an email to 
  the account's contact address, alerting them that a new message has arrived.

  Will return :http:statuscode:`200` on success, :http:statuscode:`400` if the
  passed *message_id* is a duplicate.
  
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}",
    "view_func":"account_inbox_message",
    "access_doc":"The Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        'MESSAGE_ID':'The unique identifier of the Indivo Message',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Retrieve an individual message from an account's inbox.

  This call additionally filters message content based on its
  body-type. For example, markdown content is scrubbed of 
  extraneous HTML, then converted to HTML content. Also, this
  call marks the message as read.

  *message_id* should be the external identifier of the message
  as created by 
  :py:meth:`~indivo_server.indivo.views.messaging.account_send_message` or
  :py:meth:`~indivo_server.indivo.views.messaging.record_send_message`.

  Will return :http:statuscode:`200` with XML describing the message
  (id, sender, dates received, read, and archived, subject, body,
  severity, etc.) on success.

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}/archive",
    "view_func":"account_message_archive",
    "access_doc":"The Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        'MESSAGE_ID':'The unique identifier of the Indivo Message',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Archive a message.

  This call sets a message's archival date as now, unless it's already set. 
  This means that future calls to 
  :py:meth:`~indivo_server.indivo.views.messaging.account_inbox` will not
  display this message by default.
  
  Will return :http:statuscode:`200` on success.

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}/accept",
    "view_func":"account_inbox_message_attachment_accept",
    "access_doc":"The Account owner.",
    "url_params":{
        'ATTACHMENT_NUM':'The 1-indexed number corresponding to the message attachment',
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        'MESSAGE_ID':'The unique identifier of the Indivo Message',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Accept a message attachment into the record it corresponds to.

  This call is triggered when a user views a message with an attachment, and 
  chooses to add the attachment contents into their record.

  Will return :http:statuscode:`200` on success, :http:statuscode:`410` if the 
  attachment has already been saved.

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/info-set",
    "view_func":"account_info_set",
    "access_doc":"Any admin app, or the Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Set basic information about an account.

    request.POST can contain any of:

    * *contact_email*: A new contact email for the account.

    * *full_name*: A new full name for the account.

    Each passed parameter will be updated for the account.

    Will return :http:statuscode:`200` on success, 
    :http:statuscode:`400` if the POST data contains none of
    the settable parameters.
    
    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/initialize/{PRIMARY_SECRET}",
    "view_func":"account_initialize",
    "access_doc":"Any Indivo UI app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        'PRIMARY_SECRET':'A confirmation string sent securely to the patient from Indivo',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
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
    
    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/notifications/",
    "view_func":"account_notifications",
    "access_doc":"The Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List an account's notifications.

  Orders by *order_by*, pages by *limit* and *offset*.
  
  Will return :http:statuscode:`200` with a list of notifications on success.

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/permissions/",
    "view_func":"account_permissions",
    "access_doc":"The Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Retrieve the permissions of a given account across all carenets
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/primary-secret",
    "view_func":"account_primary_secret",
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Display an account's primary secret.

    This is an admin-facing call, and should be used sparingly,
    as we would like to avoid sending primary-secrets over the
    wire. If possible, use 
    :py:meth:`~indivo_server.indivo.views.account.account_check_secrets`
    instead.

    Will return :http:statuscode:`200` with the primary secret on success.
    
    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/records/",
    "view_func":"record_list",
    "access_doc":"The Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
  A list of records available for a given account
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/reset",
    "view_func":"account_reset",
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Reset an account to an ``uninitialized`` state.

    Just calls into :py:meth:`~indivo_server.indivo.models.accounts.Account.reset`.

    Will return :http:statuscode:`200` on success.

    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/secret",
    "view_func":"account_secret",
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Return the secondary secret of an account.

    Will always return :http:statuscode:`200`. If the account 
    has no associated secondary secret, the return XML will
    be empty.

    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/secret-resend",
    "view_func":"account_resend_secret",
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Sends an account user their primary secret in case they lost it.

    Will return :http:statuscode:`200` on success.

    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/set-state",
    "view_func":"account_set_state",
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
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

    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/apps/",
    "view_func":"all_phas",
    "access_doc":"Any principal in Indivo.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List all available userapps.

  Will return :http:statuscode:`200` with an XML list of apps on success.

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"DELETE",
    "path":"/apps/{PHA_EMAIL}",
    "view_func":"pha_delete",
    "access_doc":"The user app itself.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Delete a userapp from Indivo.

  This call removes the app entirely from indivo, so it will never be
  accessible again. To remove an app just from a single record, see
  :py:meth:`~indivo_server.indivo.views.pha.pha_record_delete`.

  Will return :http:statuscode:`200` on success.

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/apps/{PHA_EMAIL}",
    "view_func":"pha",
    "access_doc":"Any principal in Indivo.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Return a description of a single userapp.

  Will return :http:statuscode:`200` with an XML description of the app 
  on success.
  
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/apps/{PHA_EMAIL}/documents/",
    "view_func":"app_document_list",
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls document_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/apps/{PHA_EMAIL}/documents/",
    "view_func":"app_document_create",
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping from views: calls document_create_or_update()
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}",
    "view_func":"app_document_create_or_update_ext",
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'EXTERNAL_ID':'The external identifier of the desired resource',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping from views: calls document_create_or_update()
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}/meta",
    "view_func":"app_document_meta_ext",
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'EXTERNAL_ID':'The external identifier of the desired resource',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls _document_meta
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"DELETE",
    "path":"/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}",
    "view_func":"app_document_delete",
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
  Delete an application specific document: no restrictions, since this storage is 
  managed by the app.
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}",
    "view_func":"app_specific_document",
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Retrive an app-specific document: calls document()
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}",
    "view_func":"app_document_create_or_update",
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping from views: calls document_create_or_update()
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/label",
    "view_func":"app_document_label",
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For a 1:1 mapping of URLs to views: calls document_label
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/meta",
    "view_func":"app_document_meta",
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls _document_meta
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"DELETE",
    "path":"/carenets/{CARENET_ID}",
    "view_func":"carenet_delete",
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/accounts/",
    "view_func":"carenet_account_list",
    "access_doc":"A principal in the carenet, in full control of the carenet's record, or any admin app.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
List the accounts of a given carenet
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/carenets/{CARENET_ID}/accounts/",
    "view_func":"carenet_account_create",
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Link an account to a given carenet
  write=false or write=true
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"DELETE",
    "path":"/carenets/{CARENET_ID}/accounts/{ACCOUNT_ID}",
    "view_func":"carenet_account_delete",
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'ACCOUNT_ID':'The email identifier of the Indivo account',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Unlink an account from a given carenet
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/accounts/{ACCOUNT_ID}/permissions",
    "view_func":"carenet_account_permissions",
    "access_doc":"A user app with access to the carenet and proxying the account, a principal in full control of the carenet's record, or any admin app.",
    "url_params":{
        'ACCOUNT_ID':'The email identifier of the Indivo account',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Retrieve the permissions of a given account within a given carenet
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/apps/",
    "view_func":"carenet_apps_list",
    "access_doc":"A principal in the carenet, in full control of the carenet's record, or any admin app.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
List Apps within a given carenet
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"DELETE",
    "path":"/carenets/{CARENET_ID}/apps/{PHA_EMAIL}",
    "view_func":"carenet_apps_delete",
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
  Add app to a given carenet
  read/write ability is determined by the user who uses the app, not by the app itself.
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/carenets/{CARENET_ID}/apps/{PHA_EMAIL}",
    "view_func":"carenet_apps_create",
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
  Add app to a given carenet
  read/write ability is determined by the user who uses the app, not by the app itself.
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/apps/{PHA_EMAIL}/permissions",
    "view_func":"carenet_app_permissions",
    "access_doc":"",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Retrieve the permissions for an app within a carenet
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/documents/",
    "view_func":"carenet_document_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
List documents from a given carenet

    Return both documents in the given carenet and 
    documents with the same types as in the record's autoshare

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/documents/special/{SPECIAL_DOCUMENT}",
    "view_func":"read_special_document_carenet",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, an account in the carenet or in control of the record, or the admin app that created the carenet's record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        'SPECIAL_DOCUMENT':'The type of special document to access. Options are ``demographics``, ``contact``',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Read a special document from a carenet
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/documents/{DOCUMENT_ID}",
    "view_func":"carenet_document",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Return a document given a record and carenet id

    Return the document if it is in the given carenet or 
    its type is in the record's autoshare
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/documents/{DOCUMENT_ID}/meta",
    "view_func":"carenet_document_meta",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls _document_meta
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/record",
    "view_func":"carenet_record",
    "access_doc":"",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Basic record information within a carenet

  For now, just the record label
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/carenets/{CARENET_ID}/rename",
    "view_func":"carenet_rename",
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/allergies/",
    "view_func":"carenet_allergy_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls _allergy_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/equipment/",
    "view_func":"carenet_equipment_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls _equipment_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/immunizations/",
    "view_func":"carenet_immunization_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views: calls _immunization_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/labs/",
    "view_func":"carenet_lab_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls _lab_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/measurements/{LAB_CODE}/",
    "view_func":"carenet_measurement_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        'LAB_CODE':'The identifier corresponding to the measurement being made.',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 For 1:1 mapping of URLs to views: calls _measurement_list 
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/medications/",
    "view_func":"carenet_medication_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views: calls _medication_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/problems/",
    "view_func":"carenet_problem_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views: calls _problem_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/procedures/",
    "view_func":"carenet_procedure_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views: calls _procedure_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/simple-clinical-notes/",
    "view_func":"carenet_simple_clinical_notes_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls _simple_clinical_notes_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/vitals/",
    "view_func":"carenet_vitals_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping from URLs to views: calls _vitals_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/vitals/{CATEGORY}",
    "view_func":"carenet_vitals_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CATEGORY':'The category of vital sign, i.e. ``weight``, ``Blood_Pressure_Systolic``',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping from URLs to views: calls _vitals_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/codes/systems/",
    "view_func":"coding_systems_list",
    "access_doc":"",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/codes/systems/{SYSTEM_SHORT_NAME}/query",
    "view_func":"coding_system_query",
    "access_doc":"",
    "url_params":{
        'SYSTEM_SHORT_NAME':'',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/oauth/access_token",
    "view_func":"exchange_token",
    "access_doc":"A request signed by a RequestToken.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Exchange a request token for a valid access token.

  This call requires that the request be signed with a valid oauth request
  token that has previously been authorized.

  Will return :http:statuscode:`200` with the access token on success,
  :http:statuscode:`403` if the oauth signature is missing or invalid.

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/oauth/internal/request_tokens/{REQTOKEN_ID}/approve",
    "view_func":"request_token_approve",
    "access_doc":"A principal in the carenet to which the request token is restricted (if the token is restricted), or a principal with full control over the record (if the token is not restricted).",
    "url_params":{
        'REQTOKEN_ID':'',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Indicate a user's consent to bind an app to a record or carenet.

  request.POST must contain **EITHER**:
  
  * *record_id*: The record to bind to.

  * *carenet_id*: The carenet to bind to.

  Will return :http:statuscode:`200` with a redirect url to the app on success,
  :http:statuscode:`403` if *record_id*/*carenet_id* don't match *reqtoken*.

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/oauth/internal/request_tokens/{REQTOKEN_ID}/claim",
    "view_func":"request_token_claim",
    "access_doc":"Any Account.",
    "url_params":{
        'REQTOKEN_ID':'',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Claim a request token on behalf of an account.

  After this call, no one but ``request.principal`` will be able to
  approve *reqtoken*.

  Will return :http:statuscode:`200` with the email of the claiming principal
  on success, :http:statuscode:`403` if the token has already been claimed.

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/oauth/internal/request_tokens/{REQTOKEN_ID}/info",
    "view_func":"request_token_info",
    "access_doc":"Any Account.",
    "url_params":{
        'REQTOKEN_ID':'',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Get information about a request token.

  Information includes: 

  * the record/carenet it is bound to
  
  * Whether the bound record/carenet has been authorized before
  
  * Information about the app for which the token was generated.

  Will return :http:statuscode:`200` with the info on success.
  
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/oauth/internal/session_create",
    "view_func":"session_create",
    "access_doc":"Any Indivo UI app.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Authenticate a user and register a web session for them.

  request.POST must contain:

  * *username*: the username of the user to authenticate.

  request.POST may contain **EITHER**:
  
  * *password*: the password to use with *username* against the
    internal password auth system.

  * *system*: An external auth system to authenticate the user
    with.

  Will return :http:statuscode:`200` with a valid session token 
  on success, :http:statuscode:`403` if the passed credentials were
  invalid or it the passed *system* doesn't exist.
  
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/oauth/internal/surl-verify",
    "view_func":"surl_verify",
    "access_doc":"Any Account.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Verify a signed URL.
  
  The URL must contain the following GET parameters:
  
  * *surl_timestamp*: when the url was generated. Must be within the past hour,
    to avoid permitting old surls.

  * *surl_token* The access token used to sign the url.

  * *surl_sig* The computed signature (base-64 encoded sha1) of the url.

  Will always return :http:statuscode:`200`. The response body will be one of:
  
  * ``<result>ok</result>``: The surl was valid.

  * ``<result>old</result>``: The surl was too old.

  * ``<result>mismatch</result>``: The surl's signature was invalid.
  
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/oauth/request_token",
    "view_func":"request_token",
    "access_doc":"Any user app.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Get a new request token, bound to a record or carenet if desired.

    request.POST may contain **EITHER**:

    * *indivo_record_id*: The record to which to bind the request token.
    
    * *indivo_carenet_id*: The carenet to which to bind the request token.

    Will return :http:statuscode:`200` with the request token on success,
    :http:statuscode:`403` if the oauth signature on the request was missing
    of faulty.

    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/",
    "view_func":"record_create",
    "access_doc":"Any admin app.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views: calls _record_create
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/records/external/{PRINCIPAL_EMAIL}/{EXTERNAL_ID}",
    "view_func":"record_create_ext",
    "access_doc":"An admin app with an id matching the principal_email in the URL.",
    "url_params":{
        'PRINCIPAL_EMAIL':'',
        'EXTERNAL_ID':'The external identifier of the desired resource',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views: calls _record_create
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}",
    "view_func":"record",
    "access_doc":"A principal in full control of the record, the admin app that created the record, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/apps/",
    "view_func":"record_phas",
    "access_doc":"A principal in full control of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"DELETE",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}",
    "view_func":"pha_record_delete",
    "access_doc":"Any admin app, or a principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Remove a userapp from a record.

  This is accomplished by deleting the app from all carenets belonging to
  the record, then removing the Shares between the record and the app.

  Will return :http:statuscode:`200` on success, :http:statuscode:`404` if
  either the record or the app don't exist.

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}",
    "view_func":"record_pha",
    "access_doc":"A principal in full control of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/",
    "view_func":"record_app_document_list",
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls document_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/",
    "view_func":"record_app_document_create",
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping from views: calls document_create_or_update()
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}",
    "view_func":"record_app_document_create_or_update_ext",
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'EXTERNAL_ID':'The external identifier of the desired resource',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping from views: calls document_create_or_update()
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}",
    "view_func":"record_app_document_create_or_update_ext",
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'EXTERNAL_ID':'The external identifier of the desired resource',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping from views: calls document_create_or_update()
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}/meta",
    "view_func":"record_app_document_meta_ext",
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'EXTERNAL_ID':'The external identifier of the desired resource',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls _document_meta
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"DELETE",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}",
    "view_func":"record_app_document_delete",
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
  Delete a record-application specific document: no restrictions, since this storage is 
  managed by the app.
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}",
    "view_func":"record_app_specific_document",
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Retrieve a record-app-specific document: calls document()
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/label",
    "view_func":"record_app_document_label",
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For a 1:1 mapping of URLs to views: calls document_label
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/meta",
    "view_func":"record_app_document_meta",
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls _document_meta
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/setup",
    "view_func":"record_pha_setup",
    "access_doc":"Any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Set up a PHA in a record ahead of time

  FIXME: eventually, when there are permission restrictions on a PHA, make sure that
  any permission restrictions on the current PHA are transitioned accordingly
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/audits/",
    "view_func":"audit_record_view",
    "access_doc":"A principal in full control of the record, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Return audits of calls touching *record*.

  Will return :http:statuscode:`200` with matching audits on succes, 
  :http:statuscode:`404` if *record* doesn't exist.

  .. deprecated:: 0.9.3
     Use :py:meth:`~indivo_server.indivo.views.audit.audit_query` instead.

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/audits/documents/{DOCUMENT_ID}/",
    "view_func":"audit_document_view",
    "access_doc":"A principal in full control of the record, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Return audits of calls touching *record* and *document_id*.

  Will return :http:statuscode:`200` with matching audits on succes, 
  :http:statuscode:`404` if *record* or *document_id* don't exist.

  .. deprecated:: 0.9.3
     Use :py:meth:`~indivo_server.indivo.views.audit.audit_query` instead.

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/audits/documents/{DOCUMENT_ID}/functions/{FUNCTION_NAME}/",
    "view_func":"audit_function_view",
    "access_doc":"A principal in full control of the record, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        'FUNCTION_NAME':'The internal Indivo function name called by the API request',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Return audits of calls to *function_name* touching *record* and *document_id*.

  Will return :http:statuscode:`200` with matching audits on succes, 
  :http:statuscode:`404` if *record* or *document_id* don't exist.

  .. deprecated:: 0.9.3
     Use :py:meth:`~indivo_server.indivo.views.audit.audit_query` instead.

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/audits/query/",
    "view_func":"audit_query",
    "access_doc":"A principal in full control of the record, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Select Audit Objects via the Query API Interface.

  Accepts any argument specified by the :doc:`/query-api`, and filters
  available audit objects by the arguments.

  Will return :http:statuscode:`200` with XML containing individual or
  aggregated audit records on succes, :http:statuscode:`400` if any of 
  the arguments to the query interface are invalid.

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/autoshare/bytype/",
    "view_func":"autoshare_list",
    "access_doc":"A principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/autoshare/bytype/all",
    "view_func":"autoshare_list_bytype_all",
    "access_doc":"A principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
  provide all of the autoshares, grouped by type
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/autoshare/carenets/{CARENET_ID}/bytype/set",
    "view_func":"autoshare_create",
    "access_doc":"A principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/autoshare/carenets/{CARENET_ID}/bytype/unset",
    "view_func":"autoshare_delete",
    "access_doc":"A principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/carenets/",
    "view_func":"carenet_list",
    "access_doc":"A principal in full control of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/carenets/",
    "view_func":"carenet_create",
    "access_doc":"A principal in full control of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
    POST to /records/{record_id}/carenets/
    Must have a 'name' key/value pair and the name must not yet be used by this record
    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"DELETE",
    "path":"/records/{RECORD_ID}/documents/",
    "view_func":"documents_delete",
    "access_doc":"",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/",
    "view_func":"record_document_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls document_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/documents/",
    "view_func":"document_create",
    "access_doc":"A user app with access to the record, a principal in full control of the record, or the admin app that created the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
  Create a document, possibly with the given external_id
  This call is ONLY made on NON-app-specific data,
  so the PHA argument is non-null only for specifying an external_id
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}",
    "view_func":"document_create_by_ext_id",
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'EXTERNAL_ID':'The external identifier of the desired resource',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
  Create a document with the given external_id
  Same as document_create: this function exists
  to preserve the 1:1 mapping from functions to views
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}/label",
    "view_func":"record_document_label_ext",
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'EXTERNAL_ID':'The external identifier of the desired resource',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For a 1:1 mapping of URLs to views: calls document_label
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}/meta",
    "view_func":"record_document_meta_ext",
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'EXTERNAL_ID':'The external identifier of the desired resource',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls _document_meta
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}",
    "view_func":"read_special_document",
    "access_doc":"A user app with access to the record, a principal in full control of the record, or the admin app that created the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'SPECIAL_DOCUMENT':'The type of special document to access. Options are ``demographics``, ``contact``',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Read a special document from a record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}",
    "view_func":"save_special_document",
    "access_doc":"A user app with access to the record, a principal in full control of the record, or the admin app that created the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'SPECIAL_DOCUMENT':'The type of special document to access. Options are ``demographics``, ``contact``',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Save a new special document 
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}",
    "view_func":"save_special_document",
    "access_doc":"A user app with access to the record, a principal in full control of the record, or the admin app that created the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'SPECIAL_DOCUMENT':'The type of special document to access. Options are ``demographics``, ``contact``',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Save a new special document 
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID_0}/rels/{REL}/{DOCUMENT_ID_1}",
    "view_func":"document_rels",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID_1':'The id of the document that is the subject of the relationship, i.e. DOCUMENT_ID_1 *annotates* DOCUMENT_ID_0',
        'DOCUMENT_ID_0':'The id of the document that is the object of the relationship, i.e. DOCUMENT_ID_0 *is annotated by* DOCUMENT_ID_1',
        'REL':'The type of relationship between the documents, i.e. ``annotation``, ``interpretation``',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
  create a new document relationship between existing docs.
  2010-08-15: removed external_id and pha parameters as they are never set.
  That's for create_by_rel
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}",
    "view_func":"record_specific_document",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Retrieve a record-specific document: calls document()
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/",
    "view_func":"document_carenets",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
List all the carenets for a given document

    This view retrieves all the carenets in which  a given 
    document has been placed
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"DELETE",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}",
    "view_func":"carenet_document_delete",
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Delete a document into a given carenet
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}",
    "view_func":"carenet_document_placement",
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
  Place a document into a given carenet
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}/autoshare-revert",
    "view_func":"autoshare_revert",
    "access_doc":"A principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/label",
    "view_func":"record_document_label",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For a 1:1 mapping of URLs to views: calls document_label
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/meta",
    "view_func":"record_document_meta",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls _document_meta
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/meta",
    "view_func":"update_document_meta",
    "access_doc":"",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"DELETE",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/nevershare",
    "view_func":"document_remove_nevershare",
    "access_doc":"A principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
  Remove nevershare flag
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/nevershare",
    "view_func":"document_set_nevershare",
    "access_doc":"A principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
  Flag a document as nevershare
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/",
    "view_func":"get_documents_by_rel",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'REL':'The type of relationship between the documents, i.e. ``annotation``, ``interpretation``',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
  get all documents related to argument-document by rel-type defined by rel
  includes relationships to other versions of the argument-document
  (also limit, offset and status)
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/",
    "view_func":"document_create_by_rel",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'REL':'The type of relationship between the documents, i.e. ``annotation``, ``interpretation``',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Calls _document_create_by_rel: exists for 1:1 mapping of URLs to views
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/external/{PHA_EMAIL}/{EXTERNAL_ID}",
    "view_func":"document_create_by_rel_with_ext_id",
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'EXTERNAL_ID':'The external identifier of the desired resource',
        'REL':'The type of relationship between the documents, i.e. ``annotation``, ``interpretation``',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Calls _document_create_by_rel: exists for 1:1 mapping of URLs to views
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/external/{PHA_EMAIL}/{EXTERNAL_ID}",
    "view_func":"document_create_by_rel_with_ext_id",
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'EXTERNAL_ID':'The external identifier of the desired resource',
        'REL':'The type of relationship between the documents, i.e. ``annotation``, ``interpretation``',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Calls _document_create_by_rel: exists for 1:1 mapping of URLs to views
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/replace",
    "view_func":"document_version",
    "access_doc":"A user app with access to the record, a principal in full control of the record, or the admin app that created the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Version a document without external_id: just calls _document_version
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/replace/external/{PHA_EMAIL}/{EXTERNAL_ID}",
    "view_func":"document_version_by_ext_id",
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'EXTERNAL_ID':'The external identifier of the desired resource',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Version a document with an external_id: just calls _document_version
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/set-status",
    "view_func":"document_set_status",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/status-history",
    "view_func":"document_status_history",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/versions/",
    "view_func":"document_versions",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Retrieve the versions of a document
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/inbox/{MESSAGE_ID}",
    "view_func":"record_send_message",
    "access_doc":"Any admin app, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'MESSAGE_ID':'The unique identifier of the Indivo Message',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Send a message to a record.

  request.POST may contain any of:

  * *body*: The message body. Defaults to ``[no body]``.

  * *body_type*: The formatting of the message body. Options are ``plaintext``,
    ``markdown``. Defaults to ``markdown``.

  * *num_attachments*: The number of attachments this message requires. Attachments
    are uploaded with calls to 
    :py:meth:`~indivo_server.indivo.views.messaging.record_message_attach`, and 
    the message will not be delivered until all attachments have been uploaded.
    Defaults to 0.

  * *severity*: The importance of the message. Options are ``low``, ``medium``,
    ``high``. Defaults to ``low``.

  After delivering the message to the Indivo inbox of all accounts authorized to
  view messages for the passed *record*, this call will send an email to each 
  account's contact address, alerting them that a new message has arrived.

  Will return :http:statuscode:`200` on success, :http:statuscode:`400` if the
  passed *message_id* is a duplicate.
  
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}",
    "view_func":"record_message_attach",
    "access_doc":"Any admin app, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'ATTACHMENT_NUM':'The 1-indexed number corresponding to the message attachment',
        'MESSAGE_ID':'The unique identifier of the Indivo Message',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Attach a document to an Indivo message.

  Only XML documents are accepted for now. Since Message objects are duplicated
  for each recipient account, this call may attach the document to multiple
  Message objects.

  request.POST must contain the raw XML attachment data.

  Will return :http:statuscode:`200` on success, :http:statuscode:`400` if the
  attachment with number *attachment_num* has already been uploaded.

  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/notifications/",
    "view_func":"record_notify",
    "access_doc":"Any admin app, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/notify",
    "view_func":"record_notify",
    "access_doc":"Any admin app, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/owner",
    "view_func":"record_get_owner",
    "access_doc":"A principal in full control of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/owner",
    "view_func":"record_set_owner",
    "access_doc":"Any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/owner",
    "view_func":"record_set_owner",
    "access_doc":"Any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/experimental/ccr",
    "view_func":"report_ccr",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/allergies/",
    "view_func":"allergy_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls _allergy_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/equipment/",
    "view_func":"equipment_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls _equipment_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/immunizations/",
    "view_func":"immunization_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views: calls _immunization_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/labs/",
    "view_func":"lab_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls _lab_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/measurements/{LAB_CODE}/",
    "view_func":"measurement_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'LAB_CODE':'The identifier corresponding to the measurement being made.',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 For 1:1 mapping of URLs to views: calls _measurement_list 
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/medications/",
    "view_func":"medication_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views: calls _medication_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/problems/",
    "view_func":"problem_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views: calls _problem_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/procedures/",
    "view_func":"procedure_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views: calls _procedure_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/simple-clinical-notes/",
    "view_func":"simple_clinical_notes_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping of URLs to views. Calls _simple_clinical_notes_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/vitals/",
    "view_func":"vitals_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping from URLs to views: calls _vitals_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/vitals/{CATEGORY}/",
    "view_func":"vitals_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'CATEGORY':'The category of vital sign, i.e. ``weight``, ``Blood_Pressure_Systolic``',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
For 1:1 mapping from URLs to views: calls _vitals_list
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/shares/",
    "view_func":"record_shares",
    "access_doc":"The owner of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the shares of a record
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/shares/",
    "view_func":"record_share_add",
    "access_doc":"The owner of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
  Add a share
  FIXME: add label
  
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"DELETE",
    "path":"/records/{RECORD_ID}/shares/{OTHER_ACCOUNT_ID}",
    "view_func":"record_share_delete",
    "access_doc":"The owner of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'OTHER_ACCOUNT_ID':'The email identifier of the Indivo account to share with',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Remove a share
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/shares/{OTHER_ACCOUNT_ID}/delete",
    "view_func":"record_share_delete",
    "access_doc":"The owner of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'OTHER_ACCOUNT_ID':'The email identifier of the Indivo account to share with',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
Remove a share
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/static/{PATH}",
    "view_func":"serve",
    "access_doc":"",
    "url_params":{
        'PATH':'The path to a static resource. Relative to the indivo_server static directory.',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
    Serve static files below a given point in the directory structure.

    To use, put a URL pattern such as::

        (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root' : '/path/to/my/files/'})

    in your URLconf. You must provide the ``document_root`` param. You may
    also set ``show_indexes`` to ``True`` if you'd like to serve a basic index
    of the directory.  This index view will use the template hardcoded below,
    but if you'd like to override it, you can create a template called
    ``static/directory_index.html``.
    
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

},
{
    "method":"GET",
    "path":"/version",
    "view_func":"get_version",
    "access_doc":"Any principal in Indivo.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Return the current version of Indivo.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',

}]