from lxml import etree

from indivo.tests.internal_tests import IndivoLiveServerTestCase

from indivo.tests.indivo_client_py.client import IndivoClient


class DocumentMetadataIntegrationTests(IndivoLiveServerTestCase):
    fixtures = ['machineApps', 'userApps', 'records', 'statusNames']

    @classmethod
    def setUpClass(cls):
        super(DocumentMetadataIntegrationTests, cls).setUpClass()

    def setUp(self):
        super(DocumentMetadataIntegrationTests, self).setUp()
        server_params = {'api_base':self.live_server_url,
                         'authorization_base':'FAKE'}
        self.admin_client = IndivoClient(server_params, self.ADMIN_CONSUMER_PARAMS)
        self.user_client = IndivoClient(server_params, self.AUTONOMOUS_CONSUMER_PARAMS)
        self.autonomous_app_email = 'testAutonomousApp@apps.indivo.org'

    def test_document_metadata(self):
        record_id = 'dc10d0fd-a19a-404e-a3cc-1089dd8aa6e3'

        resp, content = self.admin_client.record_pha_setup(record_id=record_id, pha_email=self.autonomous_app_email)
        self.assert_200(resp)
        token = self.parse_tokens(content)
        self.user_client.update_token(token)

        # record specific
        resp, content = self.user_client.document_create(record_id=record_id, body='<test>doc1</test>')
        self.assert_200(resp)
        doc_id = etree.XML(content).attrib['id']
        resp, content = self.user_client.record_document_meta(record_id=record_id, document_id=doc_id)
        self.assert_200(resp)

        # record specific with external ID
        resp, content = self.user_client.document_create_by_ext_id(record_id=record_id, pha_email=self.autonomous_app_email, external_id='extid1', body='<test>doc1</test>')
        self.assert_200(resp)
        resp, content = self.user_client.record_document_meta_ext(record_id=record_id, pha_email=self.autonomous_app_email, external_id='extid1')
        self.assert_200(resp)

        # record app specific
        resp, content = self.user_client.record_app_document_create(record_id=record_id, pha_email=self.autonomous_app_email, body='<test>doc1</test>')
        self.assert_200(resp)
        doc_id = etree.XML(content).attrib['id']
        resp, content = self.user_client.record_app_document_meta(record_id=record_id, pha_email=self.autonomous_app_email, document_id=doc_id)
        self.assert_200(resp)

        # record app specific with external ID
        resp, content = self.user_client.record_app_document_create_or_update_ext(record_id=record_id, pha_email=self.autonomous_app_email, external_id='extid2', body='<test>doc1</test>')
        self.assert_200(resp)
        resp, content = self.user_client.record_app_document_meta_ext(record_id=record_id, pha_email=self.autonomous_app_email, external_id='extid2')
        self.assert_200(resp)

        # app specific
        resp, content = self.user_client.app_document_create(pha_email=self.autonomous_app_email, body='<test>doc1</test>')
        self.assert_200(resp)
        doc_id = etree.XML(content).attrib['id']
        resp, content = self.user_client.app_document_meta(pha_email=self.autonomous_app_email, document_id=doc_id)
        self.assert_200(resp)

        # app specific with external ID
        resp, content = self.user_client.app_document_create_or_update_ext(pha_email=self.autonomous_app_email, external_id='extid3', body='<test>doc1</test>')
        self.assert_200(resp)
        resp, content = self.user_client.app_document_meta_ext(pha_email=self.autonomous_app_email, external_id='extid3')
        self.assert_200(resp)