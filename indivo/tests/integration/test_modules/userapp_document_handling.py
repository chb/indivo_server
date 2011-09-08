import os
import data

from utils import assert_403

def test_userapp_document_handling(IndivoClient):
  PRD = 'prd'

  try:
    admin_client = IndivoClient(data.machine_app_email, data.machine_app_secret)
    record_id = admin_client.create_record(data=data.contact).response[PRD]['Record'][0]
    admin_client.set_app_id(data.app_email)
    admin_client.get_version()

    token = admin_client.setup_app(record_id=record_id, app_id=data.app_email).response[PRD]
    user_client = IndivoClient(data.app_email, 'norepinephrine')

    # Should return a 403
    assert_403(user_client.read_record(record_id=record_id))

    # set up the credentials and now this should work
    user_client.set_app_id(data.app_email)
    user_client.update_token(token)

    user_client.post_app_document(data=data.access_key)
    doc_id = user_client.post_app_document(data=data.patient_access_key).response[PRD]['Document'][0]

    user_client.read_app_document(document_id=doc_id)
    user_client.read_app_documents(parameters={'type':'PatientAccessKey'})
    user_client.read_app_documents(parameters={'type':'AccessKey'})
    user_client.read_app_document_meta(document_id=doc_id)
    user_client.read_app_document()
    user_client.post_app_document_ext(external_id='extid', data=data.doc01)

    user_client.read_app_document_ext_meta(external_id='extid')
    user_client.read_app_documents()

    #user_client.create_or_replace_app_document, document_id=doc_id, data=data.doc02)
    #user_client.post_app_document_label(data.app_email, doc_id, label)
    #user_client.remove_app_document(data.app_email, doc_id)
  except Exception, e:
    return False, e
  return True
