from lxml import etree

from indivo.tests.indivo_client_py.client import IndivoClient
from indivo.tests.internal_tests import IndivoLiveServerTestCase


class RecordSharesIntegrationTests(IndivoLiveServerTestCase):
    fixtures = ['machineApps', 'userApps', 'accountsWithRecords', 'authSystems', 'statusNames']

    @classmethod
    def setUpClass(cls):
        super(RecordSharesIntegrationTests, cls).setUpClass()

    def setUp(self):
        super(RecordSharesIntegrationTests, self).setUp()
        server_params = {'api_base':self.live_server_url,
                         'authorization_base':'FAKE'}
        self.chrome_client = IndivoClient(server_params, self.CHROME_CONSUMER_PARAMS)
        self.user_client = IndivoClient(server_params, self.USER_CONSUMER_PARAMS)

    def test_record_shares(self):
        record_id = 'dc10d0fd-a19a-404e-a3cc-1089dd8aa6e4'
        new_account_id = 'ben@indivo.org'

        # read shares
        resp, content = self.chrome_client.record_shares(record_id=record_id)
        self.assert_200(resp)
        self.assertEqual(len(etree.XML(content).findall('Share')), 0)

        # create new account and share record with it
        resp, content = self.chrome_client.account_create({'account_id':new_account_id, 'contact_email':'ben@test.com'})
        self.assert_200(resp)
        resp, content = self.chrome_client.record_share_add(record_id=record_id, body={'account_id':new_account_id})
        self.assert_200(resp)

        # try to share again, with a role label this time
        resp, content = self.chrome_client.record_share_add(record_id=record_id, body={'account_id':new_account_id, 'role_label':'test role'})
        self.assert_200(resp)

        # read shares
        resp, content = self.chrome_client.record_shares(record_id=record_id)
        self.assert_200(resp)
        shares = etree.XML(content).findall('Share')
        self.assertEqual(len(shares), 1)
        self.assertEqual(shares[0].attrib['account'], new_account_id)

        # delete share
        resp, content = self.chrome_client.record_share_delete(record_id=record_id, other_account_id=new_account_id)
        self.assert_200(resp)

        # read shares
        resp, content = self.chrome_client.record_shares(record_id=record_id)
        self.assert_200(resp)
        self.assertEqual(len(etree.XML(content).findall('Share')), 0)