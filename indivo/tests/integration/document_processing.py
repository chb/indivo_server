from lxml import etree

from indivo.tests.internal_tests import IndivoLiveServerTestCase

from indivo.tests.indivo_client_py.client import IndivoClient


class DocumentProcessingIntegrationTests(IndivoLiveServerTestCase):
    fixtures = ['machineApps', 'userApps', 'records', 'statusNames', 'authSystems', 'documentSchemas']

    @classmethod
    def setUpClass(cls):
        super(DocumentProcessingIntegrationTests, cls).setUpClass()

    def setUp(self):
        super(DocumentProcessingIntegrationTests, self).setUp()
        server_params = {'api_base':self.live_server_url,
                         'authorization_base':'FAKE'}
        self.admin_client = IndivoClient(server_params, self.ADMIN_CONSUMER_PARAMS)
        self.user_client = IndivoClient(server_params, self.AUTONOMOUS_CONSUMER_PARAMS)
        self.autonomous_app_email = 'testAutonomousApp@apps.indivo.org'

    def test_document_processing(self):
        #TODO: do the old tests make sense to port over?
        self.assertTrue(False)