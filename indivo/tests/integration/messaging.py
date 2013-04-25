from lxml import etree

from indivo.tests.internal_tests import IndivoLiveServerTestCase

from indivo.tests.indivo_client_py.client import IndivoClient


class MessagingIntegrationTests(IndivoLiveServerTestCase):
    fixtures = ['machineApps', 'userApps', 'accountsWithRecords', 'authSystems', 'statusNames']

    @classmethod
    def setUpClass(cls):
        super(MessagingIntegrationTests, cls).setUpClass()

    def setUp(self):
        super(MessagingIntegrationTests, self).setUp()
        server_params = {'api_base':self.live_server_url,
                         'authorization_base':'FAKE'}
        self.admin_client = IndivoClient(server_params, self.ADMIN_CONSUMER_PARAMS)
        self.chrome_client = IndivoClient(server_params, self.CHROME_CONSUMER_PARAMS)
        self.user_client = IndivoClient(server_params, self.AUTONOMOUS_CONSUMER_PARAMS)
        self.autonomous_app_email = 'testAutonomousApp@apps.indivo.org'

    def test_document_messaging(self):
        record_id = 'dc10d0fd-a19a-404e-a3cc-1089dd8aa6e4'
        account_id = 'testaccount@indivo.org'

        message = {'body': 'test body',
                   'subject': 'test subject'}

        # message account from admin app
        resp, content = self.admin_client.account_send_message(account_email=account_id, body=message)
        self.assert_200(resp)

        # message record from admin app
        resp, content = self.admin_client.record_send_message(record_id=record_id, message_id='1', body=message)
        self.assert_200(resp)
        resp, content = self.admin_client.record_send_message(record_id=record_id, message_id='1', body=message)
        self.assert_400(resp)

        # message record from user app
        resp, content = self.admin_client.record_pha_setup(record_id=record_id, pha_email=self.autonomous_app_email)
        self.assert_200(resp)
        token = self.parse_tokens(content)
        self.user_client.update_token(token)
        resp, content = self.user_client.record_send_message(record_id=record_id, message_id='2', body=message)
        self.assert_200(resp)

        resp, content = self.chrome_client.account_authsystem_add(account_email=account_id,
                                                                  body={'system':'password', 'username':'test',
                                                                        'password':'test_password'})
        self.assert_200(resp)

        # see if we can create a session for it
        resp, content = self.chrome_client.session_create({'username': 'test', 'password':'test_password'})
        self.assert_200(resp)
        token = self.parse_tokens(content)
        self.chrome_client.update_token(token)

        resp, content = self.chrome_client.account_inbox(account_email=account_id)
        self.assert_200(resp)
        root = etree.XML(content)
        self.assertEqual(len(root.findall('Message')), 3)
        message_id = root.find('Message').attrib['id']

        resp, content = self.chrome_client.account_message_archive(account_email=account_id, message_id=message_id)
        self.assert_200(resp)

        resp, content = self.chrome_client.account_inbox(account_email=account_id)
        self.assert_200(resp)
        root = etree.XML(content)
        self.assertEqual(len(root.findall('Message')), 2)

        #TODO message attachments, different severity, different body_types, notification emails