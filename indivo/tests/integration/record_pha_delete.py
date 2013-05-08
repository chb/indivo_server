from indivo.tests.indivo_client_py.client import IndivoClient
from indivo.tests.internal_tests import IndivoLiveServerTestCase


class RecordPHADeleteIntegrationTests(IndivoLiveServerTestCase):
    fixtures = ['machineApps', 'userApps', 'accountsWithRecords', 'authSystems', 'statusNames']

    @classmethod
    def setUpClass(cls):
        super(RecordPHADeleteIntegrationTests, cls).setUpClass()

    def setUp(self):
        super(RecordPHADeleteIntegrationTests, self).setUp()
        server_params = {'api_base':self.live_server_url,
                         'authorization_base':'FAKE'}
        self.admin_client = IndivoClient(server_params, self.ADMIN_CONSUMER_PARAMS)
        self.user_client = IndivoClient(server_params, self.USER_CONSUMER_PARAMS)
        self.app_email = 'testApp@apps.indivo.org'

    def test_record_pha_delete(self):
        record_id = 'dc10d0fd-a19a-404e-a3cc-1089dd8aa6e4'

        # enable app
        resp, content = self.admin_client.record_pha_setup(record_id=record_id, pha_email=self.app_email)
        self.assert_200(resp)

        # enable app again
        resp, content = self.admin_client.record_pha_setup(record_id=record_id, pha_email=self.app_email)
        self.assert_200(resp)

        # disable app
        resp, content = self.admin_client.pha_record_delete(record_id=record_id, pha_email=self.app_email)
        self.assert_200(resp)

        # disable app again
        resp, content = self.admin_client.pha_record_delete(record_id=record_id, pha_email=self.app_email)
        self.assert_200(resp)

        # disable app with bad Record ID
        resp, content = self.admin_client.pha_record_delete(record_id='junk', pha_email=self.app_email)
        self.assert_404(resp)

        # disable app with bad App ID
        resp, content = self.admin_client.pha_record_delete(record_id=record_id, pha_email='junk')
        self.assert_404(resp)