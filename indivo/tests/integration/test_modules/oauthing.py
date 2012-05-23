import data

def test_oauthing(IndivoClient):
  user_client = IndivoClient(data.app_email, data.app_secret)
  user_client.set_app_id(data.app_email)
  user_client.get_request_token(data='oauth_callback=oob')

  admin_client = IndivoClient(data.machine_app_email, data.machine_app_secret)
  admin_client.set_app_id(data.app_email)
  record_id = admin_client.create_record(data=data.demographics).response['prd']['Record'][0]
  admin_client.set_record_owner(data=data.account['account_id'])

  # try setting up with two setup documents, to make sure that's possible
  admin_client.setup_app(record_id=record_id, app_id=data.app_email, data="<setup>foo</setup>")
  admin_client.setup_app(record_id=record_id, app_id=data.app2_email, data="<setup>bar</setup>")
