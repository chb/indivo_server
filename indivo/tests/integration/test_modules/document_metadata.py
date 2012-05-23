import os
import data

def test_document_metadata(IndivoClient):
  PRD = 'prd'

  try:
    admin_client = IndivoClient(data.machine_app_email, data.machine_app_secret)
    record_id = admin_client.create_record(data=data.demographics).response[PRD]['Record'][0]

    admin_client.set_app_id(data.app_email)
    admin_client.set_record_owner(data=data.account['account_id'])
    token = admin_client.setup_app(record_id=record_id, app_id=data.app_email).response[PRD]

    chrome_client = IndivoClient('chrome', 'chrome')
    chrome_client.create_session(data.account)
    chrome_client.set_app_id(data.app_email)
    chrome_client.read_record(record_id=record_id)

    # Record specific
    chrome_client.post_document(data=data.doc01)
    chrome_client.read_document_meta()

    # Record specific w/external_id
    chrome_client.post_document_ext(external_id='extid1', app_id='problems@apps.indivo.org', data=data.doc01)
    chrome_client.read_document_ext_meta(external_id='extid1', app_id='problems@apps.indivo.org')

    user_client = IndivoClient(data.app_email, data.app_secret)
    user_client.set_app_id(data.app_email)
    user_client.update_token(token)
    user_client.ds.record_id = record_id

    # Record-App specific
    user_client.post_recapp_document(data=data.doc02)
    user_client.read_recapp_document_meta()

    user_client.put_recapp_document_ext(external_id='extid', data=data.doc03)
    user_client.read_recapp_document_ext_meta(external_id='extid')

    # App specific
    user_client.post_app_document(data=data.patient_access_key)
    user_client.read_app_document_meta()

    user_client.post_app_document_ext(external_id='extid2', data=data.doc04)
    user_client.read_app_document_ext_meta(external_id='extid2')

  except Exception, e:
    return False, e
  return True
