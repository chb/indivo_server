from xml.etree import ElementTree

from utils import parse_xml, xpath, assert_403, assert_200

def test_account(IndivoClient):
  try:
    chrome_client = IndivoClient('chrome', 'chrome')

    # simplest test case
    chrome_client.create_account({'user_email' : 'ben5@indivo.org', 'contact_email':'ben5@adida.net', 'user_pass': 'foo'})
    chrome_client.add_auth_system(account_id='ben5@indivo.org', data={'system':'password', 'username':'ben5', 'password': 'test5'})
      
    # create an account
    chrome_client.create_account({'user_email' : 'ben@indivo.org', 'primary_secret_p' : '1', 'secondary_secret_p' : '1', 'contact_email':'ben@adida.net'})

    # reset it
    chrome_client.account_reset(account_id='ben@indivo.org')

    # get the account info 
    account_resp = chrome_client.account_info(account_id = 'ben@indivo.org')
    parsed_resp = ElementTree.fromstring(account_resp.response['response_data'])
    secondary_secret = parsed_resp.findtext('secret')

    # get the primary secret
    primary_secret_resp = chrome_client.account_primary_secret(account_id = 'ben@indivo.org')
    parsed_resp = ElementTree.fromstring(primary_secret_resp.response['response_data'])
    primary_secret = parsed_resp.text

    # initialize it
    chrome_client.account_initialize(account_id='ben@indivo.org', primary_secret=primary_secret, data={'secondary_secret':secondary_secret})

    # set username and password
    chrome_client.add_auth_system(account_id='ben@indivo.org', data={'system':'password', 'username':'ben', 'password': 'test'})

    # set the password to something else
    chrome_client.account_set_password(account_id='ben@indivo.org', data={'password':'test2'})      
      
    # see if we can create a session for it
    chrome_client.create_session({'username':'ben','user_pass':'test2'})

    # now the token is in the client, we can change the password
    chrome_client.account_change_password(account_id = 'ben@indivo.org', data={'old':'test2','new':'test3'})

    # change the info
    assert_200(chrome_client.account_info_set(account_id= 'ben@indivo.org', data={'contact_email':'ben2@adida.net','full_name':'Ben2 Adida'}))

    # change the username
    assert_200(chrome_client.account_username_set(account_id='ben@indivo.org', data={'username':'ben2'}))

    chrome_client = IndivoClient('chrome', 'chrome')
    chrome_client.create_session({'username':'ben2','user_pass':'test3'})

    # change the state back and forth
    chrome_client.account_set_state(account_id='ben@indivo.org', data={'state': 'disabled'})
    chrome_client.account_set_state(account_id='ben@indivo.org', data={'state': 'active'})
    chrome_client.account_set_state(account_id='ben@indivo.org', data={'state': 'retired'})
    assert_403(chrome_client.account_set_state(account_id='ben@indivo.org', data={'state': 'active'}))
    
    # do account search
    chrome_client = IndivoClient('chrome', 'chrome')
    accounts = parse_xml(chrome_client.account_search(parameters={'contact_email': 'ben@adida.net'}))
    accounts2 = parse_xml(chrome_client.account_search(parameters={'fullname': 'Steve Zabak'}))

    # create an account with a mychildrens auth system
    chrome_client.create_account({'user_email' : 'ben-chb@indivo.org', 'primary_secret_p' : '0', 'secondary_secret_p' : '0', 'contact_email':'ben-chb@adida.net'})
    chrome_client.add_auth_system(account_id='ben-chb@indivo.org', data={'system':'mychildrens', 'username':'ben-chb'})
    chrome_client.account_set_state(account_id='ben-chb@indivo.org', data={'state':'active'})
    
    # log in with the mychildrens auth system
    chrome_client.create_session({'username':'ben-chb','system':'mychildrens'})
  except Exception, e:
    return False, e
  return True
