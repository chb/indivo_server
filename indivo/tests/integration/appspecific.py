from lxml import etree

from indivo.tests.indivo_client_py.client import IndivoClient
from indivo.tests.data.reports import TEST_ALLERGIES, TEST_IMMUNIZATIONS
from indivo.tests.internal_tests import IndivoLiveServerTestCase


class AppSpecificIntegrationTests(IndivoLiveServerTestCase):
    fixtures = ['authSystems', 'machineApps', 'userApps', 'records', 'statusNames']

    @classmethod
    def setUpClass(cls):
        super(AppSpecificIntegrationTests, cls).setUpClass()

    def setUp(self):
        super(AppSpecificIntegrationTests, self).setUp()
        server_params = {'api_base':self.live_server_url,
                         'authorization_base':'FAKE'}
        self.admin_client = IndivoClient(server_params, self.ADMIN_CONSUMER_PARAMS)
        self.user_client = IndivoClient(server_params, self.USER_CONSUMER_PARAMS)
        self.user_app_email = 'testApp@apps.indivo.org'

    def test_appspecific(self):
        """
        ensure that app-specific and app-record-specific data are
        properly partitioned
        """
        record_id = 'dc10d0fd-a19a-404e-a3cc-1089dd8aa6e3'
        resp, content = self.admin_client.record_pha_setup(record_id=record_id, pha_email=self.user_app_email)
        token = self.parse_tokens(content)

        # store an app-specific document
        resp, content = self.user_client.app_document_create_or_update_ext(pha_email=self.user_app_email,
                                                                           external_id='foobar_partition_appspecific',
                                                                           body=TEST_ALLERGIES[0])
        self.assert_200(resp)
        root = etree.XML(content)
        app_specific_doc_id = root.attrib['id']

        # store an app-record-specific document
        self.user_client.update_token(token)
        resp, content = self.user_client.record_app_document_create_or_update_ext(record_id=record_id,
                                                                                  pha_email=self.user_app_email,
                                                                                  external_id='foobar_partition_apprecordspecific',
                                                                                  body=TEST_ALLERGIES[0])
        self.assert_200(resp)
        root = etree.XML(content)
        app_record_specific_doc_id = root.attrib['id']

        # get it by metadata
        self.user_client.record_app_document_meta_ext(record_id=record_id,
                                                      pha_email=self.user_app_email,
                                                      external_id='foobar_partition_apprecordspecific')
        self.assert_200(resp)

        self.user_client.token = None
        resp, content = self.user_client.app_document_list(pha_email=self.user_app_email, body={})
        self.assert_200(resp)
        root = etree.XML(content)
        docs = root.findall('Document')
        app_doc_ids = [doc.attrib['id'] for doc in docs]

        self.user_client.update_token(token)
        resp, content = self.user_client.record_app_document_list(record_id=record_id, pha_email=self.user_app_email)
        self.assert_200(resp)
        root = etree.XML(content)
        docs = root.findall('Document')
        app_record_doc_ids = [doc.attrib['id'] for doc in docs]

        self.assertIn(app_specific_doc_id, app_doc_ids)
        self.assertNotIn(app_specific_doc_id, app_record_doc_ids)
        self.assertIn(app_record_specific_doc_id, app_record_doc_ids)
        self.assertNotIn(app_record_specific_doc_id, app_doc_ids)

        # authorize the App on a second Record
        record_id_2 = 'e18b00e7-8772-4db4-8e41-6ab3cfbfea67'
        resp, content = self.admin_client.record_pha_setup(record_id=record_id_2, pha_email=self.user_app_email)
        token_2 = self.parse_tokens(content)

        # add an app-record-specific doc in there, shouldn't affect either of the other two, and should be able to use the same external_id
        self.user_client.update_token(token_2)
        resp, content = self.user_client.record_app_document_create_or_update_ext(record_id=record_id_2, pha_email=self.user_app_email,
                                                                                  external_id='foobar_partition_apprecordspecific',
                                                                                  body=TEST_IMMUNIZATIONS[0])
        self.assert_200(resp)

        self.user_client.token = None
        resp, content = self.user_client.app_document_list(pha_email=self.user_app_email, body={})
        self.assert_200(resp)
        root = etree.XML(content)
        docs = root.findall('Document')
        app_doc_ids = [doc.attrib['id'] for doc in docs]

        self.user_client.update_token(token)
        resp, content = self.user_client.record_app_document_list(record_id=record_id, pha_email=self.user_app_email)
        self.assert_200(resp)
        root = etree.XML(content)
        docs = root.findall('Document')
        app_record_doc_ids = [doc.attrib['id'] for doc in docs]

        self.assertIn(app_specific_doc_id, app_doc_ids)
        self.assertNotIn(app_specific_doc_id, app_record_doc_ids)
        self.assertIn(app_record_specific_doc_id, app_record_doc_ids)
        self.assertNotIn(app_record_specific_doc_id, app_doc_ids)