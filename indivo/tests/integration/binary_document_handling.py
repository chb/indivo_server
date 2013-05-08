import base64

from indivo.tests.internal_tests import IndivoLiveServerTestCase
from indivo.tests.indivo_client_py.client import IndivoClient


class BinaryDocumentIntegrationTests(IndivoLiveServerTestCase):
    fixtures = ['userApps', 'statusNames']

    @classmethod
    def setUpClass(cls):
        super(BinaryDocumentIntegrationTests, cls).setUpClass()

    def setUp(self):
        super(BinaryDocumentIntegrationTests, self).setUp()
        server_params = {'api_base':self.live_server_url,
                         'authorization_base':'FAKE'}
        self.client = IndivoClient(server_params, self.USER_CONSUMER_PARAMS)

    def test_binary_documents(self):
        with open('indivo/tests/data/binary/xxsmall_binary.chp', 'rb') as binary_file:
            resp, content = self.client.app_document_create(pha_email='testApp@apps.indivo.org', body=base64.b64encode(binary_file.read()))
            self.assert_200(resp)