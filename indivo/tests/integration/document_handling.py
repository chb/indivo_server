import urlparse
from lxml import etree

from indivo.tests.internal_tests import IndivoLiveServerTestCase

from indivo.tests.indivo_client_py.client import IndivoClient
from indivo.tests.data import TEST_DEMOGRAPHICS_XML


class DocumentHandlingIntegrationTests(IndivoLiveServerTestCase):
    fixtures = ['machineApps', 'userApps', 'accountsWithRecords', 'statusNames', 'authSystems', 'documentSchemas']

    ADMIN_CONSUMER_PARAMS = {"consumer_key": "admin_key",
                             "consumer_secret": "admin_secret"}
    CHROME_CONSUMER_PARAMS = {"consumer_key":"chrome_key",
                              "consumer_secret":"chrome_secret"}

    @classmethod
    def setUpClass(cls):
        super(DocumentHandlingIntegrationTests, cls).setUpClass()

    def setUp(self):
        super(DocumentHandlingIntegrationTests, self).setUp()
        server_params = {'api_base':self.live_server_url,
                         'authorization_base':'FAKE'}
        self.admin_client = IndivoClient(server_params, self.ADMIN_CONSUMER_PARAMS)
        self.chrome_client = IndivoClient(server_params, self.CHROME_CONSUMER_PARAMS)

    def test_document_handling(self):
        account_id = 'testaccount@indivo.org'
        # Create a new record by external ID, twice.
        resp, content = self.admin_client.record_create_ext(principal_email='admin@apps.indivo.org', external_id='record_ext_foobar', body=TEST_DEMOGRAPHICS_XML)
        self.assert_200(resp)
        record_id_1 = etree.XML(content).attrib['id']
        resp, content = self.admin_client.record_create_ext(principal_email='admin@apps.indivo.org', external_id='record_ext_foobar', body=TEST_DEMOGRAPHICS_XML)
        self.assert_200(resp)
        record_id_2 = etree.XML(content).attrib['id']
        self.assertEqual(record_id_1, record_id_2)

        self.chrome_client.record_set_owner(record_id=record_id_1, body=account_id)

        # set username and password
        resp, content = self.chrome_client.account_authsystem_add(account_email=account_id,
                                                                  body={'system':'password', 'username':'test',
                                                                        'password':'test_password'})
        self.assert_200(resp)

        resp, content = self.chrome_client.session_create({'username': 'test', 'password':'test_password'})
        self.assert_200(resp)
        token = dict(urlparse.parse_qsl(content))
        self.chrome_client.update_token(token)

        # write document and read it and its meta data
        resp, content = self.chrome_client.document_create(record_id=record_id_1, body="<test>doc1</test>")
        self.assert_200(resp)
        doc_id = etree.XML(content).attrib['id']
        resp, content = self.chrome_client.record_document(record_id=record_id_1, document_id=doc_id)
        self.assert_200(resp)
        resp, content = self.chrome_client.record_document_meta(record_id=record_id_1, document_id=doc_id)
        self.assert_200(resp)

        # change status of the document, and check the status history
        resp, content = self.chrome_client.document_set_status(record_id=record_id_1, document_id=doc_id, body={'status':'void','reason':'void reason'})
        self.assert_200(resp)
        resp, content = self.chrome_client.document_set_status(record_id=record_id_1, document_id=doc_id, body={'status':'archived','reason':'archived reason'})
        self.assert_200(resp)
        resp, content = self.chrome_client.document_set_status(record_id=record_id_1, document_id=doc_id, body={'status':'active','reason':'active reason'})
        self.assert_200(resp)
        resp, content = self.chrome_client.document_set_status(record_id=record_id_1, document_id=doc_id, body={'status':'void','reason':'void reason 2'})
        self.assert_200(resp)
        resp, content = self.chrome_client.document_set_status(record_id=record_id_1, document_id=doc_id, body={'status':'badstatus','reason':'bad reason'})
        self.assert_400(resp)
        resp, content = self.chrome_client.document_status_history(record_id=record_id_1, document_id=doc_id)
        self.assert_200(resp)
        self.assertEqual(len(etree.XML(content).findall('DocumentStatus')), 4)

        # create an 'active' document
        resp, content = self.chrome_client.document_create(record_id=record_id_1, body="<test>doc2</test>")
        self.assert_200(resp)

        # retrieve documents by status
        resp, content = self.chrome_client.record_document_list(record_id=record_id_1)
        self.assert_200(resp)
        self.assertEqual(len(etree.XML(content).findall('Document')), 2)
        resp, content = self.chrome_client.record_document_list(record_id=record_id_1, body={'status':'active'})
        self.assert_200(resp)
        self.assertEqual(len(etree.XML(content).findall('Document')), 2)
        resp, content = self.chrome_client.record_document_list(record_id=record_id_1, body={'status':'void'})
        self.assert_200(resp)
        self.assertEqual(len(etree.XML(content).findall('Document')), 1)

        # retrieve documents by type
        resp, content = self.chrome_client.record_document_list(record_id=record_id_1, body={'type':'Demographics'})
        self.assert_200(resp)
        self.assertEqual(len(etree.XML(content).findall('Document')), 1)

        # read document versions
        resp, content = self.chrome_client.document_versions(record_id=record_id_1, document_id=doc_id)
        self.assert_200(resp)

        # attach a document label
        resp, content = self.chrome_client.record_document_label(record_id=record_id_1, document_id=doc_id, body='test_label')
        self.assert_200(resp)

        # add a related document
        annotation_doc = '<test>annotation</test>'
        resp, content = self.chrome_client.document_create(record_id=record_id_1, body=annotation_doc)
        self.assert_200(resp)
        annotation_doc_id = etree.XML(content).attrib['id']
        resp, content = self.chrome_client.document_rels(record_id=record_id_1, document_id_0=doc_id, document_id_1=annotation_doc_id, rel='annotation')
        self.assert_200(resp)

        # retrieve related documents
        resp, content = self.chrome_client.get_documents_by_rel(record_id=record_id_1, document_id=doc_id, rel='annotation')
        self.assert_200(resp)
        self.assertEqual(len(etree.XML(content).findall('Document')), 1)

        original_doc_id = doc_id

        # version the document
        for doc in ['<test>doc3</test>', '<test>doc4</test>', '<test>doc5</test>', '<test>doc6</test>']:
            resp, content = self.chrome_client.document_version(record_id=record_id_1, document_id=doc_id, body=doc)
            self.assert_200(resp)
            doc_id = etree.XML(content).attrib['id']

        # try to replace an already replaced document
        resp, content = self.chrome_client.document_version(record_id=record_id_1, document_id=original_doc_id, body='<test>doc7</test>')
        self.assert_400(resp)

        # try to replace a non-existent document
        resp, content = self.chrome_client.document_version(record_id=record_id_1, document_id='facke', body='<test>doc7</test>')
        self.assert_404(resp)

        # check version count
        resp, content = self.chrome_client.document_versions(record_id=record_id_1, document_id=doc_id)
        self.assert_200(resp)
        self.assertEqual(len(etree.XML(content).findall('Document')), 4)
