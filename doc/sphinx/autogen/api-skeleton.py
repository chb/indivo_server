
from indivo.views import *
from codingsystems.views import *
from django.views.static import serve


CALLS=[{
"method":"POST",
    "path":"/accounts/",
    "view_func":account_create,
    "access_doc":"Any admin app.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/accounts/search",
    "view_func":account_search,
    "access_doc":"Any admin app.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}",
    "view_func":account_info,
    "access_doc":"Any admin app, or the Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/authsystems/",
    "view_func":account_authsystem_add,
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/authsystems/password/change",
    "view_func":account_password_change,
    "access_doc":"The Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/authsystems/password/set",
    "view_func":account_password_set,
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/authsystems/password/set-username",
    "view_func":account_username_set,
    "access_doc":"Any admin app, or the Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/check-secrets/{PRIMARY_SECRET}",
    "view_func":account_check_secrets,
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        'PRIMARY_SECRET':'A confirmation string sent securely to the patient from Indivo',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/forgot-password",
    "view_func":account_forgot_password,
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/inbox/",
    "view_func":account_inbox,
    "access_doc":"The Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/inbox/",
    "view_func":account_send_message,
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}",
    "view_func":account_inbox_message,
    "access_doc":"The Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        'MESSAGE_ID':'The unique identifier of the Indivo Message',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}/archive",
    "view_func":account_message_archive,
    "access_doc":"The Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        'MESSAGE_ID':'The unique identifier of the Indivo Message',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}/accept",
    "view_func":account_inbox_message_attachment_accept,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/info-set",
    "view_func":account_info_set,
    "access_doc":"Any admin app, or the Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/initialize/{PRIMARY_SECRET}",
    "view_func":account_initialize,
    "access_doc":"Any Indivo UI app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        'PRIMARY_SECRET':'A confirmation string sent securely to the patient from Indivo',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/notifications/",
    "view_func":account_notifications,
    "access_doc":"The Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/permissions/",
    "view_func":account_permissions,
    "access_doc":"The Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/primary-secret",
    "view_func":account_primary_secret,
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/records/",
    "view_func":record_list,
    "access_doc":"The Account owner.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/reset",
    "view_func":account_reset,
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/accounts/{ACCOUNT_EMAIL}/secret",
    "view_func":account_secret,
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/secret-resend",
    "view_func":account_resend_secret,
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/accounts/{ACCOUNT_EMAIL}/set-state",
    "view_func":account_set_state,
    "access_doc":"Any admin app.",
    "url_params":{
        'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/apps/",
    "view_func":all_phas,
    "access_doc":"Any principal in Indivo.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"DELETE",
    "path":"/apps/{PHA_EMAIL}",
    "view_func":pha_delete,
    "access_doc":"The user app itself.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/apps/{PHA_EMAIL}",
    "view_func":pha,
    "access_doc":"Any principal in Indivo.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/apps/{PHA_EMAIL}/documents/",
    "view_func":app_document_list,
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/apps/{PHA_EMAIL}/documents/",
    "view_func":app_document_create,
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"PUT",
    "path":"/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}",
    "view_func":app_document_create_or_update_ext,
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'EXTERNAL_ID':'The external identifier of the desired resource',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}/meta",
    "view_func":app_document_meta_ext,
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'EXTERNAL_ID':'The external identifier of the desired resource',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"DELETE",
    "path":"/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}",
    "view_func":app_document_delete,
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}",
    "view_func":app_specific_document,
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"PUT",
    "path":"/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}",
    "view_func":app_document_create_or_update,
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"PUT",
    "path":"/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/label",
    "view_func":app_document_label,
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/meta",
    "view_func":app_document_meta,
    "access_doc":"A user app with an id matching the app email in the URL.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"DELETE",
    "path":"/carenets/{CARENET_ID}",
    "view_func":carenet_delete,
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/accounts/",
    "view_func":carenet_account_list,
    "access_doc":"A principal in the carenet, in full control of the carenet's record, or any admin app.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/carenets/{CARENET_ID}/accounts/",
    "view_func":carenet_account_create,
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"DELETE",
    "path":"/carenets/{CARENET_ID}/accounts/{ACCOUNT_ID}",
    "view_func":carenet_account_delete,
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'ACCOUNT_ID':'The email identifier of the Indivo account',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/accounts/{ACCOUNT_ID}/permissions",
    "view_func":carenet_account_permissions,
    "access_doc":"A user app with access to the carenet and proxying the account, a principal in full control of the carenet's record, or any admin app.",
    "url_params":{
        'ACCOUNT_ID':'The email identifier of the Indivo account',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/apps/",
    "view_func":carenet_apps_list,
    "access_doc":"A principal in the carenet, in full control of the carenet's record, or any admin app.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"DELETE",
    "path":"/carenets/{CARENET_ID}/apps/{PHA_EMAIL}",
    "view_func":carenet_apps_delete,
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"PUT",
    "path":"/carenets/{CARENET_ID}/apps/{PHA_EMAIL}",
    "view_func":carenet_apps_create,
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/apps/{PHA_EMAIL}/permissions",
    "view_func":carenet_app_permissions,
    "access_doc":"",
    "url_params":{
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/documents/",
    "view_func":carenet_document_list,
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/documents/special/{SPECIAL_DOCUMENT}",
    "view_func":read_special_document_carenet,
    "access_doc":"A user app with access to the carenet or the entire carenet's record, an account in the carenet or in control of the record, or the admin app that created the carenet's record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        'SPECIAL_DOCUMENT':'The type of special document to access. Options are ``demographics``, ``contact``',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/documents/{DOCUMENT_ID}",
    "view_func":carenet_document,
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/documents/{DOCUMENT_ID}/meta",
    "view_func":carenet_document_meta,
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/record",
    "view_func":carenet_record,
    "access_doc":"",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/carenets/{CARENET_ID}/rename",
    "view_func":carenet_rename,
    "access_doc":"A principal in full control of the carenet's record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/allergies/",
    "view_func":carenet_allergy_list,
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/equipment/",
    "view_func":carenet_equipment_list,
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/immunizations/",
    "view_func":carenet_immunization_list,
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/measurements/{LAB_CODE}/",
    "view_func":carenet_measurement_list,
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        'LAB_CODE':'The identifier corresponding to the measurement being made.',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/medications/",
    "view_func":carenet_medication_list,
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/problems/",
    "view_func":carenet_problem_list,
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/procedures/",
    "view_func":carenet_procedure_list,
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/vitals/",
    "view_func":carenet_vitals_list,
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/carenets/{CARENET_ID}/reports/minimal/vitals/{CATEGORY}",
    "view_func":carenet_vitals_list,
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'CATEGORY':'The category of vital sign, i.e. ``weight``, ``Blood_Pressure_Systolic``',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/codes/systems/",
    "view_func":coding_systems_list,
    "access_doc":"",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/codes/systems/{SYSTEM_SHORT_NAME}/query",
    "view_func":coding_system_query,
    "access_doc":"",
    "url_params":{
        'SYSTEM_SHORT_NAME':'',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/id",
    "view_func":get_id,
    "access_doc":"",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/oauth/access_token",
    "view_func":exchange_token,
    "access_doc":"A request signed by a RequestToken.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/oauth/internal/request_tokens/{REQTOKEN_ID}/approve",
    "view_func":request_token_approve,
    "access_doc":"A principal in the carenet to which the request token is restricted (if the token is restricted), or a principal with full control over the record (if the token is not restricted).",
    "url_params":{
        'REQTOKEN_ID':'',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/oauth/internal/request_tokens/{REQTOKEN_ID}/claim",
    "view_func":request_token_claim,
    "access_doc":"Any Account.",
    "url_params":{
        'REQTOKEN_ID':'',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/oauth/internal/request_tokens/{REQTOKEN_ID}/info",
    "view_func":request_token_info,
    "access_doc":"Any Account.",
    "url_params":{
        'REQTOKEN_ID':'',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/oauth/internal/session_create",
    "view_func":session_create,
    "access_doc":"Any Indivo UI app.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/oauth/internal/surl-verify",
    "view_func":surl_verify,
    "access_doc":"Any Account.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/oauth/request_token",
    "view_func":request_token,
    "access_doc":"Any user app.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/",
    "view_func":record_create,
    "access_doc":"Any admin app.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"PUT",
    "path":"/records/external/{PRINCIPAL_EMAIL}/{EXTERNAL_ID}",
    "view_func":record_create_ext,
    "access_doc":"An admin app with an id matching the principal_email in the URL.",
    "url_params":{
        'PRINCIPAL_EMAIL':'',
        'EXTERNAL_ID':'The external identifier of the desired resource',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}",
    "view_func":record,
    "access_doc":"A principal in full control of the record, the admin app that created the record, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/apps/",
    "view_func":record_phas,
    "access_doc":"A principal in full control of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"DELETE",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}",
    "view_func":pha_record_delete,
    "access_doc":"Any admin app, or a principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}",
    "view_func":record_pha,
    "access_doc":"A principal in full control of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/",
    "view_func":record_app_document_list,
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/",
    "view_func":record_app_document_create,
    "access_doc":"A user app with access to the record, with an id matching the app email in the URL.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}",
    "view_func":record_app_document_create_or_update_ext,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"PUT",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}",
    "view_func":record_app_document_create_or_update_ext,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/external/{EXTERNAL_ID}/meta",
    "view_func":record_app_document_meta_ext,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"DELETE",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}",
    "view_func":record_app_document_delete,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}",
    "view_func":record_app_specific_document,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/label",
    "view_func":record_app_document_label,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/documents/{DOCUMENT_ID}/meta",
    "view_func":record_app_document_meta,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/apps/{PHA_EMAIL}/setup",
    "view_func":record_pha_setup,
    "access_doc":"Any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'PHA_EMAIL':'The email identifier of the Indivo user app',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/audits/",
    "view_func":audit_record_view,
    "access_doc":"A principal in full control of the record, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/audits/documents/{DOCUMENT_ID}/",
    "view_func":audit_document_view,
    "access_doc":"A principal in full control of the record, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/audits/documents/{DOCUMENT_ID}/functions/{FUNCTION_NAME}/",
    "view_func":audit_function_view,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/audits/query/",
    "view_func":audit_query,
    "access_doc":"A principal in full control of the record, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/autoshare/bytype/",
    "view_func":autoshare_list,
    "access_doc":"A principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/autoshare/bytype/all",
    "view_func":autoshare_list_bytype_all,
    "access_doc":"A principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/autoshare/carenets/{CARENET_ID}/bytype/set",
    "view_func":autoshare_create,
    "access_doc":"A principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/autoshare/carenets/{CARENET_ID}/bytype/unset",
    "view_func":autoshare_delete,
    "access_doc":"A principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'CARENET_ID':'The id string associated with the Indivo carenet',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/carenets/",
    "view_func":carenet_list,
    "access_doc":"A principal in full control of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/carenets/",
    "view_func":carenet_create,
    "access_doc":"A principal in full control of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"DELETE",
    "path":"/records/{RECORD_ID}/documents/",
    "view_func":documents_delete,
    "access_doc":"",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/documents/",
    "view_func":record_document_list,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/documents/",
    "view_func":document_create,
    "access_doc":"A user app with access to the record, a principal in full control of the record, or the admin app that created the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"PUT",
    "path":"/records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}",
    "view_func":document_create_by_ext_id,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}/label",
    "view_func":record_document_label_ext,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/documents/external/{PHA_EMAIL}/{EXTERNAL_ID}/meta",
    "view_func":record_document_meta_ext,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}",
    "view_func":read_special_document,
    "access_doc":"A user app with access to the record, a principal in full control of the record, or the admin app that created the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'SPECIAL_DOCUMENT':'The type of special document to access. Options are ``demographics``, ``contact``',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}",
    "view_func":save_special_document,
    "access_doc":"A user app with access to the record, a principal in full control of the record, or the admin app that created the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'SPECIAL_DOCUMENT':'The type of special document to access. Options are ``demographics``, ``contact``',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"PUT",
    "path":"/records/{RECORD_ID}/documents/special/{SPECIAL_DOCUMENT}",
    "view_func":save_special_document,
    "access_doc":"A user app with access to the record, a principal in full control of the record, or the admin app that created the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'SPECIAL_DOCUMENT':'The type of special document to access. Options are ``demographics``, ``contact``',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID_0}/rels/{REL}/{DOCUMENT_ID_1}",
    "view_func":document_rels,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}",
    "view_func":record_specific_document,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/",
    "view_func":document_carenets,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"DELETE",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}",
    "view_func":carenet_document_delete,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}",
    "view_func":carenet_document_placement,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/carenets/{CARENET_ID}/autoshare-revert",
    "view_func":autoshare_revert,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/label",
    "view_func":record_document_label,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/meta",
    "view_func":record_document_meta,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/meta",
    "view_func":update_document_meta,
    "access_doc":"",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"DELETE",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/nevershar",
    "view_func":document_remove_nevershare,
    "access_doc":"A principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/nevershar",
    "view_func":document_set_nevershare,
    "access_doc":"A principal in full control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/",
    "view_func":get_documents_by_rel,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/",
    "view_func":document_create_by_rel,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/external/{PHA_EMAIL}/{EXTERNAL_ID}",
    "view_func":document_create_by_rel_with_ext_id,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/rels/{REL}/external/{PHA_EMAIL}/{EXTERNAL_ID}",
    "view_func":document_create_by_rel_with_ext_id,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/replace",
    "view_func":document_version,
    "access_doc":"A user app with access to the record, a principal in full control of the record, or the admin app that created the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"PUT",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/replace/external/{PHA_EMAIL}/{EXTERNAL_ID}",
    "view_func":document_version_by_ext_id,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/set-status",
    "view_func":document_set_status,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/status-history",
    "view_func":document_status_history,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/documents/{DOCUMENT_ID}/versions/",
    "view_func":document_versions,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'DOCUMENT_ID':'The unique identifier of the Indivo document',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/inbox/",
    "view_func":record_inbox,
    "access_doc":"",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/inbox/{MESSAGE_ID}",
    "view_func":record_send_message,
    "access_doc":"Any admin app, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'MESSAGE_ID':'The unique identifier of the Indivo Message',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/inbox/{MESSAGE_ID}/attachments/{ATTACHMENT_NUM}",
    "view_func":record_message_attach,
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
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/notifications/",
    "view_func":record_notify,
    "access_doc":"Any admin app, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/notify",
    "view_func":record_notify,
    "access_doc":"Any admin app, or a user app with access to the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/owner",
    "view_func":record_get_owner,
    "access_doc":"A principal in full control of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/owner",
    "view_func":record_set_owner,
    "access_doc":"Any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"PUT",
    "path":"/records/{RECORD_ID}/owner",
    "view_func":record_set_owner,
    "access_doc":"Any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/reports/experimental/ccr",
    "view_func":report_ccr,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/allergies/",
    "view_func":allergy_list,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/equipment/",
    "view_func":equipment_list,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/immunizations/",
    "view_func":immunization_list,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/labs/",
    "view_func":lab_list,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/measurements/{LAB_CODE}/",
    "view_func":measurement_list,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'LAB_CODE':'The identifier corresponding to the measurement being made.',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/medications/",
    "view_func":medication_list,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/problems/",
    "view_func":problem_list,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/procedures/",
    "view_func":procedure_list,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/simple-clinical-notes/",
    "view_func":simple_clinical_notes_list,
    "access_doc":"A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/vitals/",
    "view_func":vitals_list,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/reports/minimal/vitals/{CATEGORY}/",
    "view_func":vitals_list,
    "access_doc":"A user app with access to the record, or a principal in full control of the record",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'CATEGORY':'The category of vital sign, i.e. ``weight``, ``Blood_Pressure_Systolic``',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/records/{RECORD_ID}/shares/",
    "view_func":record_shares,
    "access_doc":"The owner of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/shares/",
    "view_func":record_share_add,
    "access_doc":"The owner of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"DELETE",
    "path":"/records/{RECORD_ID}/shares/{OTHER_ACCOUNT_ID}",
    "view_func":record_share_delete,
    "access_doc":"The owner of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'OTHER_ACCOUNT_ID':'The email identifier of the Indivo account to share with',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"POST",
    "path":"/records/{RECORD_ID}/shares/{OTHER_ACCOUNT_ID}/delete",
    "view_func":record_share_delete,
    "access_doc":"The owner of the record, or any admin app.",
    "url_params":{
        'RECORD_ID':'The id string associated with the Indivo record',
        'OTHER_ACCOUNT_ID':'The email identifier of the Indivo account to share with',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/static/{PATH}",
    "view_func":serve,
    "access_doc":"",
    "url_params":{
        'PATH':'The path to a static resource. Relative to the indivo_server static directory.',
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

},
{
"method":"GET",
    "path":"/version",
    "view_func":get_version,
    "access_doc":"Any principal in Indivo.",
    "url_params":{
        },
    "query_opts":{
        },
    "data_fields":{
        },
    "description":"ADD A DESCRIPTION OF THE CALL HERE",

}]