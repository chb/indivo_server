

CALLS=[{
    "method":"POST",
    "path":"/accounts/",
    "view_func_name":"account_create",
    "access_doc":"Any admin app.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Create a new account.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/accounts/search",
    "view_func_name":"account_search",
    "access_doc":"Any admin app.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Search for accounts by name or email.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}",
    "view_func_name":"account_info",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/authsystems/",
    "view_func_name":"account_authsystem_add",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/authsystems/password/change",
    "view_func_name":"account_password_change",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/authsystems/password/set",
    "view_func_name":"account_password_set",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/authsystems/password/set-username",
    "view_func_name":"account_username_set",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/check-secrets/{PRIMARY_SECRET}",
    "view_func_name":"account_check_secrets",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/forgot-password",
    "view_func_name":"account_forgot_password",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/inbox/",
    "view_func_name":"account_inbox",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/inbox/",
    "view_func_name":"account_send_message",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}",
    "view_func_name":"account_inbox_message",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}/archive",
    "view_func_name":"account_message_archive",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}/accept",
    "view_func_name":"account_inbox_message_attachment_accept",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/info-set",
    "view_func_name":"account_info_set",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/initialize/{PRIMARY_SECRET}",
    "view_func_name":"account_initialize",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/notifications/",
    "view_func_name":"account_notifications",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/permissions/",
    "view_func_name":"account_permissions",
    "access_doc":"The Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the carenets that an account has access to.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/primary-secret",
    "view_func_name":"account_primary_secret",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/records/",
    "view_func_name":"record_list",
    "access_doc":"The Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List all available records for an account.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/reset",
    "view_func_name":"account_reset",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/secret",
    "view_func_name":"account_secret",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/secret-resend",
    "view_func_name":"account_resend_secret",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/set-state",
    "view_func_name":"account_set_state",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/apps/",
    "view_func_name":"all_phas",
    "access_doc":"Any principal in Indivo.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List all available userapps.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"DELETE",
    "path":"/apps/{PHA_EMAIL}",
    "view_func_name":"pha_delete",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/apps/{PHA_EMAIL}",
    "view_func_name":"pha",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/apps/{PHA_EMAIL}/documents/",
    "view_func_name":"app_document_list",
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List app-specific documents.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/apps/{PHA_EMAIL}/documents/",
    "view_func_name":"app_document_create",
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Create an app-specific Indivo document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}",
    "view_func_name":"app_document_create_or_update_ext",
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
 Create an app-specific Indivo document with an associated external id.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}/meta",
    "view_func_name":"app_document_meta_ext",
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
 Fetch the metadata of an app-specific document identified by external id.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"DELETE",
    "path":"/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}",
    "view_func_name":"app_document_delete",
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
 Delete an app-specific document. 
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}",
    "view_func_name":"app_specific_document",
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
 Retrive an app-specific document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}",
    "view_func_name":"app_document_create_or_update",
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
 Create or Overwrite an app-specific Indivo document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/label",
    "view_func_name":"app_document_label",
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
 Set the label of an app-specific document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/meta",
    "view_func_name":"app_document_meta",
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
 Fetch the metadata of an app-specific document via a carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"DELETE",
    "path":"/carenets/{CARENET_ID}",
    "view_func_name":"carenet_delete",
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Delete a carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/accounts/",
    "view_func_name":"carenet_account_list",
    "access_doc":"A principal in the carenet, in full control of the carenet's record, or any admin app.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the accounts in a carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/carenets/{CARENET_ID}/accounts/",
    "view_func_name":"carenet_account_create",
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Add an account to a carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"DELETE",
    "path":"/carenets/{CARENET_ID}/accounts/{ACCOUNT_ID}",
    "view_func_name":"carenet_account_delete",
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
 Remove an account from a carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/accounts/{ACCOUNT_ID}/permissions",
    "view_func_name":"carenet_account_permissions",
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
 List the permissions of an account within a carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/apps/",
    "view_func_name":"carenet_apps_list",
    "access_doc":"A principal in the carenet, in full control of the carenet's record, or any admin app.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List Apps within a given carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"DELETE",
    "path":"/carenets/{CARENET_ID}/apps/{PHA_EMAIL}",
    "view_func_name":"carenet_apps_delete",
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
 Remove an app from a given carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/carenets/{CARENET_ID}/apps/{PHA_EMAIL}",
    "view_func_name":"carenet_apps_create",
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
 Add an app to a carenet
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/apps/{PHA_EMAIL}/permissions",
    "view_func_name":"carenet_app_permissions",
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
 Retrieve the permissions for an app within a carenet. NOT IMPLEMENTED.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/documents/",
    "view_func_name":"carenet_document_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
List documents from a given carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/documents/special/{SPECIAL_DOCUMENT}",
    "view_func_name":"read_special_document_carenet",
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
 Read a special document from a carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/documents/{DOCUMENT_ID}",
    "view_func_name":"carenet_document",
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
Return a document from a carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/documents/{DOCUMENT_ID}/meta",
    "view_func_name":"carenet_document_meta",
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
 Fetch the metadata of a record-specific document via a carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/record",
    "view_func_name":"carenet_record",
    "access_doc":"",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Get basic information about the record to which a carenet belongs.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/carenets/{CARENET_ID}/rename",
    "view_func_name":"carenet_rename",
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Change a carenet's name.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/allergies/",
    "view_func_name":"carenet_allergy_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the allergy data for a given carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/equipment/",
    "view_func_name":"carenet_equipment_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the equipment data for a given carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/immunizations/",
    "view_func_name":"carenet_immunization_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the immunization data for a given carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/labs/",
    "view_func_name":"carenet_lab_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the lab data for a given carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/measurements/{LAB_CODE}/",
    "view_func_name":"carenet_measurement_list",
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
 List the measurement data for a given carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/medications/",
    "view_func_name":"carenet_medication_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the medication data for a given carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/problems/",
    "view_func_name":"carenet_problem_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the problem data for a given carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/procedures/",
    "view_func_name":"carenet_procedure_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the procedure data for a given carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/simple-clinical-notes/",
    "view_func_name":"carenet_simple_clinical_notes_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the simple_clinical_notes data for a given carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/vitals/",
    "view_func_name":"carenet_vitals_list",
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the vitals data for a given carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/vitals/{CATEGORY}",
    "view_func_name":"carenet_vitals_list",
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
 List the vitals data for a given carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/codes/systems/",
    "view_func_name":"coding_systems_list",
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
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/codes/systems/{SYSTEM_SHORT_NAME}/query",
    "view_func_name":"coding_system_query",
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
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/oauth/access_token",
    "view_func_name":"exchange_token",
    "access_doc":"A request signed by a RequestToken.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Exchange a request token for a valid access token.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/oauth/internal/request_tokens/{REQTOKEN_ID}/approve",
    "view_func_name":"request_token_approve",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/oauth/internal/request_tokens/{REQTOKEN_ID}/claim",
    "view_func_name":"request_token_claim",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/oauth/internal/request_tokens/{REQTOKEN_ID}/info",
    "view_func_name":"request_token_info",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/oauth/internal/session_create",
    "view_func_name":"session_create",
    "access_doc":"Any Indivo UI app.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Authenticate a user and register a web session for them.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/oauth/internal/surl-verify",
    "view_func_name":"surl_verify",
    "access_doc":"Any Account.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Verify a signed URL.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/oauth/request_token",
    "view_func_name":"request_token",
    "access_doc":"Any user app.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Get a new request token, bound to a record or carenet if desired.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/",
    "view_func_name":"record_create",
    "access_doc":"Any admin app.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Create a new record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/records/external/{PRINCIPAL_EMAIL}/{EXTERNAL_ID}",
    "view_func_name":"record_create_ext",
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
 Create a new record with an associated external id.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}",
    "view_func_name":"record",
    "access_doc":"A principal in full control of the record, the admin app that created the record, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Get information about an individual record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/apps/",
    "view_func_name":"record_phas",
    "access_doc":"A principal in full control of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List userapps bound to a given record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"DELETE",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}",
    "view_func_name":"pha_record_delete",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}",
    "view_func_name":"record_pha",
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
 Get information about a given userapp bound to a record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/",
    "view_func_name":"record_app_document_list",
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
 List record-app-specific documents.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/",
    "view_func_name":"record_app_document_create",
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
 Create a record-app-specific Indivo document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}",
    "view_func_name":"record_app_document_create_or_update_ext",
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
 Create or Overwrite a record-app-specific Indivo document with an associated external id.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}",
    "view_func_name":"record_app_document_create_or_update_ext",
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
 Create or Overwrite a record-app-specific Indivo document with an associated external id.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}/meta",
    "view_func_name":"record_app_document_meta_ext",
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
 Fetch the metadata of a record-app-specific document identified by external id.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"DELETE",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}",
    "view_func_name":"record_app_document_delete",
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
 Delete a record-app-specific document. 
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}",
    "view_func_name":"record_app_specific_document",
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
 Retrieve a record-app-specific document. 
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/label",
    "view_func_name":"record_app_document_label",
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
 Set the label of a record-app-specific document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/meta",
    "view_func_name":"record_app_document_meta",
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
 Fetch the metadata of a record-app-specific document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/setup",
    "view_func_name":"record_pha_setup",
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
 Bind an app to a record without user authorization.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/audits/",
    "view_func_name":"audit_record_view",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/audits/documents/{DOCUMENT_ID}/",
    "view_func_name":"audit_document_view",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/audits/documents/{DOCUMENT_ID}/functions/{FUNCTION_NAME}/",
    "view_func_name":"audit_function_view",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/audits/query/",
    "view_func_name":"audit_query",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/autoshare/bytype/",
    "view_func_name":"autoshare_list",
    "access_doc":"A principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 For a single record, list all carenets that a given doctype is autoshared with.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/autoshare/bytype/all",
    "view_func_name":"autoshare_list_bytype_all",
    "access_doc":"A principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 For a single record, list all doctypes autoshared into carenets.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/autoshare/carenets/{CARENET_ID}/bytype/set",
    "view_func_name":"autoshare_create",
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
 Automatically share all documents of a certain type into a carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/autoshare/carenets/{CARENET_ID}/bytype/unset",
    "view_func_name":"autoshare_delete",
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
 Remove an autoshare from a carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/carenets/",
    "view_func_name":"carenet_list",
    "access_doc":"A principal in full control of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List all carenets for a record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/carenets/",
    "view_func_name":"carenet_create",
    "access_doc":"A principal in full control of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Create a new carenet for a record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"DELETE",
    "path":"/records/{RECORD_ID}/documents/",
    "view_func_name":"documents_delete",
    "access_doc":"",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Delete all documents associated with a record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/",
    "view_func_name":"record_document_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List record-specific documents.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/documents/",
    "view_func_name":"document_create",
    "access_doc":"A user app with access to the record, a principal in full control of the record, or the admin app that created the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Create a record-specific Indivo Document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}",
    "view_func_name":"document_create_by_ext_id",
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
 Create a record-specific Indivo Document with an associated external id.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}/label",
    "view_func_name":"record_document_label_ext",
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
 Set the label of a record-specific document, specified by external id.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}/meta",
    "view_func_name":"record_document_meta_ext",
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
 Fetch the metadata of a record-specific document identified by external id.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}",
    "view_func_name":"read_special_document",
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
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}",
    "view_func_name":"save_special_document",
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
 Create or update a special document on a record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}",
    "view_func_name":"save_special_document",
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
 Create or update a special document on a record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID_0}/rels/{REL}/{DOCUMENT_ID_1}",
    "view_func_name":"document_rels",
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
 Create a new relationship between two existing documents.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}",
    "view_func_name":"record_specific_document",
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
 Retrieve a record-specific document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/",
    "view_func_name":"document_carenets",
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
List all the carenets into which a document has been shared.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"DELETE",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}",
    "view_func_name":"carenet_document_delete",
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
 Unshare a document from a given carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}",
    "view_func_name":"carenet_document_placement",
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
 Place a document into a given carenet.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}/autoshare-revert",
    "view_func_name":"autoshare_revert",
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
 Revert the document-sharing of a document in a carent to whatever rules are specified by autoshares. NOT IMPLEMENTED.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/label",
    "view_func_name":"record_document_label",
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
 Set the label of a record-specific document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/meta",
    "view_func_name":"record_document_meta",
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
 Fetch the metadata of a record-specific document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/meta",
    "view_func_name":"update_document_meta",
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
 Set metadata fields on a document. NOT IMPLEMENTED. 
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"DELETE",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/nevershare",
    "view_func_name":"document_remove_nevershare",
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
 Remove the nevershare flag from a document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/nevershare",
    "view_func_name":"document_set_nevershare",
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
 Flag a document to never be shared, anywhere.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/",
    "view_func_name":"get_documents_by_rel",
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
 Get all documents related to the passed document_id by a relation of the passed relation-type.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/",
    "view_func_name":"document_create_by_rel",
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
 Create a document and relate it to an existing document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/external/{PHA_EMAIL}/{EXTERNAL_ID}",
    "view_func_name":"document_create_by_rel_with_ext_id",
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
 Create a document, assign it an external id, and relate it to an existing document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/external/{PHA_EMAIL}/{EXTERNAL_ID}",
    "view_func_name":"document_create_by_rel_with_ext_id",
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
 Create a document, assign it an external id, and relate it to an existing document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/replace",
    "view_func_name":"document_version",
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
 Create a new version of a record-specific document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/replace/external/{PHA_EMAIL}/{EXTERNAL_ID}",
    "view_func_name":"document_version_by_ext_id",
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
 Create a new version of a record-specific document and assign it an external id.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/set-status",
    "view_func_name":"document_set_status",
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
 Set the status of a record-specific document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/status-history",
    "view_func_name":"document_status_history",
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
 List all changes to a document's status over time.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/versions/",
    "view_func_name":"document_versions",
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
 Retrieve the versions of a document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/inbox/{MESSAGE_ID}",
    "view_func_name":"record_send_message",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}",
    "view_func_name":"record_message_attach",
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
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/notifications/",
    "view_func_name":"record_notify",
    "access_doc":"Any admin app, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Send a notification about a record to all accounts authorized to be notified.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/notify",
    "view_func_name":"record_notify",
    "access_doc":"Any admin app, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Send a notification about a record to all accounts authorized to be notified.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/owner",
    "view_func_name":"record_get_owner",
    "access_doc":"A principal in full control of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Get the owner of a record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/owner",
    "view_func_name":"record_set_owner",
    "access_doc":"Any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Set the owner of a record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/owner",
    "view_func_name":"record_set_owner",
    "access_doc":"Any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Set the owner of a record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/experimental/ccr",
    "view_func_name":"report_ccr",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Export patient data as a Continuity of Care Record (CCR) document.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/allergies/",
    "view_func_name":"allergy_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the allergy data for a given record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/equipment/",
    "view_func_name":"equipment_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the equipment data for a given record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/immunizations/",
    "view_func_name":"immunization_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the immunization data for a given record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/labs/",
    "view_func_name":"lab_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the lab data for a given record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/measurements/{LAB_CODE}/",
    "view_func_name":"measurement_list",
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
 List the measurement data for a given record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/medications/",
    "view_func_name":"medication_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the medication data for a given record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/problems/",
    "view_func_name":"problem_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the problem data for a given record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/procedures/",
    "view_func_name":"procedure_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the procedure data for a given record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/simple-clinical-notes/",
    "view_func_name":"simple_clinical_notes_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the simple_clinical_notes data for a given record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/vitals/",
    "view_func_name":"vitals_list",
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the vitals data for a given record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/vitals/{CATEGORY}/",
    "view_func_name":"vitals_list",
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
 List the vitals data for a given record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/records/{RECORD_ID}/shares/",
    "view_func_name":"record_shares",
    "access_doc":"The owner of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 List the shares of a record.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/shares/",
    "view_func_name":"record_share_add",
    "access_doc":"The owner of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":'''
 Fully share a record with another account.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"DELETE",
    "path":"/records/{RECORD_ID}/shares/{OTHER_ACCOUNT_ID}",
    "view_func_name":"record_share_delete",
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
 Undo a full record share with an account.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"POST",
    "path":"/records/{RECORD_ID}/shares/{OTHER_ACCOUNT_ID}/delete",
    "view_func_name":"record_share_delete",
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
 Undo a full record share with an account.
''',
    "return_desc":"DESCRIBE THE VALUES THAT THE CALL RETURNS",
    "return_ex":'''
GIVE AN EXAMPLE OF A RETURN VALUE
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/static/{PATH}",
    "view_func_name":"serve",
    "access_doc":"",
    "url_params":{
        'PATH':'The path to a static resource. Relative to the indivo_server static directory.',
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
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/version",
    "view_func_name":"get_version",
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
    "deprecated": None,
    "added": None,
    "changed": None,

}]