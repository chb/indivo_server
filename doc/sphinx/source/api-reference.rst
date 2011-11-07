
API Reference
=============

This page contains a full list of valid Indivo API calls, generated from the code.
For a more detailed walkthrough of individual calls, see :doc:`api`


--------

.. http:get:: /accounts/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_create
   :accesscontrol: Any admin app.


--------

.. http:get:: /accounts/forgot-password

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_forgot_password
   :accesscontrol: Any admin app.


--------

.. http:get:: /accounts/search

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_search
   :accesscontrol: Any admin app.


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_info
   :accesscontrol: Any admin app, or the Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/authsystems/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_authsystem_add
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/authsystems/password/change

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_password_change
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/authsystems/password/set

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_password_set
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/authsystems/password/set-username

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_username_set
   :accesscontrol: Any admin app, or the Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/check-secrets/{PRIMARY_SECRET}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_check_secrets
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :parameter PRIMARY_SECRET: A confirmation string sent securely to the patient from Indivo


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/inbox/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_inbox
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/inbox/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_send_message
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_inbox_message
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :parameter MESSAGE_ID: The unique identifier of the Indivo Message


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}/archive

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_message_archive
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :parameter MESSAGE_ID: The unique identifier of the Indivo Message


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}/accept

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_inbox_message_attachment_accept
   :accesscontrol: The Account owner.
   :parameter ATTACHMENT_NUM: The 1-indexed number corresponding to the message attachment
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :parameter MESSAGE_ID: The unique identifier of the Indivo Message


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/info-set

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_info_set
   :accesscontrol: Any admin app, or the Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/initialize/{PRIMARY_SECRET}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_initialize
   :accesscontrol: Any Indivo UI app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account
   :parameter PRIMARY_SECRET: A confirmation string sent securely to the patient from Indivo


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/notifications/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_notifications
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/permissions/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_permissions
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/primary-secret

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_primary_secret
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/records/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_list
   :accesscontrol: The Account owner.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/reset

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_reset
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/secret

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_secret
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account


--------

.. http:get:: /accounts/{ACCOUNT_EMAIL}/secret-resend

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_resend_secret
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account


--------

.. http:post:: /accounts/{ACCOUNT_EMAIL}/set-state

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: account_set_state
   :accesscontrol: Any admin app.
   :parameter ACCOUNT_EMAIL: The email identifier of the Indivo account


--------

.. http:get:: /apps/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: all_phas
   :accesscontrol: Any principal in Indivo.


--------

.. http:delete:: /apps/{PHA_EMAIL}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: pha_delete
   :accesscontrol: The user app itself.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:get:: /apps/{PHA_EMAIL}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: pha
   :accesscontrol: Any principal in Indivo.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:get:: /apps/{PHA_EMAIL}/documents/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: app_document_list
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:post:: /apps/{PHA_EMAIL}/documents/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: app_document_create
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:put:: /apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: app_document_create_or_update_ext
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:get:: /apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}/meta

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: app_document_meta_ext
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:delete:: /apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: app_document_delete
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: app_specific_document
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:put:: /apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: app_document_create_or_update
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/label

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: app_document_label
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/meta

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: app_document_meta
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/update

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: app_document_update
   :accesscontrol: A user app with an id matching the app email in the URL.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:delete:: /carenets/{CARENET_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_delete
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /carenets/{CARENET_ID}/accounts/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_account_list
   :accesscontrol: A principal in the carenet, in full control of the carenet's record, or any admin app.
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:post:: /carenets/{CARENET_ID}/accounts/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_account_create
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:delete:: /carenets/{CARENET_ID}/accounts/{ACCOUNT_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_account_delete
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter ACCOUNT_ID: The email identifier of the Indivo account
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /carenets/{CARENET_ID}/accounts/{ACCOUNT_ID}/permissions

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_account_permissions
   :accesscontrol: A user app with access to the carenet and proxying the account, a principal in full control of the carenet's record, or any admin app.
   :parameter ACCOUNT_ID: The email identifier of the Indivo account
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /carenets/{CARENET_ID}/apps/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_apps_list
   :accesscontrol: A principal in the carenet, in full control of the carenet's record, or any admin app.
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:delete:: /carenets/{CARENET_ID}/apps/{PHA_EMAIL}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_apps_delete
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:put:: /carenets/{CARENET_ID}/apps/{PHA_EMAIL}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_apps_create
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /carenets/{CARENET_ID}/apps/{PHA_EMAIL}/permissions

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_app_permissions
   :accesscontrol: 
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /carenets/{CARENET_ID}/documents/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_document_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /carenets/{CARENET_ID}/documents/special/{SPECIAL_DOCUMENT}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: read_special_document_carenet
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, an account in the carenet or in control of the record, or the admin app that created the carenet's record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :parameter SPECIAL_DOCUMENT: The type of special document to access. Options are ``demographics``, ``contact``


--------

.. http:get:: /carenets/{CARENET_ID}/documents/{DOCUMENT_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_document
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /carenets/{CARENET_ID}/documents/{DOCUMENT_ID}/meta

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_document_meta
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /carenets/{CARENET_ID}/record

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_record
   :accesscontrol: 
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:post:: /carenets/{CARENET_ID}/rename

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_rename
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/allergies/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_allergy_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/equipment/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_equipment_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/immunizations/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_immunization_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/measurements/{LAB_CODE}/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_measurement_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet
   :parameter LAB_CODE: The identifier corresponding to the measurement being made.


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/medications/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_medication_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/problems/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_problem_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/procedures/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_procedure_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/vitals/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_vitals_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /carenets/{CARENET_ID}/reports/minimal/vitals/{CATEGORY}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_vitals_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter CATEGORY: The category of vital sign, i.e. ``weight``, ``Blood_Pressure_Systolic``
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /codes/systems/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: coding_systems_list
   :accesscontrol: 


--------

.. http:get:: /codes/systems/{SYSTEM_SHORT_NAME}/query

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: coding_system_query
   :accesscontrol: 
   :parameter SYSTEM_SHORT_NAME: 


--------

.. http:get:: /id

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: get_id
   :accesscontrol: 


--------

.. http:get:: /oauth/access_token

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: exchange_token
   :accesscontrol: A request signed by a RequestToken.


--------

.. http:get:: /oauth/authorize

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: user_authorization
   :accesscontrol: 


--------

.. http:get:: /oauth/internal/long-lived-token

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: get_long_lived_token
   :accesscontrol: A request signed by an AccessToken.


--------

.. http:get:: /oauth/internal/request_tokens/{REQTOKEN_ID}/approve

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: request_token_approve
   :accesscontrol: A principal in the carenet to which the request token is restricted (if the token is restricted), or a principal with full control over the record (if the token is not restricted).
   :parameter REQTOKEN_ID: 


--------

.. http:get:: /oauth/internal/request_tokens/{REQTOKEN_ID}/claim

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: request_token_claim
   :accesscontrol: Any Account.
   :parameter REQTOKEN_ID: 


--------

.. http:get:: /oauth/internal/request_tokens/{REQTOKEN_ID}/info

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: request_token_info
   :accesscontrol: Any Account.
   :parameter REQTOKEN_ID: 


--------

.. http:get:: /oauth/internal/session_create

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: session_create
   :accesscontrol: Any Indivo UI app.


--------

.. http:get:: /oauth/internal/surl-verify

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: surl_verify
   :accesscontrol: Any Account.


--------

.. http:get:: /oauth/request_token

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: request_token
   :accesscontrol: Any user app.


--------

.. http:post:: /records/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_create
   :accesscontrol: Any admin app.


--------

.. http:put:: /records/external/{PRINCIPAL_EMAIL}/{EXTERNAL_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_create_ext
   :accesscontrol: An admin app with an id matching the principal_email in the URL.
   :parameter PRINCIPAL_EMAIL: 
   :parameter EXTERNAL_ID: The external identifier of the desired resource


--------

.. http:get:: /records/{RECORD_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record
   :accesscontrol: A principal in full control of the record, the admin app that created the record, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/apps/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_phas
   :accesscontrol: A principal in full control of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:delete:: /records/{RECORD_ID}/apps/{PHA_EMAIL}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: pha_record_delete
   :accesscontrol: Any admin app, or a principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_pha
   :accesscontrol: A principal in full control of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_app_document_list
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:post:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_app_document_create
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:post:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_app_document_create_or_update_ext
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:put:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_app_document_create_or_update_ext
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}/meta

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_app_document_meta_ext
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:delete:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_app_document_delete
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_app_specific_document
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/label

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_app_document_label
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/meta

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_app_document_meta
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/update

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_app_document_update
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /records/{RECORD_ID}/apps/{PHA_EMAIL}/setup

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_pha_setup
   :accesscontrol: Any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:get:: /records/{RECORD_ID}/audits/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: audit_record_view
   :accesscontrol: A principal in full control of the record, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/audits/documents/{DOCUMENT_ID}/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: audit_document_view
   :accesscontrol: A principal in full control of the record, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /records/{RECORD_ID}/audits/documents/{DOCUMENT_ID}/functions/{FUNCTION_NAME}/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: audit_function_view
   :accesscontrol: A principal in full control of the record, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter FUNCTION_NAME: The internal Indivo function name called by the API request


--------

.. http:get:: /records/{RECORD_ID}/audits/query/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: audit_query
   :accesscontrol: A principal in full control of the record, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/autoshare/bytype/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: autoshare_list
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/autoshare/bytype/all

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: autoshare_list_bytype_all
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:post:: /records/{RECORD_ID}/autoshare/carenets/{CARENET_ID}/bytype/set

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: autoshare_create
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:post:: /records/{RECORD_ID}/autoshare/carenets/{CARENET_ID}/bytype/unset

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: autoshare_delete
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /records/{RECORD_ID}/carenets/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_list
   :accesscontrol: A principal in full control of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:post:: /records/{RECORD_ID}/carenets/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_create
   :accesscontrol: A principal in full control of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:delete:: /records/{RECORD_ID}/documents/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: documents_delete
   :accesscontrol: 
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/documents/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_document_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:post:: /records/{RECORD_ID}/documents/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: document_create
   :accesscontrol: A user app with access to the record, a principal in full control of the record, or the admin app that created the record.
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:put:: /records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: document_create_by_ext_id
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:get:: /records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}/label

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_document_label_ext
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:get:: /records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}/meta

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_document_meta_ext
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:get:: /records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: read_special_document
   :accesscontrol: A user app with access to the record, a principal in full control of the record, or the admin app that created the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter SPECIAL_DOCUMENT: The type of special document to access. Options are ``demographics``, ``contact``


--------

.. http:post:: /records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: save_special_document
   :accesscontrol: A user app with access to the record, a principal in full control of the record, or the admin app that created the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter SPECIAL_DOCUMENT: The type of special document to access. Options are ``demographics``, ``contact``


--------

.. http:put:: /records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: save_special_document
   :accesscontrol: A user app with access to the record, a principal in full control of the record, or the admin app that created the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter SPECIAL_DOCUMENT: The type of special document to access. Options are ``demographics``, ``contact``


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID_0}/rels/{REL}/{DOCUMENT_ID_1}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: document_rels
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID_1: The id of the document that is the subject of the relationship, i.e. DOCUMENT_ID_1 *annotates* DOCUMENT_ID_0
   :parameter DOCUMENT_ID_0: The id of the document that is the object of the relationship, i.e. DOCUMENT_ID_0 *is annotated by* DOCUMENT_ID_1
   :parameter REL: The type of relationship between the documents, i.e. ``annotation``, ``interpretation``


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_specific_document
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: document_carenets
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:delete:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_document_delete
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: carenet_document_placement
   :accesscontrol: A principal in full control of the carenet's record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:post:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}/autoshare-revert

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: autoshare_revert
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter CARENET_ID: The id string associated with the Indivo carenet


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/label

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_document_label
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/meta

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_document_meta
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/meta

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: update_document_meta
   :accesscontrol: 
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:delete:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/nevershar

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: document_remove_nevershare
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/nevershar

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: document_set_nevershare
   :accesscontrol: A principal in full control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: get_documents_by_rel
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter REL: The type of relationship between the documents, i.e. ``annotation``, ``interpretation``


--------

.. http:post:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: document_create_by_rel
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter REL: The type of relationship between the documents, i.e. ``annotation``, ``interpretation``


--------

.. http:post:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/external/{PHA_EMAIL}/{EXTERNAL_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: document_create_by_rel_with_ext_id
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter REL: The type of relationship between the documents, i.e. ``annotation``, ``interpretation``
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/external/{PHA_EMAIL}/{EXTERNAL_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: document_create_by_rel_with_ext_id
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document
   :parameter REL: The type of relationship between the documents, i.e. ``annotation``, ``interpretation``
   :parameter PHA_EMAIL: The email identifier of the Indivo user app


--------

.. http:post:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/replace

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: document_version
   :accesscontrol: A user app with access to the record, a principal in full control of the record, or the admin app that created the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:put:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/replace/external/{PHA_EMAIL}/{EXTERNAL_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: document_version_by_ext_id
   :accesscontrol: A user app with access to the record, with an id matching the app email in the URL.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter EXTERNAL_ID: The external identifier of the desired resource
   :parameter PHA_EMAIL: The email identifier of the Indivo user app
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:post:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/set-status

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: document_set_status
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/status-history

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: document_status_history
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /records/{RECORD_ID}/documents/{DOCUMENT_ID}/versions/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: document_versions
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter DOCUMENT_ID: The unique identifier of the Indivo document


--------

.. http:get:: /records/{RECORD_ID}/inbox/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_inbox
   :accesscontrol: 
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:post:: /records/{RECORD_ID}/inbox/{MESSAGE_ID}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_send_message
   :accesscontrol: Any admin app, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter MESSAGE_ID: The unique identifier of the Indivo Message


--------

.. http:post:: /records/{RECORD_ID}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_message_attach
   :accesscontrol: Any admin app, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter ATTACHMENT_NUM: The 1-indexed number corresponding to the message attachment
   :parameter MESSAGE_ID: The unique identifier of the Indivo Message


--------

.. http:get:: /records/{RECORD_ID}/notify

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_notify
   :accesscontrol: Any admin app, or a user app with access to the record.
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/owner

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_get_owner
   :accesscontrol: A principal in full control of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:post:: /records/{RECORD_ID}/owner

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_set_owner
   :accesscontrol: Any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:put:: /records/{RECORD_ID}/owner

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_set_owner
   :accesscontrol: Any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/password_reset

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_password_reset
   :accesscontrol: 
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/reports/experimental/ccr

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: report_ccr
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/allergies/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: allergy_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/equipment/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: equipment_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/immunizations/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: immunization_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/labs/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: lab_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/measurements/{LAB_CODE}/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: measurement_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter LAB_CODE: The identifier corresponding to the measurement being made.


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/medications/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: medication_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/problems/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: problem_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/procedures/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: procedure_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/simple-clinical-notes/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: simple_clinical_notes_list
   :accesscontrol: A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/vitals/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: vitals_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/reports/minimal/vitals/{CATEGORY}/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: vitals_list
   :accesscontrol: A user app with access to the record, or a principal in full control of the record
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter CATEGORY: The category of vital sign, i.e. ``weight``, ``Blood_Pressure_Systolic``


--------

.. http:get:: /records/{RECORD_ID}/shares/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_shares
   :accesscontrol: The owner of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:post:: /records/{RECORD_ID}/shares/

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_share_add
   :accesscontrol: The owner of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record


--------

.. http:get:: /records/{RECORD_ID}/shares/{OTHER_ACCOUNT_ID}/delete

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: record_share_delete
   :accesscontrol: The owner of the record, or any admin app.
   :parameter RECORD_ID: The id string associated with the Indivo record
   :parameter OTHER_ACCOUNT_ID: The email identifier of the Indivo account to share with


--------

.. http:get:: /static/{PATH}

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: serve
   :accesscontrol: 
   :parameter PATH: The path to a static resource. Relative to the indivo_server static directory.


--------

.. http:get:: /version

   ADD A DESCRIPTION OF THE CALL HERE

   :shortname: get_version
   :accesscontrol: Any principal in Indivo.
