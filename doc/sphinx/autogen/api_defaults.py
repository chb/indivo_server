"""
Descriptions of the normal use of the given url parameters in the
Indivo API. Individual calls should customize if their definitions vary
"""

URL_PARAM_DESC = {'RECORD_ID':'The id string associated with the Indivo record',
                  'CARENET_ID':'The id string associated with the Indivo carenet',
                  'PHA_EMAIL':'The email identifier of the Indivo user app',
                  'PHA_ID':'The email identifier of the Indivo user app',
                  'DOCUMENT_ID':'The unique identifier of the Indivo document',
                  'REQUEST_TOKEN':'The oauth token string generated via the authentication dance',
                  'ACCOUNT_ID':'The email identifier of the Indivo account',
                  'ACCOUNT_EMAIL':'The email identifier of the Indivo account',
                  'PRIMARY_SECRET':'A confirmation string sent securely to the patient from Indivo',
                  'SECONDARY_SECRET':'A secondary confirmation string, accessible by the patient or an admin application',
                  'MESSAGE_ID':'The unique identifier of the Indivo Message',
                  'SHORT_NAME':'The abbreviated name of the auth system.',
                  'EXTERNAL_ID':'The external identifier of the desired resource',
                  'REL_TYPE':'The type of relationship between the documents, i.e. ``annotation``, ``interpretation``',
                  'APP_ID':'The email identifier of the Indivo user app',
                  'APP_EMAIL':'The email identifier of the Indivo user app',
                  'CATEGORY':'The category of vital sign, i.e. ``weight``, ``Blood_Pressure_Systolic``',
                  'LAB':'', 
                  'FUNCTION_NAME':'The internal Indivo function name called by the API request',
                  'REL':'The type of relationship between the documents, i.e. ``annotation``, ``interpretation``',
                  'LAB_CODE':'The identifier corresponding to the measurement being made.',
                  'OTHER_ACCOUNT_ID': 'The email identifier of the Indivo account to share with',
                  'PATH':'The path to a static resource. Relative to the indivo_server static directory.',
                  'PRINCIPAL_EMAIL':'The email with which to scope an external id.',
                  'ATTACHMENT_NUM':'The 1-indexed number corresponding to the message attachment',
                  'DOCUMENT_ID_0':'The id of the document that is the object of the relationship, i.e. DOCUMENT_ID_0 *is annotated by* DOCUMENT_ID_1',
                  'DOCUMENT_ID_1':'The id of the document that is the subject of the relationship, i.e. DOCUMENT_ID_1 *annotates* DOCUMENT_ID_0'
                  }

QUERY_PARAM_DESC = {'offset':'See :ref:`query-operators`',
                    'limit':'See :ref:`query-operators`',
                    'order_by':'See :ref:`query-operators`',
                    'group_by':'See :ref:`query-operators`',
                    'aggregate_by':'See :ref:`query-operators`',
                    'date_range':'See :ref:`query-operators`',
                    'date_group':'See :ref:`query-operators`',
                    '{FIELD}':'See :ref:`query-operators`',
                    'type':'The Indivo document type to filter by',
                    'include_archive':'0 or 1: whether or not to include archived messages in the result set.',
                    'q':'The query string to search for',
                    'fullname':'The full name of the account to search for',
                    'contact_email':'The contact email of the account to search for',
                    'status':'The account or document status to filter by',
                    }

DATA_FIELD_DESC = {
    'account_id': 'An identifier for the account. Must be a valid email address.',
    'full_name': 'The full name of the account.',
    'fullname': 'The full name of the account.',
    'contact_email': 'A valid email at which to reach the account holder.',
    'system':'The identifier of the desired authsystem. ``password`` indicates the \
             internal password system.',
    'username':'The username for this account.',
    'password':'The password for this account.',
    'message_id':'An external identifier for the message.',
    'body':'The message body. Defaults to ``[no body]``.',
    'severity': 'The importance of the message. Options are ``low``, ``medium``, ``high``. Defaults to ``low``.',
    'subject':'The message subject. Defaults to ``[no subject]``.',
    'body_type':'The formatting of the message body. Options are ``plaintext``, ``markdown``. Defaults to ``plaintext``.',
    '':'The raw content of the document to create.',
    }

TEXT_FIELD_DESC = {'description': lambda call: call.get_docstring_summary(),
                   'return_desc': 'DESCRIBE THE VALUES THAT THE CALL RETURNS',
                   'return_ex': 'GIVE AN EXAMPLE OF A RETURN VALUE',
                   }
