

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
        'contact_email':'A valid email at which to reach the account holder.',
        'secondary_secret_p':'0 or 1: Does this account require a secondary secret?',
        'primary_secret_p':'0 or 1: Does this account require a primary secret?',
        'account_id':'An identifier for the new account. Must be a valid email address. **REQUIRED**',
        'full_name':'The full name to associate with the account.',
        },
    "description":"Create a new account, and send out initialization emails.",
    "return_desc":":http:statuscode:`200` with information about the new account on success, :http:statuscode:`400` if ``ACCOUNT_ID`` isn't passed or is already used.",
    "return_ex":'''
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
        'fullname':'The full name of the account to search for',
        'contact_email':'The contact email of the account to search for',
        },
    "data_fields":{
        },
    "description":"Search for accounts by name or email.",
    "return_desc":":http:statuscode:`200` with information about matching accounts, or :http:statuscode:`400` if no search parameters are passed.",
    "return_ex":'''
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
    "description":"Display information about an account.",
    "return_desc":":http:statuscode:`200` with information about the account",
    "return_ex":'''
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
        'username':'The username for this account',
        'password':'The password for this account',
        'system':'The identifier of the desired authsystem. ``password`` indicates the              internal password system.',
        },
    "description":"Add a new method of authentication to an account.",
    "return_desc":":http:statuscode:`200 Success`, :http:statuscode:`403` if the indicated auth system doesn't exist, and :http:statuscode:`400` if a system and a username weren't passed, or if the account is already registered with the passed system, or if the username is already taken for the passed authsystem.",
    "return_ex":'''
<ok/>
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
        'new':'The desired new password.',
        'old':'The existing account password.',
        },
    "description":"Change a account's password.",
    "return_desc":":http:statuscode:`200 Success`, :http:statuscode:`403` if the old password didn't validate, or :http:statuscode:`400` if both a new and old password weren't passed.",
    "return_ex":'''
<ok/>
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
        'password':'The new password to set.',
        },
    "description":"Force the password of an account to a given value.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`400` if a new password wasn't passed.",
    "return_ex":'''
<ok/>
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
        'username':'The new username to set.',
        },
    "description":"Force the username of an account to a given value.",
    "return_desc":":http:statuscode:`200 Success`, :http:statuscode:`400` if a username wasn't passed.",
    "return_ex":'''
<ok/>
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
        'secondary_secret':'The secondary secret of the account to check.',
        },
    "data_fields":{
        },
    "description":"Validate an account's primary and secondary secrets.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`403` if validation fails.",
    "return_ex":'''
<ok/>
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
    "description":"Resets an account if the user has forgotten its password.",
    "return_desc":":http:statuscode`200` with the account's new secondary secret, or :http:statuscode:`400` if the account hasn't yet been initialized.",
    "return_ex":'''
<secret>123456</secret>
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
        'status':'The account or document status to filter by',
        'limit':'See :ref:`query-operators`',
        'order_by':'See :ref:`query-operators`',
        'include_archive':'0 or 1: whether or not to include archived messages in the result set.',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List messages in an account's inbox.",
    "return_desc":":http:statuscode:`200`, with a list of inbox messages.",
    "return_ex":'''
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
        'body':'The message body. Defaults to ``[no body]``.',
        'subject':'The message subject. Defaults to ``[no subject]``.',
        'message_id':'An external identifier for the message.',
        'severity':'The importance of the message. Options are ``low``, ``medium``, ``high``. Defaults to ``low``.',
        },
    "description":"Send a message to an account.",
    "return_desc":":http:statuscode:`200 Success`, or http:statuscode:`400` if the passed message_id is a duplicate. Also emails account to alert them that a new message has arrived.",
    "return_ex":'''
<ok/>
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
    "description":"Retrieve an individual message from an account's inbox.",
    "return_desc":":http:statuscode:`200`, with XML describing the message.",
    "return_ex":'''
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
    "description":"Archive a message.",
    "return_desc":":http:statuscode:`200 Success`.",
    "return_ex":'''
<ok/>
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
    "description":"Accept a message attachment into the record it corresponds to.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`410` if the attachment has already been saved.",
    "return_ex":'''
<ok/>
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
        'contact_email':'A valid email at which to reach the account holder.',
        'full_name':'The full name of the account.',
        },
    "description":"Set basic information about an account.",
    "return_desc":":http:statuscode:`200`, or :http:statuscode:`400` if no parameters are passed in.",
    "return_ex":'''
<ok/>
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
        'secondary_secret':'',
        },
    "description":"Initialize an account, activating it.",
    "return_desc":":http:statuscode:`200 Success`, :http:statuscode:`403` if the account has already been initialized or if secrets didn't validate, and :http:statuscode:`400` if a secondary secret was required but missing.",
    "return_ex":'''
<ok/>
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
        'status':'The account or document status to filter by',
        'order_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List an account's notifications.",
    "return_desc":":http:statuscode:`200` with a list of the account's notifications.",
    "return_ex":'''
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
    "description":"List the carenets that an account has access to.",
    "return_desc":":http:statuscode:`200` with a list of carenets.",
    "return_ex":'''
<Carenets record_id="01234">
    <Carenet id="456" name="family" mode="explicit" />
    <Carenet id="567" name="school" mode="explicit" />
</Carenets>
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
    "description":"Display an account's primary secret.",
    "return_desc":":http:statuscode:`200`, with the primary secret.",
    "return_ex":'''
<secret>123absxzyasdg13b</secret>
''',
    "deprecated": ('1.0.0', 'Avoid sending primary secrets over the wire. Instead, use :http:get:`/accounts/{ACCOUNT_EMAIL}/check-secrets/{PRIMARY_SECRET}`.'),
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
        'status':'The account or document status to filter by',
        'limit':'See :ref:`query-operators`',
        'order_by':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List all available records for an account.",
    "return_desc":":http:statuscode:`200`, with a list of records owned or shared with the account.",
    "return_ex":'''
<Records>
  <Record id="123" label="John R. Smith" />
  <Record id="234" label="John R. Smith Jr. (shared)" shared="true" role_label="Guardian" />
  <Record id="345" label="Juanita R. Smith (carenet)" shared="true" carenet_id="678" carenet_name="family" />

  ...

</Records>
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
    "description":"Reset an account to an ``uninitialized`` state.",
    "return_desc":":http:statuscode:`200 Success`.",
    "return_ex":'''
<ok/>
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
    "description":"Return the secondary secret of an account.",
    "return_desc":":http:statuscode:`200`, with the secondary secret.",
    "return_ex":'''
<secret>123456</secret>
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
    "description":"Sends an account user their primary secret in case they lost it.",
    "return_desc":":http:statuscode:`200 Success`. Also emails the account with their new secret.",
    "return_ex":'''
<ok/>
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
        'state':'The desired state of the account. Options are ``active``, ``disabled``, ``retired``.',
        },
    "description":"Set the state of an account.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`403` if the account has been retired and can no longer change state.",
    "return_ex":'''
<ok/>
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
    "description":"List all available userapps.",
    "return_desc":":http:statuscode:`200`, with a list of userapps.",
    "return_ex":'''
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
    "description":"Delete a userapp from Indivo.",
    "return_desc":":http:statuscode:`200 Success`.",
    "return_ex":'''
<ok/>
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
    "description":"Return a description of a single userapp.",
    "return_desc":":http:statuscode:`200`, with information about the userapp.",
    "return_ex":'''
<App id="problems@apps.indivo.org">
  <startURLTemplate>http://problems.indivo.org/auth/start?record_id={record_id}&amp;carenet_id={carenet_id}</startURLTemplate>
  <name>Problem List</name>
  <description>Managing your problem list</description>
  <autonomous>false</autonomous>
  <frameable>true</frameable>
  <ui>true</ui>
</App>
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
        'status':'The account or document status to filter by',
        'type':'The Indivo document type to filter by',
        'order_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List app-specific documents.",
    "return_desc":":http:statuscode:`200` with A list of documents, or http:statuscode:`404` if an invalid type was passed in the querystring.",
    "return_ex":'''
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
        '':'The raw content of the document to create.',
        },
    "description":"Create an app-specific Indivo document.",
    "return_desc":":http:statuscode:`200` with the metadata of the created document, or :http:statuscode:`400` if the new document failed validation.",
    "return_ex":'''
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
        '':'The raw content of the document to create.',
        },
    "description":"Create an app-specific Indivo document with an associated external id.",
    "return_desc":":http:statuscode:`200` with the metadata of the created or updated document, or :http:statuscode:`400` if the passed content didn't validate.",
    "return_ex":'''
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
    "description":"Fetch the metadata of an app-specific document identified by external id.",
    "return_desc":":http:statuscode:`200` with metadata describing the specified document, or http:statuscode:`404` if the external_id is invalid.",
    "return_ex":'''
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
    "description":"Delete an app-specific document.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.",
    "return_ex":'''
</ok>
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
    "description":"Retrive an app-specific document.",
    "return_desc":":http:statuscode:`200` with the raw content of the document, or :http:statuscode:`404` if the document could not be found.",
    "return_ex":'''
<DefaultProblemsPreferences record_id="123">
  <Preference name="hide_void" value="true" />
  <Preference name="show_rels" value="false" />
</DefaultProblemsPreferences>
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
        '':'The raw content of the document to create.',
        },
    "description":"Create or Overwrite an app-specific Indivo document.",
    "return_desc":":http:statuscode:`200` with metadata describing the created or updated document, or :http:statuscode:`400` if the passed content didn't validate.",
    "return_ex":'''
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
        '':'The new label for the document',
        },
    "description":"Set the label of an app-specific document.",
    "return_desc":":http:statuscode:`200` with metadata describing the re-labeled document, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.",
    "return_ex":'''
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
    "description":"Fetch the metadata of an app-specific document.",
    "return_desc":":http:statuscode:`200` with the document metadata, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.",
    "return_ex":'''
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
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/apps/{PHA_EMAIL}/records/",
    "view_func_name":"app_record_list",
    "access_doc":"Any autonomous user app.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"Return a list of all records that have this pha enabled.",
    "return_desc":":http:statuscode:`200` with a list of records on success.",
    "return_ex":'''
<Records>
  <Record id="123" label="John R. Smith" />
  <Record id = "234" label="Frank Frankson" />

  ...

</Records>
''',
    "deprecated": None,
    "added": ('1.0.0', ''),
    "changed": None,

},
{
    "method":"POST",
    "path":"/apps/{PHA_EMAIL}/records/{RECORD_ID}/access_token",
    "view_func_name":"autonomous_access_token",
    "access_doc":"An autonomous user app with a record on which the app is authorized to run.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"Fetch an access token for an autonomous app to access a record.",
    "return_desc":":http:statuscode:`200` with a valid access token for the app bound to the record on success.",
    "return_ex":'''
oauth_token=abcd1fw3gasdgh3&oauth_token_secret=jgrlhre4291hfjas&xoauth_indivo_record_id=123
''',
    "deprecated": None,
    "added": ('1.0.0', ''),
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
    "description":"Delete a carenet.",
    "return_desc":":http:statuscode:`200 Success`.",
    "return_ex":'''
<ok/>
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
    "description":"List the accounts in a carenet.",
    "return_desc":":http:statuscode:`200` with a list of accounts in the specified carenet.",
    "return_ex":'''
<CarenetAccounts>
  <CarenetAccount id="johndoe@indivo.org" fullName="John Doe" write="true" />

  ...

</CarenetAccounts>
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
        'write':'``true`` or ``false``. Whether this account can write to the carenet.',
        'account_id':'An identifier for the account. Must be a valid email address.',
        },
    "description":"Add an account to a carenet.",
    "return_desc":":http:statuscode:`200 Success`, :http:statuscode:`404` if the specified account or carenet don't exist, or :http:statuscode:`400` if an account_id isn't passed.",
    "return_ex":'''
<ok/>
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
    "description":"Remove an account from a carenet.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`404` if either the passed account or the passed carenet doesn't exist.",
    "return_ex":'''
<ok/>
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
    "description":"List the permissions of an account within a carenet.",
    "return_desc":":http:statuscode:`200` with a list of document types that the account can access within a carenet. Currently always returns all document types.",
    "return_ex":'''
<Permissions>
  <DocumentType type="*" write="true" />
</Permissions>
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
    "description":"List Apps within a given carenet.",
    "return_desc":":http:statuscode:`200` with a list of applications in the carenet.",
    "return_ex":'''
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
    "description":"Remove an app from a given carenet.",
    "return_desc":":http:statuscode:`200 Success`.",
    "return_ex":'''
<ok/>
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
    "description":"Add an app to a carenet",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`400` if the passed PHA is autonomous (autonomous apps can't be scoped to carenets).",
    "return_ex":'''
<ok/>
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/apps/{PHA_EMAIL}/permissions",
    "view_func_name":"carenet_app_permissions",
    "access_doc":"Nobody",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"Retrieve the permissions for an app within a carenet. NOT IMPLEMENTED.",
    "return_desc":":http:statuscode:`200`. This call is unimplemented, and has no effect.",
    "return_ex":'''
<ok/>
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
        'type':'The Indivo document type to filter by',
        },
    "data_fields":{
        },
    "description":"List documents from a given carenet.",
    "return_desc":":http:statuscode:`200` with a document list on success, :http:statuscode:`404` if *type* doesn't exist.",
    "return_ex":'''
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
    "description":"Read a special document from a carenet.",
    "return_desc":":http:statuscode:`200` with the special document's raw content, or :http:statuscode:`404` if the document hasn't been created yet.",
    "return_ex":'''
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
        'CARENET_ID':'The id string associated with the Indivo carenet',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"Return a document from a carenet.",
    "return_desc":":http:statuscode:`200` with the document content on success, :http:statuscode:`404` if document_id is invalid or if the document is not shared in the carenet.",
    "return_ex":'''
<ExampleDocument>
  <content>That's my content</content>
  <otherField attr="val" />
</ExampleDocument>
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
        'CARENET_ID':'The id string associated with the Indivo carenet',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"Fetch the metadata of a record-specific document via a carenet.",
    "return_desc":":http:statuscode:`200` with the document's metadata, or :http:statuscode:`404` if ``document_id`` doesn't identify an existing document in the carenet.",
    "return_ex":'''
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
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/carenets/{CARENET_ID}/record",
    "view_func_name":"carenet_record",
    "access_doc":"Nobody",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"Get basic information about the record to which a carenet belongs.",
    "return_desc":":http:statuscode:`200` with XML describing the record.",
    "return_ex":'''
<Record id="123" label="Joe User">
  <contact document_id="790" />
  <demographics document_id="467" />
  <created at="2010-10-23T10:23:34Z" by="indivoconnector@apps.indivo.org" />
</Record>
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
        'name':'The new name for the carenet.',
        },
    "description":"Change a carenet's name.",
    "return_desc":":http:statuscode:`200` with XML describing the renamed carenet on success, :http:statuscode:`400` if ``name`` wasn't passed or if a carenet named ``name`` already exists on this record.",
    "return_ex":'''
<Carenets record_id="123">
    <Carenet id="789" name="Work/School" mode="explicit" />
</Carenets>
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the allergy data for a given carenet.",
    "return_desc":":http:statuscode:`200` with a list of allergies, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the equipment data for a given carenet.",
    "return_desc":":http:statuscode:`200` with a list of equipment, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the immunization data for a given carenet.",
    "return_desc":":http:statuscode:`200` with a list of immunizations, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the lab data for a given carenet.",
    "return_desc":":http:statuscode:`200` with a list of labs, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the measurement data for a given carenet.",
    "return_desc":":http:statuscode:`200` with a list of measurements, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the medication data for a given carenet.",
    "return_desc":":http:statuscode:`200` with a list of medications, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the problem data for a given carenet.",
    "return_desc":":http:statuscode:`200` with a list of problems, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the procedure data for a given carenet.",
    "return_desc":":http:statuscode:`200` with a list of procedures, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the simple_clinical_notes data for a given carenet.",
    "return_desc":":http:statuscode:`200` with a list of notes, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the vitals data for a given carenet.",
    "return_desc":":http:statuscode:`200` with a list of notes, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the vitals data for a given carenet.",
    "return_desc":":http:statuscode:`200` with a list of notes, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/codes/systems/",
    "view_func_name":"coding_systems_list",
    "access_doc":"Anybody",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"List available codingsystems. NOT IMPLEMENTED.",
    "return_desc":":http:statuscode:`500`, as the system cannot process the call.",
    "return_ex":'''
[{"short_name": "umls-snomed", "name": "UMLS SNOMED", "description" : "..."},
 {..},
 {..}]
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"GET",
    "path":"/codes/systems/{SYSTEM_SHORT_NAME}/query",
    "view_func_name":"coding_system_query",
    "access_doc":"Anybody",
    "url_params":{
        'SYSTEM_SHORT_NAME':'',
        },
    "query_opts":{
        'q':'The query string to search for',
        },
    "data_fields":{
        },
    "description":"Query a codingsystem for a value.",
    "return_desc":":http:statuscode:`200` with JSON describing codingsystems entries that matched *q*, or :http:statuscode:`404` if ``SYSTEM_SHORT_NAME`` is invalid.",
    "return_ex":'''
[{"abbreviation": null, "code": "38341003", "consumer_value": null,
  "umls_code": "C0020538",
  "full_value": "Hypertensive disorder, systemic arterial (disorder)"},
 {"abbreviation": null, "code": "55822004", "consumer_value": null,
  "umls_code": "C0020473", "full_value": "Hyperlipidemia (disorder)"}]
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
    "description":"Exchange a request token for a valid access token.",
    "return_desc":":http:statuscode:`200` with an access token, or :http:statuscode:`403` if the request token didn't validate.",
    "return_ex":'''
oauth_token=abcd1fw3gasdgh3&oauth_token_secret=jgrlhre4291hfjas&xoauth_indivo_record_id=123
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
        'record_id':'The record to bind to. Either *record_id* or *carenet_id* is required.',
        'carenet_id':'The carenet to bind to. Either *record_id* or *carenet_id* is required.',
        },
    "description":"Indicate a user's consent to bind an app to a record or carenet.",
    "return_desc":":http:statuscode:`200` with a redirect url to the app on success, :http:statuscode:`403` if *record_id*/*carenet_id* don't match *reqtoken*.",
    "return_ex":'''
location=http%3A%2F%2Fapps.indivo.org%2Fproblems%2Fafter_auth%3Foauth_token%3Dabc123%26oauth_verifier%3Dabc123

(which is the urlencoded form of:

http://apps.indivo.org/problems/after_auth?oauth_token=abc123&oauth_verifier=abc123 )
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
    "description":"Claim a request token on behalf of an account.",
    "return_desc":":http:statuscode:`200` with the email of the claiming principal, or :http:statuscode:`403` if the token has already been claimed.",
    "return_ex":'''
joeuser@indivo.org
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
    "description":"Get information about a request token.",
    "return_desc":":http:statuscode:`200` with information about the token.",
    "return_ex":'''
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
        'username':'The username of the user to authenticate.',
        'password':'The password to use with *username* against the internal password auth system. EITHER *password* or *system* is **Required**.',
        'system':'An external auth system to authenticate the user with. EITHER *password* or *system* is **Required**.',
        },
    "description":"Authenticate a user and register a web session for them.",
    "return_desc":":http:statuscode:`200` with a valid session token, or :http:statuscode:`403` if the passed credentials were invalid.",
    "return_ex":'''
oauth_token=XYZ&oauth_token_secret=ABC&account_id=joeuser%40indivo.org
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
        'surl_sig':'The computed signature (base-64 encoded sha1) of the url.',
        'surl_timestamp':'when the url was generated. Must be within the past hour.',
        'surl_token':'The access token used to sign the url.',
        },
    "data_fields":{
        },
    "description":"Verify a signed URL.",
    "return_desc":":http:statuscode:`200` with XML describing whether the surl validated.",
    "return_ex":'''
If the surl validated:

<result>ok</result>

If the surl was too old:

<result>old</result>

If the surl's signature was invalid:

<result>mismatch</result>
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
        'indivo_record_id':'The record to which to bind the request token. EITHER *indivo_record_id* or *indivo_carenet_id* is **REQUIRED**.',
        'indivo_carenet_id':'The carenet to which to bind the request token. EITHER *indivo_record_id* or *indivo_carenet_id* is **REQUIRED**.',
        },
    "description":"Get a new request token, bound to a record or carenet if desired.",
    "return_desc":":http:statuscode:`200` with the request token on success, :http:statuscode:`403` if the oauth signature on the request of missing or faulty.",
    "return_ex":'''
oauth_token=abcd1fw3gasdgh3&oauth_token_secret=jgrlhre4291hfjas&xoauth_indivo_record_id=123
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
        '':'A valid Indivo Contact Document (see :doc:`/schemas/contact-schema`).',
        },
    "description":"Create a new record.",
    "return_desc":":http:statuscode:`200` with information about the record on success, :http:statuscode:`400` if the contact XML was empty or invalid.",
    "return_ex":'''
<Record id="123" label="Joe Smith">
  <contact document_id="234" />
  <demographics document_id="" />
</Record>
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
        'PRINCIPAL_EMAIL':'The email with which to scope an external id.',
        'EXTERNAL_ID':'The external identifier of the desired resource',
        },
    "query_opts":{
        },
    "data_fields":{
        '':'A valid Indivo Contact Document (see :doc:`/schemas/contact-schema`).',
        },
    "description":"Create a new record with an associated external id.",
    "return_desc":":http:statuscode:`200` with information about the record on success, :http:statuscode:`400` if the contact XML was empty or invalid.",
    "return_ex":'''
<Record id="123" label="Joe Smith">
  <contact document_id="234" />
  <demographics document_id="" />
</Record>
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
    "description":"Get information about an individual record.",
    "return_desc":":http:statuscode:`200` with information about the record.",
    "return_ex":'''
<Record id="123" label="Joe Smith">
  <contact document_id="234" />
  <demographics document_id="346" />
</Record>
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
        'type':'A namespaced document type. If specified, only apps which explicitly declare themselves as supporting that document type will be returned.',
        },
    "data_fields":{
        },
    "description":"List userapps bound to a given record.",
    "return_desc":":http:statuscode:`200` with a list of userapps.",
    "return_ex":'''
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
    "description":"Remove a userapp from a record.",
    "return_desc":":http:statuscode:`200 Success`.",
    "return_ex":'''
<ok/>
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
    "description":"Get information about a given userapp bound to a record.",
    "return_desc":":http:statuscode:`200` with information about the app, or :http:statuscode:`404` if the app isn't bound to the record.",
    "return_ex":'''
<App id="problems@apps.indivo.org">
  <startURLTemplate>http://problems.indivo.org/auth/start?record_id={record_id}&amp;carenet_id={carenet_id}</startURLTemplate>
  <name>Problem List</name>
  <description>Managing your problem list</description>
  <autonomous>false</autonomous>
  <frameable>true</frameable>
  <ui>true</ui>
</App>
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}",
    "view_func_name":"record_pha_enable",
    "access_doc":"Any admin app, or a principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"Enable a userapp for a record.",
    "return_desc":":http:statuscode:`200` on success, :http:statuscode:`404` if either the specified record or the specified app doesn't exist.",
    "return_ex":'''
<ok/>
''',
    "deprecated": None,
    "added": ('1.0.0', ''),
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
        'status':'The account or document status to filter by',
        'type':'The Indivo document type to filter by',
        'order_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List record-app-specific documents.",
    "return_desc":":http:statuscode:`200` with a list of documents, or :http:statuscode:`404` if an invalid type was passed in the querystring.",
    "return_ex":'''
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
        '':'The raw content of the document to create.',
        },
    "description":"Create a record-app-specific Indivo document.",
    "return_desc":":http:statuscode:`200` with the metadata of the created document, or :http:statuscode:`400` if the new document failed validation.",
    "return_ex":'''
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
        '':'The raw content of the document to create/update.',
        },
    "description":"Create or Overwrite a record-app-specific Indivo document with an associated external id.",
    "return_desc":":http:statuscode:`200` with metadata describing the created or updated document, or :http:statuscode:`400` if the passed content didn't validate.",
    "return_ex":'''
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
        '':'The raw content of the document to create/update.',
        },
    "description":"Create or Overwrite a record-app-specific Indivo document with an associated external id.",
    "return_desc":":http:statuscode:`200` with metadata describing the created or updated document, or :http:statuscode:`400` if the passed content didn't validate.",
    "return_ex":'''
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
    "description":"Fetch the metadata of a record-app-specific document identified by external id.",
    "return_desc":":http:statuscode:`200` with metadata describing the specified document, or http:statuscode:`404` if the external_id is invalid.",
    "return_ex":'''
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
    "description":"Delete a record-app-specific document.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.",
    "return_ex":'''
<ok/>
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
    "description":"Retrieve a record-app-specific document.",
    "return_desc":":http:statuscode:`200` with the raw content of the document, or :http:statuscode:`404` if the document could not be found.",
    "return_ex":'''
<ProblemsPreferences record_id="123">
  <Preference name="hide_void" value="true" />
  <Preference name="show_rels" value="false" />
</ProblemsPreferences>
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
        '':'The new label for the document',
        },
    "description":"Set the label of a record-app-specific document.",
    "return_desc":":http:statuscode:`200` with metadata describing the re-labeled document, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.",
    "return_ex":'''
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
    "description":"Fetch the metadata of a record-app-specific document.",
    "return_desc":":http:statuscode:`200` with the document metadata, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.",
    "return_ex":'''
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
        '':'Raw content that will be used as a setup document for the record. **OPTIONAL**.',
        },
    "description":"Bind an app to a record without user authorization.",
    "return_desc":":http:statuscode:`200` with a valid access token for the newly set up app.",
    "return_ex":'''
oauth_token=abcd1fw3gasdgh3&oauth_token_secret=jgrlhre4291hfjas&xoauth_indivo_record_id=123
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
        'order_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"Return audits of calls touching *record*.",
    "return_desc":":http:statuscode:`200`, with a list of Audit Reports.",
    "return_ex":'''
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
''',
    "deprecated": ('0.9.3', 'Use :http:get:`/records/{RECORD_ID}/audits/query/` instead.'),
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
        'order_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"Return audits of calls touching *record* and *document_id*.",
    "return_desc":":http:statuscode:`200`, with a list of Audit Reports.",
    "return_ex":'''
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
''',
    "deprecated": ('0.9.3', 'Use :http:get:`/records/{RECORD_ID}/audits/query/` instead.'),
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
        'order_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"Return audits of calls to *function_name* touching *record* and *document_id*.",
    "return_desc":":http:statuscode:`200`, with a list of Audit Reports.",
    "return_ex":'''
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
''',
    "deprecated": ('0.9.3', 'Use :http:get:`/records/{RECORD_ID}/audits/query/` instead.'),
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`audit-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"Select Audit Objects via the Query API Interface.",
    "return_desc":":http:statuscode:`200` with a list of audit records, or :http:statuscode:`400` if any of the arguments to the query interface are invalid.",
    "return_ex":'''
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
''',
    "deprecated": None,
    "added": ('0.9.3', ''),
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
        'type':'The document schema type to check autoshares for. **REQUIRED**.',
        },
    "data_fields":{
        },
    "description":"For a single record, list all carenets that a given doctype is autoshared with.",
    "return_desc":":http:statuscode:`200` with a list of carenets, or :http:statuscode:`404` if the passed document type is invalid.",
    "return_ex":'''
<Carenets record_id="123">
  <Carenet id="789" name="Work/School" mode="explicit" />

  ...

</Carenets>
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
    "description":"For a single record, list all doctypes autoshared into carenets.",
    "return_desc":":http:statuscode:`200` with a list of doctypes and their shared carenets.",
    "return_ex":'''
<DocumentSchemas>
  <DocumentSchema type="http://indivo.org/vocab/xml/documents#Medication">
    <Carenet id="123" name="Family" mode="explicit" />

    ...

  </DocumentSchema>

  ...

</DocumentSchemas>
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
        'type':'the document schema type to create an autoshare for',
        },
    "description":"Automatically share all documents of a certain type into a carenet.",
    "return_desc":":http:statuscode:`200`, or :http:statuscode:`404` if the passed document type doesn't exist.",
    "return_ex":'''
<ok/>
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
        'type':'the document schema type to remove an autoshare for',
        },
    "description":"Remove an autoshare from a carenet.",
    "return_desc":":http:statuscode:`200`, or :http:statuscode:`404` if the passed document type doesn't exist.",
    "return_ex":'''
<ok/>
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
    "description":"List all carenets for a record.",
    "return_desc":":http:statuscode:`200`, with a list of carenets.",
    "return_ex":'''
<Carenets record_id="123">
  <Carenet id="789" name="Work/School" mode="explicit" />

  ...

</Carenets>
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
        'name':'The label for the new carenet.',
        },
    "description":"Create a new carenet for a record.",
    "return_desc":":http:statuscode:`200` with a description of the new carenet, or :http:statuscode:`400` if the name of the carenet wasn't passed or already exists.",
    "return_ex":'''
<Carenets record_id="123">
  <Carenet id="789" name="Work/School" mode="explicit" />
</Carenets>
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"DELETE",
    "path":"/records/{RECORD_ID}/documents/",
    "view_func_name":"documents_delete",
    "access_doc":"Nobody",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"Delete all documents associated with a record.",
    "return_desc":":http:statuscode:`200 Success`",
    "return_ex":'''
<ok/>
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
        'status':'The account or document status to filter by',
        'type':'The Indivo document type to filter by',
        'order_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List record-specific documents.",
    "return_desc":":http:statuscode:`200` with a list of documents, or :http:statuscode:`404` if an invalid type was passed in the querystring.",
    "return_ex":'''
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
        '':'The raw content of the document to create.',
        },
    "description":"Create a record-specific Indivo Document.",
    "return_desc":":http:statuscode:`200` with the metadata of the created document, or :http:statuscode:`400` if the new document failed validation.",
    "return_ex":'''
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
        '':'The raw content of the document to create.',
        },
    "description":"Create a record-specific Indivo Document with an associated external id.",
    "return_desc":":http:statuscode:`200` with the metadata of the created document, or :http:statuscode:`400` if the new document failed validation, or if the external id was taken.",
    "return_ex":'''
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
        '':'The new label for the document',
        },
    "description":"Set the label of a record-specific document, specified by external id.",
    "return_desc":":http:statuscode:`200` with metadata describing the re-labeled document, or :http:statuscode:`404` if ``EXTERNAL_ID`` is invalid.",
    "return_ex":'''
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
    "description":"Fetch the metadata of a record-specific document identified by external id.",
    "return_desc":":http:statuscode:`200` with the document metadata, or :http:statuscode:`404` if ``EXTERNAL_ID`` is invalid.",
    "return_ex":'''
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
    "description":"Read a special document from a record.",
    "return_desc":":http:statuscode:`200` with the special document's raw content, or :http:statuscode:`404` if the document hasn't been created yet.",
    "return_ex":'''
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
        '':'The raw content of the document to create.',
        },
    "description":"Create or update a special document on a record.",
    "return_desc":":http:statuscode:`200` with metadata on the updated document, or :http:statuscode:`400` if the new content didn't validate.",
    "return_ex":'''
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
        '':'The raw content of the document to create.',
        },
    "description":"Create or update a special document on a record.",
    "return_desc":":http:statuscode:`200` with metadata on the updated document, or :http:statuscode:`400` if the new content didn't validate.",
    "return_ex":'''
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
    "description":"Create a new relationship between two existing documents.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`404` if ``DOCUMENT_ID_0``, ``DOCUMENT_ID_1``, or ``REL`` don't exist.",
    "return_ex":'''
<ok/>
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
    "description":"Retrieve a record-specific document.",
    "return_desc":":http:statuscode:`200` with the raw content of the document, or :http:statuscode:`404` if the document could not be found.",
    "return_ex":'''
<HBA1C xmlns="http://indivo.org/vocab#" value="5.3" unit="percent" datetime="2011-01-15T17:00:00.000Z" />
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
    "description":"List all the carenets into which a document has been shared.",
    "return_desc":":http:statuscode:`200` with a list of carenets.",
    "return_ex":'''
<Carenets record_id="123">
  <Carenet id="789" name="Work/School" mode="explicit" />

  ...

</Carenets>
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
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"Unshare a document from a given carenet.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid or if either the passed carenet or document do not belong to the passed record.",
    "return_ex":'''
<ok/>
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
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"Place a document into a given carenet.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid or nevershared.",
    "return_ex":'''
<ok/>
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
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"Revert the document-sharing of a document in a carent to whatever rules are specified by autoshares. NOT IMPLEMENTED.",
    "return_desc":":http:statuscode:`200 Success`.",
    "return_ex":'''
<ok/>
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
        '':'The new label for the document',
        },
    "description":"Set the label of a record-specific document.",
    "return_desc":":http:statuscode:`200` with metadata describing the re-labeled document, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.",
    "return_ex":'''
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
    "description":"Fetch the metadata of a record-specific document.",
    "return_desc":":http:statuscode:`200` with the document metadata, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.",
    "return_ex":'''
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
''',
    "deprecated": None,
    "added": None,
    "changed": None,

},
{
    "method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/meta",
    "view_func_name":"update_document_meta",
    "access_doc":"Nobody",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"Set metadata fields on a document. NOT IMPLEMENTED.",
    "return_desc":":http:statuscode:`200 Success`.",
    "return_ex":'''
<ok/>
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
    "description":"Remove the nevershare flag from a document.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.",
    "return_ex":'''
<ok/>
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
    "description":"Flag a document to never be shared, anywhere.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.",
    "return_ex":'''
<ok/>
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
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        'REL':'The type of relationship between the documents, i.e. ``annotation``, ``interpretation``',
        },
    "query_opts":{
        'status':'The account or document status to filter by.',
        'order_by':'See :ref:`query-operators`. **CURRENTLY UNIMPLEMENTED**.',
        'limit':'See :ref:`query-operators`. **CURRENTLY UNIMPLEMENTED**.',
        'offset':'See :ref:`query-operators`. **CURRENTLY UNIMPLEMENTED**',
        },
    "data_fields":{
        },
    "description":"Get all documents related to the passed document_id by a relation of the passed relation-type.",
    "return_desc":":http:statuscode:`200` with a list of related documents, or :http:statuscode:`400` if ``DOCUMENT_ID`` is invalid.",
    "return_ex":'''
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
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        'REL':'The type of relationship between the documents, i.e. ``annotation``, ``interpretation``',
        },
    "query_opts":{
        },
    "data_fields":{
        '':'The raw content of the document to create.',
        },
    "description":"Create a document and relate it to an existing document.",
    "return_desc":":http:statuscode:`200 Success`, :http:statuscode:`400` if the new content was invalid, or :http:statuscode:`404` if ``DOCUMENT_ID`` or ``REL`` are invalid.",
    "return_ex":'''
<ok/>
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
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        'EXTERNAL_ID':'The external identifier of the desired resource',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'REL':'The type of relationship between the documents, i.e. ``annotation``, ``interpretation``',
        },
    "query_opts":{
        },
    "data_fields":{
        '':'The raw content of the document to create.',
        },
    "description":"Create a document, assign it an external id, and relate it to an existing document.",
    "return_desc":":http:statuscode:`200 Success`, :http:statuscode:`400` if the new content was invalid, or :http:statuscode:`404` if ``DOCUMENT_ID`` or ``REL`` are invalid.",
    "return_ex":'''
<ok/>
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
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        'EXTERNAL_ID':'The external identifier of the desired resource',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'REL':'The type of relationship between the documents, i.e. ``annotation``, ``interpretation``',
        },
    "query_opts":{
        },
    "data_fields":{
        '':'The raw content of the document to create.',
        },
    "description":"Create a document, assign it an external id, and relate it to an existing document.",
    "return_desc":":http:statuscode:`200 Success`, :http:statuscode:`400` if the new content was invalid, or :http:statuscode:`404` if ``DOCUMENT_ID`` or ``REL`` are invalid.",
    "return_ex":'''
<ok/>
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
        '':'The raw content of the document to create.',
        },
    "description":"Create a new version of a record-specific document.",
    "return_desc":":http:statuscode:`200` with metadata on the new document, :http:statuscode:`400` if the old document has already been replaced by a newer version, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid or if the new content is invalid.",
    "return_ex":'''
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
        '':'The raw content of the document to create.',
        },
    "description":"Create a new version of a record-specific document and assign it an external id.",
    "return_desc":":http:statuscode:`200` with metadata on the new document, :http:statuscode:`400` if the old document has already been replaced by a newer version, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid or if the new content is invalid.",
    "return_ex":'''
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
        'status':'The new status for the document. Options are ``active``, ``void``, ``archived``.',
        'reason':'The reason for the status change.',
        },
    "description":"Set the status of a record-specific document.",
    "return_desc":":http:statuscode:`200 Success`, :http:statuscode:`400` if *status* or *reason* are missing, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.",
    "return_ex":'''
<ok/>
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
    "description":"List all changes to a document's status over time.",
    "return_desc":":http:statuscode:`200` with a the document's status history, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.",
    "return_ex":'''
<DocumentStatusHistory document_id="456">
  <DocumentStatus by="joeuser@indivo.example.org" at="2010-09-03T12:45:12Z" status="archived">
    <reason>no longer relevant</reason>
  </DocumentStatus>

  ...

</DocumentStatusHistory>
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
        'status':'The account or document status to filter by.',
        'order_by':'See :ref:`query-operators`.',
        'limit':'See :ref:`query-operators`.',
        'offset':'See :ref:`query-operators`.',
        },
    "data_fields":{
        },
    "description":"Retrieve the versions of a document.",
    "return_desc":":http:statuscode:`200` with a list of document versions, or :http:statuscode:`404` if ``DOCUMENT_ID`` is invalid.",
    "return_ex":'''
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
        'body':'The message body. Defaults to ``[no body]``.',
        'body_type':'The formatting for the message body. Options are ``plaintext``, ``markdown``. Defaults to ``plaintext``.',
        'num_attachments':'The number of attachments this message requires. Attachments are uploaded with calls to :http:post:`/records/{RECORD_ID}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}`. Defaults to 0.',
        'severity':'The importance of the message. Options are ``low``, ``medium``, ``high``. Defaults to ``low``.',
        'subject':'The message subject. Defaults to ``[no subject]``.',
        },
    "description":"Send a message to a record.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`400` if ``MESSAGE_ID`` was a duplicate. Also triggers notification emails to accounts authorized to view messages for the passed record.",
    "return_ex":'''
<ok/>
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
        '':'The raw XML attachment data.',
        },
    "description":"Attach a document to an Indivo message.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`400` if ``ATTACHMENT_NUM`` has already been uploaded.",
    "return_ex":'''
<ok/>
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
        'content':'The plaintext content of the notification.',
        'app_url':'A callback url to the app for more information. **OPTIONAL**.',
        'document_id':'The id of the document to which this notification pertains. **OPTIONAL**.',
        },
    "description":"Send a notification about a record to all accounts authorized to be notified.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`400` if *content* wasn't passed.",
    "return_ex":'''
<ok/>
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
        'content':'The plaintext content of the notification.',
        'app_url':'A callback url to the app for more information. **OPTIONAL**.',
        'document_id':'The id of the document to which this notification pertains. **OPTIONAL**.',
        },
    "description":"Send a notification about a record to all accounts authorized to be notified.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`400` if *content* wasn't passed.",
    "return_ex":'''
<ok/>
''',
    "deprecated": ('1.0', 'Use :http:post:`/records/{RECORD_ID}/notifications/` instead.'),
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
    "description":"Get the owner of a record.",
    "return_desc":":http:statuscode:`200 Success.`",
    "return_ex":'''
<Account id='joeuser@example.com' />
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
        '':'The email address of the new account owner.',
        },
    "description":"Set the owner of a record.",
    "return_desc":":http:statuscode:`200` with information about the account, or :http:statuscode:`400` if the passed email address is invalid.",
    "return_ex":'''
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
        '':'The email address of the new account owner.',
        },
    "description":"Set the owner of a record.",
    "return_desc":":http:statuscode:`200` with information about the account, or :http:statuscode:`400` if the passed email address is invalid.",
    "return_ex":'''
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
    "description":"Export patient data as a Continuity of Care Record (CCR) document.",
    "return_desc":":http:statuscode:`200` with an **EXPERIMENTAL** CCR document.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the allergy data for a given record.",
    "return_desc":":http:statuscode:`200` with a list of allergies, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the equipment data for a given record.",
    "return_desc":":http:statuscode:`200` with a list of equipment, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the immunization data for a given record.",
    "return_desc":":http:statuscode:`200` with a list of immunizations, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the lab data for a given record.",
    "return_desc":":http:statuscode:`200` with a list of labs, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the measurement data for a given record.",
    "return_desc":":http:statuscode:`200` with a list of measurements, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the medication data for a given record.",
    "return_desc":":http:statuscode:`200` with a list of medications, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the problem data for a given record.",
    "return_desc":":http:statuscode:`200` with a list of problems, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the procedure data for a given record.",
    "return_desc":":http:statuscode:`200` with a list of procedures, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the simple_clinical_notes data for a given record.",
    "return_desc":":http:statuscode:`200` with a list of notes, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the vitals data for a given record.",
    "return_desc":":http:statuscode:`200` with a list of notes, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
        'status':'The account or document status to filter by',
        '{FIELD}':'See :ref:`query-operators`, :ref:`valid-query-fields`',
        'order_by':'See :ref:`query-operators`',
        'aggregate_by':'See :ref:`query-operators`',
        'date_range':'See :ref:`query-operators`',
        'date_group':'See :ref:`query-operators`',
        'group_by':'See :ref:`query-operators`',
        'limit':'See :ref:`query-operators`',
        'offset':'See :ref:`query-operators`',
        },
    "data_fields":{
        },
    "description":"List the vitals data for a given record.",
    "return_desc":":http:statuscode:`200` with a list of notes, or :http:statuscode:`400` if any invalid query parameters were passed.",
    "return_ex":'''
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
    "description":"List the shares of a record.",
    "return_desc":":http:statuscode:`200` with a list of shares.",
    "return_ex":'''
<Shares record="123">
  <Share id="678" account="joeuser@example.com" />
  <Share id="789" pha="problems@apps.indivo.org" />

  ...

</Shares>
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
        'account_id':'The email address of the recipient account. **REQUIRED**.',
        'role_label':'A label for the share, usually the relationship between the owner and the recipient (i.e. ``Guardian``). **OPTIONAL**.',
        },
    "description":"Fully share a record with another account.",
    "return_desc":":http:statuscode:`200 Success`, :http:statuscode:`400` if *account_id* was not passed, or :http:statuscode:`404` if the passed *account_id* was invalid.",
    "return_ex":'''
<ok/>
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
    "description":"Undo a full record share with an account.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`404` if ``OTHER_ACCOUNT_ID`` is invalid.",
    "return_ex":'''
<ok/>
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
    "description":"Undo a full record share with an account.",
    "return_desc":":http:statuscode:`200 Success`, or :http:statuscode:`404` if ``OTHER_ACCOUNT_ID`` is invalid.",
    "return_ex":'''
<ok/>
''',
    "deprecated": ('1.0', 'Use :http:delete:`/records/{RECORD_ID}/shares/{OTHER_ACCOUNT_ID}` instead.'),
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
    "description":"Return the current version of Indivo.",
    "return_desc":":http:statuscode:`200` with the current version of Indivo.",
    "return_ex":'''
1.0.0.0
''',
    "deprecated": None,
    "added": None,
    "changed": None,

}]
