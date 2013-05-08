from lxml import etree

from indivo.tests.indivo_client_py.client import IndivoClient
from indivo.tests.internal_tests import IndivoLiveServerTestCase


class AccountIntegrationTests(IndivoLiveServerTestCase):
    fixtures = ['authSystems', 'machineApps']

    @classmethod
    def setUpClass(cls):
        super(AccountIntegrationTests, cls).setUpClass()

    def setUp(self):
        super(AccountIntegrationTests, self).setUp()

        server_params = {'api_base':self.live_server_url,
                         'authorization_base':'FAKE'}
        self.client = IndivoClient(server_params, self.CHROME_CONSUMER_PARAMS)

    def test_accounts(self):
        # simplest test case
        resp, content = self.client.account_create({'account_id':'ben5@indivo.org', 'contact_email':'ben5@adida.net'})
        self.assert_200(resp)

        resp, content = self.client.account_authsystem_add(account_email='ben5@indivo.org',
                                                           body={'system':'password',
                                                                 'username':'ben5',
                                                                 'password':'test5'})
        self.assert_200(resp)

        # create an account
        resp, content = self.client.account_create(body={'account_id':'ben@indivo.org',
                                                         'primary_secret_p':'1',
                                                         'secondary_secret_p':'1',
                                                         'contact_email':'ben@adida.net'})
        self.assert_200(resp)

        # reset it
        resp, content = self.client.account_reset(account_email='ben@indivo.org')
        self.assert_200(resp)

        # get the account info
        resp, content = self.client.account_info(account_email='ben@indivo.org')
        self.assert_200(resp)
        parsed_resp = etree.XML(content)
        secondary_secret = parsed_resp.findtext('secret')

        # get the primary secret
        resp, content = self.client.account_primary_secret(account_email='ben@indivo.org')
        self.assert_200(resp)

        parsed_resp = etree.XML(content)
        primary_secret = parsed_resp.text

        # initialize it
        resp, content = self.client.account_initialize(account_email='ben@indivo.org', primary_secret=primary_secret,
                                                       body={'secondary_secret':secondary_secret})
        self.assert_200(resp)

        # set username and password
        resp, content = self.client.account_authsystem_add(account_email='ben@indivo.org',
                                                           body={'system':'password',
                                                                 'username':'ben',
                                                                 'password':'test'})
        self.assert_200(resp)

        # set the password to something else
        resp, content = self.client.account_password_set(account_email='ben@indivo.org', body={'password':'test2'})
        self.assert_200(resp)

        # see if we can create a session for it
        resp, content = self.client.session_create({'username': 'ben', 'password':'test2'})
        self.assert_200(resp)
        token = self.parse_tokens(content)
        self.client.update_token(token)

        # now the token is in the client, we can change the password
        resp, content = self.client.account_password_change(account_email='ben@indivo.org',
                                                            body={'old':'test2', 'new':'test3'})
        self.assert_200(resp)

        # change the info
        resp, content = self.client.account_info_set(account_email='ben@indivo.org',
                                                     body={'contact_email':'ben2@adida.net',
                                                           'full_name':'Ben2 Adida'})
        self.assert_200(resp)

        # clear out the token on the client
        self.client.token = None
        # change the username
        resp, content = self.client.account_username_set(account_email='ben@indivo.org', body={'username':'ben2'})
        self.assert_200(resp)

        resp, content = self.client.session_create(body={'username':'ben2', 'password':'test3'})
        self.assert_200(resp)

        # change the state back and forth
        resp, content = self.client.account_set_state(account_email='ben@indivo.org', body={'state':'disabled'})
        self.assert_200(resp)
        resp, content = self.client.account_set_state(account_email='ben@indivo.org', body={'state':'active'})
        self.assert_200(resp)
        resp, content = self.client.account_set_state(account_email='ben@indivo.org', body={'state':'retired'})
        self.assert_200(resp)
        resp, content = self.client.account_set_state(account_email='ben@indivo.org', body={'state':'active'})
        self.assert_403(resp)

        # do account search
        resp, content = self.client.account_search(body={'contact_email':'ben@adida.net'})
        self.assert_200(resp)
        accounts = etree.XML(content)
        self.assertEqual(len(accounts.findall('Account')), 0)
        resp, content = self.client.account_search(body={'contact_email':'ben2@adida.net'})
        self.assert_200(resp)
        accounts = etree.XML(content)
        self.assertEqual(len(accounts.findall('Account')), 1)
        resp, content = self.client.account_search(body={'fullname':'Steve Zabak'})
        self.assert_200(resp)
        accounts = etree.XML(content)
        self.assertEqual(len(accounts.findall('Account')), 0)
        resp, content = self.client.account_search(body={'fullname':'Ben2 Adida'})
        self.assert_200(resp)
        accounts = etree.XML(content)
        self.assertEqual(len(accounts.findall('Account')), 1)
        resp, content = self.client.account_search(body={'fullname':'Ben'})
        self.assert_200(resp)
        accounts = etree.XML(content)
        self.assertEqual(len(accounts.findall('Account')), 1)

        # create an account with a test_auth_system auth system
        resp, content = self.client.account_create(
            {'account_id':'ben-chb@indivo.org', 'primary_secret_p':'0', 'secondary_secret_p':'0',
             'contact_email':'ben-chb@adida.net'})
        self.assert_200(resp)
        resp, content = self.client.account_authsystem_add(account_email='ben-chb@indivo.org',
                                                           body={'system':'test_auth_system', 'username':'ben-chb'})
        self.assert_200(resp)
        resp, content = self.client.account_set_state(account_email='ben-chb@indivo.org', body={'state':'active'})
        self.assert_200(resp)

        # log in with the test_auth_system auth system
        resp, content = self.client.session_create(body={'username':'ben-chb', 'system':'test_auth_system'})
        self.assert_200(resp)