import urlparse
from lxml import etree

from indivo.tests.data import TEST_DEMOGRAPHICS_XML
from indivo.tests.indivo_client_py.client import IndivoClient
from indivo.tests.internal_tests import IndivoLiveServerTestCase


class SecurityIntegrationTests(IndivoLiveServerTestCase):
    """Tests against all of our access rules"""
    fixtures = ['machineApps', 'userApps', 'accountsWithRecords', 'authSystems', 'statusNames', 'carenets']

    @classmethod
    def setUpClass(cls):
        super(SecurityIntegrationTests, cls).setUpClass()

    def setUp(self):
        """Configure a variety of accounts/records/documents/carenets/clients to be in a variety of states:

        account_1_id
            Owner of record_created_by_admin_id

        account_2_id
            Owner of record_created_by_admin_id

        record_created_by_admin_id
            Record created by an admin app

        record_created_by_chrome_id
            Record created by a chrome app

        document_1_id
            Created on record_created_by_admin_id by admin_client

        document_2_id
            Created on record_created_by_chrome_id by chrome_client

        test_carenet_1_id
            Carenet on record_created_by_chrome_id, with account_1_id and user_client_1 added in

        test_carenet_2_id
            Empty carenet on record_created_by_chrome_id

        user_client_1
            User app enabled on record_created_by_admin_id and record_created_by_chrome_id

        user_client_1_with_request_token
            User app with request token for record_created_by_admin_id

        user_client_1_with_access_token
            User app with access token for record_created_by_admin_id

        user_client_1_in_carenet_with_access_token
            User app with session on test_carenet_1_id

        user_client_2
            User app not authorized on any records

        autonomous_client
            Autonomous user app authorized on record_created_by_admin_id

        admin_client
            Admin app

        chrome_client
            Chome app

        chrome_client_with_session_account_1
            Session established through chrome client for account_1_id

        chrome_client_with_session_account_2
            Session established through chrome client for account_2_id


        """
        super(SecurityIntegrationTests, self).setUp()
        self.server_params = {'api_base':self.live_server_url, 'authorization_base':'FAKE'}
        self.admin_client = IndivoClient(self.server_params, self.ADMIN_CONSUMER_PARAMS)
        self.chrome_client = IndivoClient(self.server_params, self.CHROME_CONSUMER_PARAMS)
        self.user_client_1 = IndivoClient(self.server_params, self.USER_CONSUMER_PARAMS)
        self.user_client_2 = IndivoClient(self.server_params, self.USER_CONSUMER_PARAMS_2)
        self.autonomous_client = IndivoClient(self.server_params, self.AUTONOMOUS_CONSUMER_PARAMS)
        self.bogus_client = IndivoClient(self.server_params, {"consumer_key": "bogus_key", "consumer_secret": "bogus_secret"})
        self.admin_app_email = 'admin@apps.indivo.org'
        self.chrome_app_email = 'chrome@apps.indivo.org'
        self.user_app_email = 'testApp@apps.indivo.org'
        self.user_app_email_2 = 'testApp2@apps.indivo.org'
        self.autonomous_app_email = 'testAutonomousApp@apps.indivo.org'
        self.bogus_app_email = 'bogus@apps.indivo.org'

        self.account_1_id = 'account1@indivo.org'
        self.account_2_id = 'account2@indivo.org'

        # Create a new record with admin client
        resp, content = self.admin_client.record_create(body=TEST_DEMOGRAPHICS_XML)
        self.assert_200(resp)
        self.record_created_by_admin_id = etree.XML(content).attrib['id']

        # Create a new record with chrome client
        resp, content = self.chrome_client.record_create(body=TEST_DEMOGRAPHICS_XML)
        self.assert_200(resp)
        self.record_created_by_chrome_id = etree.XML(content).attrib['id']

        # create accounts
        resp, content = self.admin_client.account_create(body={'account_id':self.account_1_id, 'primary_secret_p':'1', 'secondary_secret_p':'1', 'contact_email':'account1@test.com'})
        self.assert_200(resp)
        resp, content = self.chrome_client.account_create(body={'account_id':self.account_2_id, 'primary_secret_p':'1', 'secondary_secret_p':'1', 'contact_email':'account2@test.com'})
        self.assert_200(resp)

        # set owners on records
        resp, content = self.admin_client.record_set_owner(record_id=self.record_created_by_admin_id, body=self.account_1_id)
        self.assert_200(resp)
        resp, content = self.chrome_client.record_set_owner(record_id=self.record_created_by_chrome_id, body=self.account_2_id)
        self.assert_200(resp)

        # setup logins for accounts
        resp, content = self.admin_client.account_authsystem_add(account_email=self.account_1_id, body={'system':'password', 'username':'account1', 'password':'test1'})
        self.assert_200(resp)
        resp, content = self.chrome_client.account_authsystem_add(account_email=self.account_2_id, body={'system':'password', 'username':'account2', 'password':'test2'})
        self.assert_200(resp)

        # add docs to records
        resp, content = self.admin_client.document_create(record_id=self.record_created_by_admin_id, body='<test>one</test>')
        self.assert_200(resp)
        self.document_1_id = etree.XML(content).attrib['id']
        resp, content = self.admin_client.document_create(record_id=self.record_created_by_admin_id, body='<test>two</test>')
        self.assert_200(resp)

        resp, content = self.chrome_client.document_create(record_id=self.record_created_by_chrome_id, body='<test>three</test>')
        self.assert_200(resp)
        self.document_2_id = etree.XML(content).attrib['id']
        resp, content = self.chrome_client.document_create(record_id=self.record_created_by_chrome_id, body='<test>four</test>')
        self.assert_200(resp)

        # create a session with a chrome client for account 1
        resp, content = self.chrome_client.session_create({'username': 'account1', 'password':'test1'})
        self.assert_200(resp)
        token = self.parse_tokens(content)
        self.chrome_client_with_session_account_1 = IndivoClient(self.server_params, self.CHROME_CONSUMER_PARAMS)
        self.chrome_client_with_session_account_1.update_token(token)

        # create a session with a chrome client for account 2
        resp, content = self.chrome_client.session_create({'username': 'account2', 'password':'test2'})
        self.assert_200(resp)
        token = self.parse_tokens(content)
        self.chrome_client_with_session_account_2 = IndivoClient(self.server_params, self.CHROME_CONSUMER_PARAMS)
        self.chrome_client_with_session_account_2.update_token(token)

        # enable client_app on self.record_created_by_admin_id
        resp, content = self.admin_client.record_pha_enable(record_id=self.record_created_by_admin_id, pha_email=self.user_app_email)
        self.assert_200(resp)

        # enable autonomous_client on self.record_created_by_admin_id
        resp, content = self.admin_client.record_pha_enable(record_id=self.record_created_by_admin_id, pha_email=self.autonomous_app_email)
        self.assert_200(resp)

        # enable client_app on self.record_created_by_chrome_id
        resp, content = self.admin_client.record_pha_enable(record_id=self.record_created_by_chrome_id, pha_email=self.user_app_email)
        self.assert_200(resp)

        # create client with access token for record created by admin app
        self.user_client_1_with_access_token = IndivoClient(self.server_params, self.USER_CONSUMER_PARAMS)
        resp, content = self.user_client_1_with_access_token.request_token(body={'indivo_record_id':self.record_created_by_admin_id, 'oauth_callback':'oob'})
        self.assert_200(resp)
        request_token_user_app_record_1 = self.parse_tokens(content)
        self.user_client_1_with_access_token.update_token(request_token_user_app_record_1)
        resp, content = self.chrome_client_with_session_account_1.request_token_approve(reqtoken_id=request_token_user_app_record_1['oauth_token'], body={'record_id':self.record_created_by_admin_id})
        token_approval = self.parse_tokens(content)
        token_approval = urlparse.urlparse(token_approval['location'])
        token_approval = self.parse_tokens(token_approval.query)
        access_token = self.user_client_1_with_access_token.exchange_token(verifier=token_approval['oauth_verifier'])

        # create client with request token for record created by admin app
        self.user_client_1_with_request_token = IndivoClient(self.server_params, self.USER_CONSUMER_PARAMS)
        resp, content = self.user_client_1_with_request_token.request_token(body={'indivo_record_id':self.record_created_by_admin_id, 'oauth_callback':'oob'})
        self.assert_200(resp)
        request_token_user_app_record_1 = self.parse_tokens(content)
        self.user_client_1_with_request_token.update_token(request_token_user_app_record_1)
        resp, content = self.chrome_client_with_session_account_1.request_token_approve(reqtoken_id=request_token_user_app_record_1['oauth_token'], body={'record_id':self.record_created_by_admin_id})
        token_approval = self.parse_tokens(content)
        token_approval = urlparse.urlparse(token_approval['location'])
        token_approval = self.parse_tokens(token_approval.query)
        self.user_client_1_with_request_token.token.set_verifier(token_approval['oauth_verifier'])

        resp, content = self.user_client_1.request_token(body={'oauth_callback':'oob'})
        self.assert_200(resp)
        request_token_user_app_no_record = self.parse_tokens(content)

        # create carenet for record created by chrome
        resp, content = self.chrome_client.carenet_create(record_id=self.record_created_by_chrome_id, body={'name':'test carenet'})
        self.assert_200(resp)
        self.test_carenet_1_id = etree.XML(content).find('Carenet').attrib['id']

        # create a second carenet that will remain empty
        resp, content = self.chrome_client.carenet_create(record_id=self.record_created_by_chrome_id, body={'name':'test carenet 2'})
        self.assert_200(resp)
        self.test_carenet_2_id = etree.XML(content).find('Carenet').attrib['id']

        # add account_1_id to the carenet
        resp, content = self.chrome_client_with_session_account_2.carenet_account_create(carenet_id=self.test_carenet_1_id, body={'write':'false', 'account_id':self.account_1_id})
        self.assert_200(resp)

        # add user app to the carenet
        resp, content = self.chrome_client_with_session_account_2.carenet_apps_create(carenet_id=self.test_carenet_1_id, pha_email=self.user_app_email)
        self.assert_200(resp)

        # create client with access token for a carenet
        self.user_client_1_in_carenet_with_access_token = IndivoClient(self.server_params, self.USER_CONSUMER_PARAMS)
        resp, content = self.user_client_1_in_carenet_with_access_token.request_token(body={'indivo_carenet_id':self.test_carenet_1_id, 'oauth_callback':'oob'})
        self.assert_200(resp)
        request_token_user_app_carenet_1 = self.parse_tokens(content)
        self.user_client_1_in_carenet_with_access_token.update_token(request_token_user_app_carenet_1)
        resp, content = self.chrome_client_with_session_account_1.request_token_approve(reqtoken_id=request_token_user_app_carenet_1['oauth_token'], body={'carenet_id':self.test_carenet_1_id})
        token_approval = self.parse_tokens(content)
        token_approval = urlparse.urlparse(token_approval['location'])
        token_approval = self.parse_tokens(token_approval.query)
        carenet_access_token = self.user_client_1_in_carenet_with_access_token.exchange_token(verifier=token_approval['oauth_verifier'])

        # get a request token for the autonomous app
        resp, content = self.autonomous_client.request_token(body={'indivo_record_id':self.record_created_by_admin_id, 'oauth_callback':'oob'})
        self.assert_200(resp)
        self.request_token_autonomous_app_record_1 = self.parse_tokens(content)

    def test_basic_access(self):
        """everyone should be able to make these calls"""
        self._basic_access(self.user_client_1)
        self._basic_access(self.user_client_1_with_request_token)
        self._basic_access(self.user_client_1_with_access_token)
        self._basic_access(self.user_client_1_in_carenet_with_access_token)
        self._basic_access(self.user_client_2)
        self._basic_access(self.autonomous_client)
        self._basic_access(self.admin_client)
        self._basic_access(self.chrome_client)
        self._basic_access(self.chrome_client_with_session_account_1)
        self._basic_access(self.chrome_client_with_session_account_2)

    def test_account_management_owner(self):
        """only admin apps and Account owners should be able to make these"""
        self._account_management_owner(self.user_client_1, self.account_1_id)
        self._account_management_owner(self.user_client_1_with_access_token, self.account_1_id)
        self._account_management_owner(self.user_client_1_in_carenet_with_access_token, self.account_2_id)
        self._account_management_owner(self.user_client_1_in_carenet_with_access_token, self.account_1_id)
        self._account_management_owner(self.user_client_2, self.account_1_id)
        self._account_management_owner(self.autonomous_client, self.account_1_id)
        self._account_management_owner(self.chrome_client_with_session_account_1, self.account_2_id)
        self._account_management_owner(self.chrome_client_with_session_account_2, self.account_1_id)

    def test_account_management_by_record(self):
        """only admin apps or principals in full control"""
        self._account_management_by_record(self.user_client_1, self.record_created_by_admin_id, self.user_app_email)
        self._account_management_by_record(self.user_client_2, self.record_created_by_admin_id, self.user_app_email_2)
        self._account_management_by_record(self.autonomous_client, self.record_created_by_admin_id, self.autonomous_app_email)

    def test_account_management_no_admin_app(self):
        """only Account principal"""
        self._account_management_no_admin_app(self.user_client_1, self.account_1_id, self.user_app_email)
        self._account_management_no_admin_app(self.user_client_1_with_access_token, self.account_1_id, self.user_app_email)
        self._account_management_no_admin_app(self.user_client_2, self.account_1_id, self.user_app_email_2)
        self._account_management_no_admin_app(self.autonomous_client, self.account_1_id, self.autonomous_app_email)
        self._account_management_no_admin_app(self.admin_client, self.account_1_id, self.admin_app_email)
        self._account_management_no_admin_app(self.chrome_client, self.account_1_id, self.chrome_app_email)
        self._account_management_no_admin_app(self.chrome_client_with_session_account_1, self.account_2_id, self.chrome_app_email)

    def test_account_management_admin_app_only(self):
        """admin apps only"""
        self._account_management_admin_app_only(self.user_client_1, self.account_1_id, self.record_created_by_admin_id)
        self._account_management_admin_app_only(self.user_client_1, self.account_1_id, self.record_created_by_chrome_id)
        self._account_management_admin_app_only(self.user_client_1, self.account_2_id, self.record_created_by_admin_id)
        self._account_management_admin_app_only(self.user_client_1, self.account_2_id, self.record_created_by_chrome_id)
        self._account_management_admin_app_only(self.user_client_2, self.account_1_id, self.record_created_by_admin_id)
        self._account_management_admin_app_only(self.autonomous_client, self.account_1_id, self.record_created_by_admin_id)
        self._account_management_admin_app_only(self.chrome_client_with_session_account_1, self.account_2_id, self.record_created_by_admin_id)

    def test_account_management_by_ext_id(self):
        """admin apps with matching app IDs"""
        self._account_management_by_ext_id(self.user_client_1, self.user_app_email)
        self._account_management_by_ext_id(self.user_client_2, self.user_app_email_2)
        self._account_management_by_ext_id(self.autonomous_client, self.autonomous_app_email)
        self._account_management_by_ext_id(self.chrome_client_with_session_account_1, self.chrome_app_email)
        self._account_management_by_ext_id(self.admin_client, self.user_app_email)  # non-matching app id
        self._account_management_by_ext_id(self.chrome_client, self.user_app_email)  # non-matching app id

    def test_chrome_app_privileges(self):
        """chrome apps only"""
        self._chrome_app_privileges(self.user_client_1, self.account_1_id)
        self._chrome_app_privileges(self.user_client_2, self.account_1_id)
        self._chrome_app_privileges(self.autonomous_client, self.account_1_id)
        self._chrome_app_privileges(self.chrome_client_with_session_account_1, self.account_1_id)
        self._chrome_app_privileges(self.admin_client, self.account_1_id)

    def test_app_privileges(self):
        """the app itself"""
        self._app_privileges(self.user_client_1, self.user_app_email_2)
        self._app_privileges(self.user_client_2, self.user_app_email)
        self._app_privileges(self.autonomous_client, self.user_app_email)
        self._app_privileges(self.chrome_client_with_session_account_1, self.user_app_email)
        self._app_privileges(self.admin_client, self.user_app_email)
        self._app_privileges(self.chrome_client, self.user_app_email)

    def test_account_for_oauth(self):
        """only Accounts"""
        # self._account_for_oauth(self.user_client_1, request_token_user_app_no_record['oauth_token'])
        self._account_for_oauth(self.user_client_2, self.request_token_autonomous_app_record_1['oauth_token'])
        self._account_for_oauth(self.autonomous_client, self.request_token_autonomous_app_record_1['oauth_token'])
        self._account_for_oauth(self.admin_client, self.request_token_autonomous_app_record_1['oauth_token'])
        self._account_for_oauth(self.chrome_client, self.request_token_autonomous_app_record_1['oauth_token'])

    def test_autonomous_app_for_oauth(self):
        """only autonomous apps"""
        self._autonomous_app_for_oauth(self.user_client_1, self.user_app_email)
        self._autonomous_app_for_oauth(self.user_client_2, self.user_app_email_2)
        self._autonomous_app_for_oauth(self.chrome_client_with_session_account_1, self.chrome_app_email)
        self._autonomous_app_for_oauth(self.admin_client, self.admin_app_email)
        self._autonomous_app_for_oauth(self.admin_client, self.autonomous_app_email)
        self._autonomous_app_for_oauth(self.chrome_client, self.chrome_app_email)

    def test_autonomous_app_on_enabled_record(self):
        """autonomous apps scoped to a record"""
        self._autonomous_app_on_enabled_record(self.user_client_1, self.record_created_by_admin_id, self.user_app_email)
        self._autonomous_app_on_enabled_record(self.user_client_2, self.record_created_by_admin_id, self.user_app_email_2)
        self._autonomous_app_on_enabled_record(self.autonomous_client, self.record_created_by_chrome_id, self.autonomous_app_email)
        self._autonomous_app_on_enabled_record(self.admin_client, self.record_created_by_admin_id, self.admin_app_email)
        self._autonomous_app_on_enabled_record(self.chrome_client, self.record_created_by_admin_id, self.chrome_app_email)
        self._autonomous_app_on_enabled_record(self.chrome_client_with_session_account_1, self.record_created_by_admin_id, self.chrome_app_email)

    def test_app_for_oauth(self):
        """any user app"""
        self._app_for_oauth(self.admin_client)
        self._app_for_oauth(self.chrome_client)
        self._app_for_oauth(self.chrome_client_with_session_account_1)

    def test_reqtoken_for_oauth(self):
        """any valid request token"""
        self._reqtoken_for_oauth(self.user_client_1)
        self._reqtoken_for_oauth(self.user_client_2)
        self._reqtoken_for_oauth(self.autonomous_client)
        self._reqtoken_for_oauth(self.admin_client)
        self._reqtoken_for_oauth(self.chrome_client)
        self._reqtoken_for_oauth(self.chrome_client_with_session_account_1)

    def test_record_limited_access(self):
        """admin app or full control"""
        self._record_limited_access(self.user_client_1, self.record_created_by_admin_id)
        self._record_limited_access(self.user_client_2, self.record_created_by_admin_id)
        self._record_limited_access(self.autonomous_client, self.record_created_by_admin_id)
        self._record_limited_access(self.chrome_client_with_session_account_1, self.record_created_by_chrome_id)  # session is not with self.record_created_by_chrome_id

    def test_record_full_admin(self):
        """admin app or record owner"""
        self._record_full_admin(self.user_client_1, self.record_created_by_admin_id, self.account_1_id)
        self._record_full_admin(self.user_client_2, self.record_created_by_admin_id, self.account_1_id)
        self._record_full_admin(self.autonomous_client, self.record_created_by_admin_id, self.account_1_id)
        self._record_full_admin(self.chrome_client_with_session_account_1, self.record_created_by_chrome_id, self.account_1_id)

    def test_record_message_access(self):
        """admin or app with access"""
        self._record_message_access(self.user_client_1, self.record_created_by_admin_id)
        self._record_message_access(self.user_client_2, self.record_created_by_admin_id)
        self._record_message_access(self.autonomous_client, self.record_created_by_admin_id)
        self._record_message_access(self.chrome_client_with_session_account_1, self.record_created_by_admin_id)
        self._record_message_access(self.chrome_client_with_session_account_1, self.record_created_by_chrome_id)

    def test_record_doc_access(self):
        """A user app with access to the record, or a principal in full control of the record"""
        self._record_doc_access(self.user_client_1, self.record_created_by_admin_id, self.document_1_id)
        self._record_doc_access(self.user_client_2, self.record_created_by_admin_id, self.document_1_id)
        self._record_doc_access(self.autonomous_client, self.record_created_by_admin_id, self.document_1_id)
        self._record_doc_access(self.admin_client, self.record_created_by_admin_id, self.document_1_id)
        self._record_doc_access(self.chrome_client, self.record_created_by_admin_id, self.document_1_id)

    def test_record_doc_access_ext(self):
        """User app with access to record, and matching id"""
        self._record_doc_access_ext(self.user_client_1, self.record_created_by_admin_id, self.user_app_email, self.document_1_id)
        self._record_doc_access_ext(self.user_client_1_with_access_token, self.record_created_by_admin_id, self.user_app_email_2, self.document_1_id)  # valid token, but wrong app id
        self._record_doc_access_ext(self.user_client_2, self.record_created_by_admin_id, self.user_app_email_2, self.document_1_id)
        self._record_doc_access_ext(self.autonomous_client, self.record_created_by_admin_id, self.autonomous_app_email, self.document_1_id)
        self._record_doc_access_ext(self.admin_client, self.record_created_by_admin_id, self.user_app_email, self.document_1_id)
        self._record_doc_access_ext(self.admin_client, self.record_created_by_admin_id, self.admin_app_email, self.document_1_id)
        self._record_doc_access_ext(self.chrome_client, self.record_created_by_admin_id, self.chrome_app_email, self.document_1_id)
        self._record_doc_access_ext(self.chrome_client_with_session_account_1, self.record_created_by_admin_id, self.chrome_app_email, self.document_1_id)

    def test_record_admin_doc_access(self):
        """A user app with access to the record, a principal in full control of the record, or the admin app that created the record"""
        self._record_admin_doc_access(self.user_client_1, self.record_created_by_admin_id, self.document_1_id)
        self._record_admin_doc_access(self.user_client_1_with_access_token, self.record_created_by_chrome_id, self.document_1_id)
        self._record_admin_doc_access(self.user_client_2, self.record_created_by_admin_id, self.document_1_id)
        self._record_admin_doc_access(self.autonomous_client, self.record_created_by_admin_id, self.document_1_id)
        self._record_admin_doc_access(self.admin_client, self.record_created_by_chrome_id, self.document_1_id)
        self._record_admin_doc_access(self.chrome_client, self.record_created_by_admin_id, self.document_1_id)
        self._record_admin_doc_access(self.chrome_client_with_session_account_1, self.record_created_by_chrome_id, self.document_1_id)

    def test_record_special_doc_access(self):
        """A user app with access to the record, a principal in full control of the record, or any admin app"""
        self._record_special_doc_access(self.user_client_1, self.record_created_by_admin_id)
        self._record_special_doc_access(self.user_client_1_with_access_token, self.record_created_by_chrome_id)
        self._record_special_doc_access(self.user_client_2, self.record_created_by_admin_id)
        self._record_special_doc_access(self.autonomous_client, self.record_created_by_admin_id)
        self._record_special_doc_access(self.chrome_client_with_session_account_1, self.record_created_by_chrome_id)

    def test_record_doc_sharing_access(self):
        """A principal in full control of the record"""
        self._record_doc_sharing_access(self.user_client_1, self.record_created_by_admin_id, self.document_1_id)
        self._record_doc_sharing_access(self.user_client_1_with_access_token, self.record_created_by_admin_id, self.document_1_id)
        self._record_doc_sharing_access(self.user_client_2, self.record_created_by_admin_id, self.document_1_id)
        self._record_doc_sharing_access(self.autonomous_client, self.record_created_by_admin_id, self.document_1_id)
        self._record_doc_sharing_access(self.admin_client, self.record_created_by_admin_id, self.document_1_id)
        self._record_doc_sharing_access(self.chrome_client, self.record_created_by_admin_id, self.document_1_id)
        self._record_doc_sharing_access(self.chrome_client_with_session_account_1, self.record_created_by_chrome_id, self.document_1_id)

    def test_record_app_doc_access(self):
        """A user app with access to the record, with an id matching the app email in the URL"""
        self._record_app_doc_access(self.user_client_1, self.record_created_by_admin_id, self.user_app_email_2, self.document_1_id)
        self._record_app_doc_access(self.user_client_1, self.record_created_by_chrome_id, self.user_app_email_2, self.document_1_id)
        self._record_app_doc_access(self.user_client_1_with_access_token, self.record_created_by_chrome_id, self.user_app_email, self.document_1_id)
        self._record_app_doc_access(self.user_client_2, self.record_created_by_admin_id, self.user_app_email, self.document_1_id)
        self._record_app_doc_access(self.autonomous_client, self.record_created_by_admin_id, self.user_app_email, self.document_1_id)
        self._record_app_doc_access(self.admin_client, self.record_created_by_admin_id, self.user_app_email, self.document_1_id)
        self._record_app_doc_access(self.chrome_client, self.record_created_by_chrome_id, self.user_app_email, self.document_1_id)
        self._record_app_doc_access(self.chrome_client_with_session_account_1, self.record_created_by_admin_id, self.user_app_email, self.document_1_id)

    def test_app_doc_access(self):
        """A user app with an id matching the app email in the URL"""
        self._app_doc_access(self.user_client_1, self.user_app_email_2, self.document_1_id)
        self._app_doc_access(self.user_client_1_with_access_token, self.user_app_email, self.document_1_id)
        self._app_doc_access(self.user_client_2, self.user_app_email, self.document_1_id)
        self._app_doc_access(self.autonomous_client, self.user_app_email, self.document_1_id)
        self._app_doc_access(self.admin_client, self.user_app_email, self.document_1_id)
        self._app_doc_access(self.chrome_client, self.user_app_email, self.document_1_id)
        self._app_doc_access(self.chrome_client_with_session_account_1, self.user_app_email, self.document_1_id)

    def test_audit_access(self):
        """A principal in full control of the record, or a user app with access to the record"""
        self._audit_access(self.user_client_1, self.record_created_by_admin_id, self.document_1_id)
        self._audit_access(self.user_client_1, self.record_created_by_chrome_id, self.document_1_id)
        self._audit_access(self.user_client_1_with_access_token, self.record_created_by_chrome_id, self.document_1_id)
        self._audit_access(self.user_client_2, self.record_created_by_admin_id, self.document_1_id)
        self._audit_access(self.autonomous_client, self.record_created_by_admin_id, self.document_1_id)
        self._audit_access(self.admin_client, self.record_created_by_admin_id, self.document_1_id)
        self._audit_access(self.chrome_client, self.record_created_by_admin_id, self.document_1_id)
        self._audit_access(self.chrome_client_with_session_account_1, self.record_created_by_chrome_id, self.document_1_id)

    def test_autoshare_permissions(self):
        """A principal in full control of the record"""
        self._autoshare_permissions(self.user_client_1, self.record_created_by_admin_id, self.test_carenet_1_id, self.document_1_id)
        self._autoshare_permissions(self.user_client_1_with_access_token, self.record_created_by_admin_id, self.test_carenet_1_id, self.document_1_id)
        self._autoshare_permissions(self.user_client_2, self.record_created_by_admin_id, self.test_carenet_1_id, self.document_1_id)
        self._autoshare_permissions(self.autonomous_client, self.record_created_by_admin_id, self.test_carenet_1_id, self.document_1_id)
        self._autoshare_permissions(self.admin_client, self.record_created_by_admin_id, self.test_carenet_1_id, self.document_1_id)
        self._autoshare_permissions(self.chrome_client, self.record_created_by_admin_id, self.test_carenet_1_id, self.document_1_id)
        self._autoshare_permissions(self.chrome_client_with_session_account_1, self.record_created_by_chrome_id, self.test_carenet_1_id, self.document_1_id)

    def test_token_approval_admin(self):
        """A principal in the carenet to which the request token is restricted (if the token is restricted), or a principal with full control over the record (if the token is not restricted)"""
        # we use a request token that has not been claimed or exchanged yet
        self._token_approval_admin(self.user_client_1, self.request_token_autonomous_app_record_1['oauth_token'])
        self._token_approval_admin(self.user_client_1_with_access_token, self.request_token_autonomous_app_record_1['oauth_token'])
        self._token_approval_admin(self.user_client_2, self.request_token_autonomous_app_record_1['oauth_token'])
        self._token_approval_admin(self.autonomous_client, self.request_token_autonomous_app_record_1['oauth_token'])
        self._token_approval_admin(self.admin_client, self.request_token_autonomous_app_record_1['oauth_token'])
        self._token_approval_admin(self.chrome_client, self.request_token_autonomous_app_record_1['oauth_token'])
        self._token_approval_admin(self.chrome_client_with_session_account_1, self.request_token_autonomous_app_record_1['oauth_token'])

    def test_carenet_read_access(self):
        """A principal in the carenet, in full control of the carenet's record, or any admin app."""
        # self._carenet_read_access(self.user_client_1, self.test_carenet_1_id) TODO: should this really give a 200?
        # self._carenet_read_access(self.user_client_1_with_access_token, self.test_carenet_1_id)
        self._carenet_read_access(self.user_client_2, self.test_carenet_1_id)
        self._carenet_read_access(self.autonomous_client, self.test_carenet_1_id)

    def test_carenet_control(self):
        """A principal in full control of the carenet's record."""
        self._carenet_control(self.user_client_1, self.test_carenet_1_id, self.account_1_id, self.user_app_email, self.document_1_id, self.record_created_by_admin_id)
        self._carenet_control(self.user_client_1_with_access_token, self.test_carenet_1_id, self.account_1_id, self.user_app_email, self.document_1_id, self.record_created_by_admin_id)
        self._carenet_control(self.user_client_1_in_carenet_with_access_token, self.test_carenet_1_id, self.account_1_id, self.user_app_email, self.document_1_id, self.record_created_by_admin_id)
        self._carenet_control(self.user_client_2, self.test_carenet_1_id, self.account_1_id, self.user_app_email, self.document_1_id, self.record_created_by_admin_id)
        self._carenet_control(self.autonomous_client, self.test_carenet_1_id, self.account_1_id, self.user_app_email, self.document_1_id, self.record_created_by_admin_id)
        self._carenet_control(self.admin_client, self.test_carenet_1_id, self.account_1_id, self.user_app_email, self.document_1_id, self.record_created_by_admin_id)
        self._carenet_control(self.chrome_client, self.test_carenet_1_id, self.account_1_id, self.user_app_email, self.document_1_id, self.record_created_by_admin_id)
        self._carenet_control(self.chrome_client_with_session_account_1, self.test_carenet_1_id, self.account_1_id, self.user_app_email, self.document_1_id, self.record_created_by_admin_id)

    def test_record_access(self):
        """A principal in full control of the record, any admin app, or a user app with access to the record"""
        self._record_access(self.user_client_1, self.record_created_by_admin_id)
        self._record_access(self.user_client_1_with_access_token, self.record_created_by_chrome_id)
        self._record_access(self.user_client_1_in_carenet_with_access_token, self.record_created_by_chrome_id)
        self._record_access(self.user_client_1_in_carenet_with_access_token, self.record_created_by_admin_id)
        self._record_access(self.user_client_2, self.record_created_by_admin_id)
        self._record_access(self.user_client_2, self.record_created_by_chrome_id)
        self._record_access(self.autonomous_client, self.record_created_by_admin_id)
        self._record_access(self.autonomous_client, self.record_created_by_chrome_id)
        self._record_access(self.chrome_client_with_session_account_1, self.record_created_by_chrome_id)
        self._record_access(self.chrome_client_with_session_account_2, self.record_created_by_admin_id)

    def test_carenet_read_all_access(self):
        """A user app with access to the carenet and proxying the account, a principal in full control of the carenet's record, or any admin app"""
        self._carenet_read_all_access(self.user_client_1, self.test_carenet_1_id, self.account_1_id)
        self._carenet_read_all_access(self.user_client_1, self.test_carenet_1_id, self.account_2_id)
        self._carenet_read_all_access(self.user_client_1_with_access_token, self.test_carenet_1_id, self.account_1_id)
        self._carenet_read_all_access(self.user_client_1_with_access_token, self.test_carenet_1_id, self.account_2_id)
        # self._carenet_read_all_access(self.user_client_1_in_carenet_with_access_token, self.test_carenet_1_id, self.account_1_id)
        self._carenet_read_all_access(self.user_client_1_in_carenet_with_access_token, self.test_carenet_1_id, self.account_2_id)
        self._carenet_read_all_access(self.user_client_2, self.test_carenet_1_id, self.account_1_id)
        self._carenet_read_all_access(self.user_client_2, self.test_carenet_1_id, self.account_2_id)
        self._carenet_read_all_access(self.autonomous_client, self.test_carenet_1_id, self.account_1_id)
        self._carenet_read_all_access(self.autonomous_client, self.test_carenet_1_id, self.account_2_id)
        # self._carenet_read_all_access(self.admin_client, self.test_carenet_1_id, self.account_1_id)
        # self._carenet_read_all_access(self.chrome_client, self.test_carenet_1_id, self.account_1_id)
        # self._carenet_read_all_access(self.chrome_client_with_session_account_1, self.test_carenet_1_id, self.account_1_id)
        self._carenet_read_all_access(self.chrome_client_with_session_account_1, self.test_carenet_1_id, self.account_2_id)
        # self._carenet_read_all_access(self.chrome_client_with_session_account_2, self.test_carenet_1_id, self.account_1_id)
        # self._carenet_read_all_access(self.chrome_client_with_session_account_2, self.test_carenet_1_id, self.account_2_id)

    def test_carenet_doc_access(self):
        """A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record"""
        self._carenet_doc_access(self.user_client_1, self.test_carenet_1_id, self.document_1_id)
        self._carenet_doc_access(self.user_client_1_with_access_token, self.test_carenet_1_id, self.document_1_id)
        # self._carenet_doc_access(self.user_client_1_in_carenet_with_access_token, self.test_carenet_1_id, self.document_1_id)
        self._carenet_doc_access(self.user_client_2, self.test_carenet_1_id, self.document_1_id)
        self._carenet_doc_access(self.autonomous_client, self.test_carenet_1_id, self.document_1_id)
        self._carenet_doc_access(self.admin_client, self.test_carenet_1_id, self.document_1_id)
        self._carenet_doc_access(self.chrome_client, self.test_carenet_1_id, self.document_1_id)
        # self._carenet_doc_access(self.chrome_client_with_session_account_1, self.test_carenet_1_id, self.document_1_id)
        self._carenet_doc_access(self.chrome_client_with_session_account_1, self.test_carenet_2_id, self.document_1_id)
        # self._carenet_doc_access(self.chrome_client_with_session_account_2, self.test_carenet_1_id, self.document_1_id)

    def test_carenet_special_doc_access(self):
        """A user app with access to the carenet or the entire carenet's record, an account in the carenet or in control of the record, or any admin app"""
        self._carenet_special_doc_access(self.user_client_1, self.test_carenet_1_id)
        self._carenet_special_doc_access(self.user_client_1, self.test_carenet_2_id)
        self._carenet_special_doc_access(self.user_client_1_with_access_token, self.test_carenet_1_id)
        # self._carenet_special_doc_access(self.user_client_1_in_carenet_with_access_token, self.test_carenet_1_id)
        self._carenet_special_doc_access(self.user_client_1_in_carenet_with_access_token, self.test_carenet_2_id)
        self._carenet_special_doc_access(self.user_client_2, self.test_carenet_1_id)
        self._carenet_special_doc_access(self.autonomous_client, self.test_carenet_1_id)
        # self._carenet_special_doc_access(self.admin_client, self.test_carenet_1_id)
        # self._carenet_special_doc_access(self.chrome_client, self.test_carenet_1_id)
        # self._carenet_special_doc_access(self.chrome_client_with_session_account_1, self.test_carenet_1_id)
        self._carenet_special_doc_access(self.chrome_client_with_session_account_1, self.test_carenet_2_id)
        # self._carenet_special_doc_access(self.chrome_client_with_session_account_2, self.test_carenet_1_id)

    def _basic_access(self, client):
        """Any principal in Indivo."""
        resp, content = client.get_version()
        self.assert_200(resp)

        resp, content = client.all_phas()
        self.assert_200(resp)

        resp, content = client.all_manifests()
        self.assert_200(resp)

        resp, content = client.pha(pha_email=self.user_app_email)
        self.assert_200(resp)

        resp, content = client.app_manifest(pha_email=self.user_app_email)
        self.assert_200(resp)

        resp, content = client.smart_ontology()
        self.assert_200(resp)

        resp, content = client.smart_manifest()
        self.assert_200(resp)

    def _account_management_owner(self, client, account_id):
        """Any admin app, or the Account owner."""
        resp, content = client.account_info(account_email=account_id)
        self.assert_403(resp)

        resp, content = client.account_info_set(account_email=account_id, body={'contact_email':'junk@indivo.org'})
        self.assert_403(resp)

        resp, content = client.account_username_set(account_email=account_id, body={'username':'junk'})
        self.assert_403(resp)

        resp, content = client.record_list(account_email=account_id)
        self.assert_403(resp)

    def _account_management_by_record(self, client, record_id, app_id):
        """Any admin app, or a principal in full control of the record."""
        resp, content = client.pha_record_delete(record_id=record_id, pha_email=app_id)
        self.assert_403(resp)

        resp, content = client.record_pha_enable(record_id=record_id, pha_email=app_id)
        self.assert_403(resp)

    def _account_management_no_admin_app(self, client, account_id, app_id):
        """The Account owner."""
        resp, content = client.account_password_change(account_email=account_id, body={'new':'newpwd', 'old':'oldpwd'})
        self.assert_403(resp)

        resp, content = client.account_inbox(account_email=account_id)
        self.assert_403(resp)

        resp, content = client.account_inbox_message(account_email=account_id, message_id='fake')
        self.assert_403(resp)

        resp, content = client.account_inbox_message_attachment_accept(account_email=account_id, message_id='fake', attachment_num='1')
        self.assert_403(resp)

        resp, content = client.account_message_archive(account_email=account_id, message_id='fake')
        self.assert_403(resp)

        resp, content = client.account_notifications(account_email=account_id)
        self.assert_403(resp)

        resp, content = client.account_permissions(account_email=account_id)
        self.assert_403(resp)

        resp, content = client.get_connect_credentials(account_email=account_id, pha_email=app_id)
        self.assert_403_or_404(resp)

        resp, content = client.get_user_preferences(account_email=account_id, pha_email=app_id)
        self.assert_403_or_404(resp)

        resp, content = client.set_user_preferences(account_email=account_id, pha_email=app_id)
        self.assert_403_or_404(resp)

        resp, content = client.delete_user_preferences(account_email=account_id, pha_email=app_id)
        self.assert_403_or_404(resp)

    def _account_management_admin_app_only(self, client, account_id, record_id):
        """Any admin app."""
        resp, content = client.account_create(body={'account_id':'junk@indivo.org'})
        self.assert_403(resp)

        resp, content = client.account_search(body={'fullname':'junk', 'contact_email':'junk@indivo.org'})
        self.assert_403(resp)

        resp, content = client.record_search(body={'label':'junk'})
        self.assert_403(resp)

        resp, content = client.account_forgot_password(account_email=account_id)
        self.assert_403(resp)

        resp, content = client.account_authsystem_add(account_email=account_id, body={'system':'password', 'username':'test', 'password':'test_password'})
        self.assert_403(resp)

        resp, content = client.account_check_secrets(account_email=account_id, primary_secret='junk')
        self.assert_403(resp)

        resp, content = client.account_resend_secret(account_email=account_id)
        self.assert_403(resp)

        resp, content = client.account_set_state(account_email=account_id, body={'state':'disabled'})
        self.assert_403(resp)

        resp, content = client.account_password_set(account_email=account_id, body={'password':'junk'})
        self.assert_403(resp)

        resp, content = client.record_create(body=TEST_DEMOGRAPHICS_XML)
        self.assert_403(resp)

        resp, content = client.record_set_owner(record_id=record_id, body='junk@indivo.org')
        self.assert_403(resp)

        resp, content = client.record_pha_setup(record_id=record_id, pha_email=self.user_app_email)
        self.assert_403(resp)

        resp, content = client.account_secret(account_email=account_id)
        self.assert_403(resp)

        resp, content = client.account_send_message(account_email=account_id, body={'body': 'test body', 'subject': 'test subject'})
        self.assert_403(resp)

    def _account_management_by_ext_id(self, client, app_id):
        """An admin app with an id matching the principal_email in the URL."""
        resp, content = client.record_create_ext(principal_email=app_id, external_id='ext1', body=TEST_DEMOGRAPHICS_XML)
        self.assert_403(resp)

    def _chrome_app_privileges(self, client, account_id):
        """Any Indivo UI app."""
        resp, content = client.session_create({'username': 'account1', 'password':'test1'})
        self.assert_403(resp)

        resp, content = client.account_initialize(account_email=account_id, primary_secret='fake')
        self.assert_403(resp)

    def _app_privileges(self, client, app_id):
        """The user app itself."""
        resp, content = client.pha_delete(pha_email=app_id)
        self.assert_403(resp)

    def _account_for_oauth(self, client, token_id):
        """Any Account."""
        resp, content = client.request_token_claim(reqtoken_id=token_id)
        self.assert_403(resp)

        resp, content = client.request_token_info(reqtoken_id=token_id)
        self.assert_403(resp)

        resp, content = client.surl_verify(body={'surl_sig':'junk', 'surl_timestamp':'junk', 'surl_token':'junk'})
        self.assert_403(resp)

    def _autonomous_app_for_oauth(self, client, app_id):
        """Any autonomous user app."""
        resp, content = client.app_record_list(pha_email=app_id)
        self.assert_403_or_404(resp)

    def _autonomous_app_on_enabled_record(self, client, record_id, app_id):
        """An autonomous user app with a record on which the app is authorized to run."""
        resp, content = client.autonomous_access_token(record_id=record_id, pha_email=app_id)
        self.assert_403_or_404(resp)

    def _app_for_oauth(self, client):
        """Any user app."""
        resp, content = client.request_token(body={'oauth_callback':'oob'})
        self.assert_403(resp)

    # TODO: client has two implementations of this, one which handles verifier and token
    def _reqtoken_for_oauth(self, client):
        """A request signed by a RequestToken."""
        resp, content = client.post('/oauth/access_token')
        self.assert_403(resp)

    def _token_approval_admin(self, client, reqtoken_id):
        """A principal in the carenet to which the request token is restricted (if the token is restricted), or a principal with full control over the record (if the token is not restricted)."""
        resp, content = client.request_token_approve(reqtoken_id=reqtoken_id)
        self.assert_403(resp)

    def _carenet_read_access(self, client, carenet_id):
        """A principal in the carenet, in full control of the carenet's record, or any admin app."""
        resp, content = client.carenet_account_list(carenet_id=carenet_id)
        self.assert_403(resp)

        resp, content = client.carenet_apps_list(carenet_id=carenet_id)
        self.assert_403(resp)

        resp, content = client.carenet_record(carenet_id=carenet_id)
        self.assert_403(resp)

    def _carenet_control(self, client, carenet_id, account_id, app_id, document_id, record_id):
        """A principal in full control of the carenet's record."""
        resp, content = client.carenet_delete(carenet_id=carenet_id)
        self.assert_403(resp)

        resp, content = client.carenet_rename(carenet_id=carenet_id, body={'name':'newname'})
        self.assert_403(resp)

        resp, content = client.carenet_account_create(carenet_id=carenet_id, body={'write':'false', 'account_id':account_id})
        self.assert_403(resp)

        resp, content = client.carenet_account_delete(carenet_id=carenet_id, account_id=account_id)
        self.assert_403(resp)

        resp, content = client.carenet_apps_create(carenet_id=carenet_id, pha_email=app_id)
        self.assert_403(resp)

        resp, content = client.carenet_apps_delete(carenet_id=carenet_id, pha_email=app_id)
        self.assert_403(resp)

        resp, content = client.carenet_document_placement(carenet_id=carenet_id, record_id=record_id, document_id=document_id)
        self.assert_403(resp)

        resp, content = client.carenet_document_delete(carenet_id=carenet_id, record_id=record_id, document_id=document_id)
        self.assert_403(resp)

    def _carenet_read_all_access(self, client, carenet_id, account_id):
        """A user app with access to the carenet and proxying the account, a principal in full control of the carenet's record, or any admin app."""

        resp, content = client.carenet_account_permissions(carenet_id=carenet_id, account_id=account_id)
        self.assert_403(resp)

    def _record_limited_access(self, client, record_id):
        """A principal in full control of the record, or any admin app."""
        resp, content = client.record_phas(record_id=record_id)
        self.assert_403(resp)

        resp, content = client.record_pha(record_id=record_id, pha_email=self.user_app_email)
        self.assert_403(resp)

        resp, content = client.record_get_owner(record_id=record_id)
        self.assert_403(resp)

        resp, content = client.carenet_list(record_id=record_id)
        self.assert_403(resp)

        resp, content = client.carenet_create(record_id=record_id, body={'name':'junkcarenet'})
        self.assert_403(resp)

    def _record_access(self, client, record_id):
        """A principal in full control of the record, any admin app, or a user app with access to the record."""
        resp, content = client.record(record_id=record_id)
        self.assert_403(resp)

    def _record_full_admin(self, client, record_id, account_id):
        """The owner of the record, or any admin app."""
        resp, content = client.record_shares(record_id=record_id)
        self.assert_403(resp)

        resp, content = client.record_share_add(record_id=record_id, body={'account_id':account_id})
        self.assert_403(resp)

        resp, content = client.record_share_delete(record_id=record_id, other_account_id=account_id)
        self.assert_403(resp)

    def _record_message_access(self, client, record_id):
        """Any admin app, or a user app with access to the record."""
        resp, content = client.record_notify(record_id=record_id, body={'content':'testing record notify'})
        self.assert_403(resp)

        resp, content = client.record_send_message(record_id=record_id, message_id='message1', body={'body':'test body', 'subject':'test subject'})
        self.assert_403(resp)

        resp, content = client.record_message_attach(record_id=record_id, attachment_num='1', message_id='message1', body="<junk>stuff</junk>")
        self.assert_403(resp)

    def _carenet_doc_access(self, client, carenet_id, document_id):
        """A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record."""
        resp, content = client.carenet_generic_list(carenet_id=carenet_id, data_model='Problem')
        self.assert_403(resp)

        resp, content = client.carenet_document_list(carenet_id=carenet_id)
        self.assert_403(resp)

        resp, content = client.carenet_document(carenet_id=carenet_id, document_id=document_id)
        self.assert_403(resp)

        resp, content = client.carenet_document_meta(carenet_id=carenet_id, document_id=document_id)
        self.assert_403(resp)

    def _carenet_special_doc_access(self, client, carenet_id):
        """A user app with access to the carenet or the entire carenet's record, an account in the carenet or in control of the record, or any admin app."""
        resp, content = client.read_demographics_carenet(carenet_id=carenet_id)
        self.assert_403(resp)

    def _record_doc_access(self, client, record_id, document_id):
        """A user app with access to the record, or a principal in full control of the record"""
        resp, content = client.smart_allergies(record_id=record_id)
        self.assert_403(resp)

        resp, content = client.smart_allergies_instance(record_id=record_id, model_id='junk')
        self.assert_403(resp)

        resp, content = client.smart_generic(record_id=record_id, model_name='Problem')
        self.assert_403(resp)

        resp, content = client.smart_generic_instance(record_id=record_id, model_name='Problem', model_id='junk')
        self.assert_403(resp)

        resp, content = client.generic_list(record_id=record_id, data_model='Problem')
        self.assert_403(resp)

        resp, content = client.report_ccr(record_id=record_id)
        self.assert_403(resp)

        resp, content = client.record_document_list(record_id=record_id)
        self.assert_403(resp)

        resp, content = client.record_document_meta(record_id=record_id, document_id=document_id)
        self.assert_403(resp)

        resp, content = client.record_document(record_id=record_id, document_id=document_id)
        self.assert_403(resp)

        resp, content = client.record_document_label(record_id=record_id, document_id=document_id, body='test label')
        self.assert_403(resp)

        resp, content = client.document_versions(record_id=record_id, document_id=document_id)
        self.assert_403(resp)

        resp, content = client.document_create_by_rel(record_id=record_id, rel='annotation', document_id=document_id, body='<test>junk</test>')
        self.assert_403(resp)

        resp, content = client.get_documents_by_rel(record_id=record_id, rel='annotation', document_id=document_id)
        self.assert_403(resp)

        resp, content = client.document_set_status(record_id=record_id, document_id=document_id, body='void')
        self.assert_403(resp)

        resp, content = client.document_status_history(record_id=record_id, document_id=document_id)
        self.assert_403(resp)

        resp, content = client.document_rels(record_id=record_id, document_id_1=document_id, document_id_0=document_id, rel='annotation')
        self.assert_403(resp)

        resp, content = client.document_carenets(record_id=record_id, document_id=document_id)
        self.assert_403(resp)

    def _record_doc_access_ext(self, client, record_id, app_id, document_id):
        """A user app with access to the record, with an id matching the app email in the URL."""
        resp, content = client.document_create_by_ext_id(record_id=record_id, external_id='external1', pha_email=app_id, body='<test>junk</test>')
        self.assert_403_or_404(resp)

        resp, content = client.document_create_by_rel_with_ext_id(record_id=record_id, rel='annotation', external_id='external1', pha_email=app_id, document_id=document_id)
        self.assert_403_or_404(resp)

        resp, content = client.document_version_by_ext_id(record_id=record_id, external_id='external1', pha_email=app_id, document_id=document_id, body='<test>junk</test>')
        self.assert_403_or_404(resp)

        resp, content = client.record_document_label_ext(record_id=record_id, external_id='external1', pha_email=app_id, body='test label')
        self.assert_403_or_404(resp)

        resp, content = client.record_document_meta_ext(record_id=record_id, external_id='external1', pha_email=app_id)
        self.assert_403_or_404(resp)

        resp, content = client.record_document_ext(record_id=record_id, external_id='external1', pha_email=app_id)
        self.assert_403_or_404(resp)

    def _record_admin_doc_access(self, client, record_id, document_id):
        """A user app with access to the record, a principal in full control of the record, or the admin app that created the record."""
        resp, content = client.document_create(record_id=record_id, body='<test>junk</test>')
        self.assert_403(resp)

        resp, content = client.document_version(record_id=record_id, document_id=document_id, body='<test>junk</test>')
        self.assert_403(resp)

    def _record_special_doc_access(self, client, record_id):
        """A user app with access to the record, a principal in full control of the record, or any admin app."""
        resp, content = client.read_demographics(record_id=record_id)
        self.assert_403(resp)

        resp, content = client.set_demographics(record_id=record_id, body='junk')
        self.assert_403(resp)

    def _record_doc_sharing_access(self, client, record_id, document_id):
        """A principal in full control of the record."""
        resp, content = client.document_set_nevershare(record_id=record_id, document_id=document_id)
        self.assert_403(resp)

        resp, content = client.document_remove_nevershare(record_id=record_id, document_id=document_id)
        self.assert_403(resp)

    def _record_app_doc_access(self, client, record_id, app_id, document_id):
        """A user app with access to the record, with an id matching the app email in the URL."""
        resp, content = client.record_app_document_meta(record_id=record_id, document_id=document_id, pha_email=app_id)
        self.assert_403_or_404(resp)

        resp, content = client.record_app_document_meta_ext(record_id=record_id, external_id='external1', pha_email=app_id)
        self.assert_403_or_404(resp)

        resp, content = client.record_app_document_list(record_id=record_id, pha_email=app_id)
        self.assert_403_or_404(resp)

        resp, content = client.record_app_document(record_id=record_id, pha_email=app_id, document_id=document_id)
        self.assert_403_or_404(resp)

        resp, content = client.record_app_document_ext(record_id=record_id, external_id='external1', pha_email=app_id)
        self.assert_403_or_404(resp)

        resp, content = client.record_app_document_create(record_id=record_id, external_id='external1', pha_email=app_id, body='<test>junk</test>')
        self.assert_403_or_404(resp)

        resp, content = client.record_app_document_create_or_update_ext(record_id=record_id, external_id='external1', pha_email=app_id, body='<test>junk</test>')
        self.assert_403_or_404(resp)

        resp, content = client.record_app_document_label(record_id=record_id, pha_email=app_id, document_id=document_id)
        self.assert_403_or_404(resp)

        resp, content = client.record_app_document_delete(record_id=record_id, pha_email=app_id, document_id=document_id)
        self.assert_403_or_404(resp)

    def _app_doc_access(self, client, app_id, document_id):
        """A user app with an id matching the app email in the URL."""
        resp, content = client.app_document_meta(pha_email=app_id, document_id=document_id)
        self.assert_403(resp)

        resp, content = client.app_document_meta_ext(pha_email=app_id, external_id='external1')
        self.assert_403(resp)

        resp, content = client.app_document_list(pha_email=app_id)
        self.assert_403(resp)

        resp, content = client.app_document(pha_email=app_id, document_id=document_id)
        self.assert_403(resp)

        resp, content = client.app_document_ext(pha_email=app_id, external_id='external1')
        self.assert_403(resp)

        resp, content = client.app_document_create(pha_email=app_id, body='<test>junk</test>')
        self.assert_403(resp)

        resp, content = client.app_document_create_or_update(pha_email=app_id, document_id=document_id, body='<test>junk</test>')
        self.assert_403(resp)

        resp, content = client.app_document_create_or_update_ext(pha_email=app_id, external_id='external1', body='<test>junk</test>')
        self.assert_403(resp)

        resp, content = client.app_document_label(pha_email=app_id, document_id=document_id, body='test label')
        self.assert_403(resp)

        resp, content = client.app_document_delete(pha_email=app_id, document_id=document_id)
        self.assert_403(resp)

    def _audit_access(self, client, record_id, document_id):
        """A principal in full control of the record, or a user app with access to the record."""
        resp, content = client.audit_record_view(record_id=record_id)
        self.assert_403(resp)

        resp, content = client.audit_document_view(record_id=record_id, document_id=document_id)
        self.assert_403(resp)

        resp, content = client.audit_function_view(record_id=record_id, document_id=document_id, function_name='record_document')
        self.assert_403(resp)

        resp, content = client.audit_query(record_id=record_id)
        self.assert_403(resp)

    def _autoshare_permissions(self, client, record_id, carenet_id, document_id):
        """A principal in full control of the record."""
        resp, content = client.autoshare_list(record_id=record_id)
        self.assert_403(resp)

        resp, content = client.autoshare_list_bytype_all(record_id=record_id)
        self.assert_403(resp)

        resp, content = client.autoshare_create(record_id=record_id, carenet_id=carenet_id)
        self.assert_403(resp)

        resp, content = client.autoshare_delete(record_id=record_id, carenet_id=carenet_id)
        self.assert_403(resp)

        resp, content = client.autoshare_revert(record_id=record_id, carenet_id=carenet_id, document_id=document_id)
        self.assert_403(resp)