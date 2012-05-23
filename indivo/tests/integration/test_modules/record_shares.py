import os
import data

def test_record_shares(IndivoClient):
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

    chrome_client.create_share(data={'account_id':'benadida@informedcohort.org'})
    chrome_client.get_shares()
    chrome_client.delete_share(account_id='benadida@informedcohort.org')
    
  except Exception, e:
    return False, e
  return True
