import data

def test_record_pha_delete(IndivoClient):
  try:
    admin_client = IndivoClient(data.machine_app_email, data.machine_app_secret)
    admin_client.set_app_id(data.app_email)
    record_id = admin_client.create_record(data=data.contact).response['prd']['Record'][0]
    admin_client.set_record_owner(data=data.account['account_id'])
    admin_client.setup_app(record_id=record_id, app_id=data.app_email)
    admin_client.delete_record_app(record_id=record_id, app_id=data.app_email)
  except Exception, e:
    return False, e
  return True
