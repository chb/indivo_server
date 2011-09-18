import data

def test_auditing(IndivoClient):
  try:
    admin_client = IndivoClient(data.machine_app_email, data.machine_app_secret)
    admin_client.set_app_id(data.app_email)
    record_id = admin_client.create_record(data=data.contact).response['prd']['Record'][0]
    admin_client.set_record_owner(data=data.account['account_id'])

    chrome_client = IndivoClient('chrome', 'chrome')
    chrome_client.create_session(data.account)
    chrome_client.read_record(record_id=record_id)

    chrome_client.post_document(data=data.doc01)
    docs = chrome_client.read_documents().response['prd']['Documents']

    # Read all documents
    for doc_id in docs:
      #Read doc_ids
      chrome_client.read_document(document=doc_id)

      # Set the app_id to data.app_email
      chrome_client.read_record_audit()
      chrome_client.read_document_audit(document_id=doc_id)
      chrome_client.read_function_audit(function_name='document')

  except Exception, e:
    return False, e
  return True, None

