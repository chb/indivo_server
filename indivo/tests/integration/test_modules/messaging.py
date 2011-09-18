import data

PRD = 'prd'

from utils import *

def test_messaging(IndivoClient):

  try:
    BODY    = 'body'
    SUBJECT = 'subject'
    MSG_ID  = 'message_id'
    SEVERITY = 'severity'

    admin_client = IndivoClient(data.machine_app_email, data.machine_app_secret)
    admin_client.set_app_id(data.app_email)

    account_id = admin_client.create_account(data.account03)[PRD]['Account'][0]
    admin_client.add_auth_system(account_id=account_id, data={'system':'password', 'username':data.account03['username'], 'password':data.account03['user_pass']})
    record_id = admin_client.create_record(data=data.contact).response['prd']['Record'][0]

    admin_client.set_record_owner(data=account_id)
    admin_client.setup_app(record_id=record_id, app_id=data.app_email)
    admin_client.message_record(data={SUBJECT : data.message01[SUBJECT], 
                                      BODY    : data.message01[BODY],
                                      SEVERITY: data.message01[SEVERITY]}, 
                                      message_id = data.message01[MSG_ID])
    admin_client.message_account(account_id = account_id,
                                  data= { SUBJECT : data.message02[SUBJECT], 
                                          BODY    : data.message02[BODY],
                                          MSG_ID  : data.message02[MSG_ID],
                                          SEVERITY : data.message02[SEVERITY]})

    token = admin_client.setup_app( record_id = record_id, 
                                    app_id    = data.app_email).response[PRD]

    user_client = IndivoClient(data.app_email, data.app_secret)
    user_client.update_token(token)
    user_client.set_app_id(data.app_email)
    user_client.get_messages(record_id = record_id)

    chrome_client = IndivoClient(data.chrome_consumer_key, data.chrome_consumer_secret)
    chrome_client.create_session(data.account03)


    #
    # check that archival removes one of the messages
    # 

    def num_messages():
      messages = xpath(parse_xml(chrome_client.account_inbox(account_id = data.account03['account_id'])), "/Messages/Message")
      return len(messages)
    
    num_messages_before = num_messages()
    message_id = xpath(parse_xml(chrome_client.account_inbox(account_id = data.account03['account_id'])), "/Messages/Message/@id")[0]

    chrome_client.account_message_archive(account_id = data.account03['account_id'], message_id = message_id)
    num_messages_after = num_messages()

    assert num_messages_before - num_messages_after == 1, "message didn't get archived"

  except Exception, e:
    return False, e
  return True
