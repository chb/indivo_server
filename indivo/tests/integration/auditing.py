import urlparse
from lxml import etree

from indivo.tests.data.reports import TEST_PROBLEMS
from indivo.tests.indivo_client_py.client import IndivoClient
from indivo.tests.internal_tests import IndivoLiveServerTestCase



class AuditingIntegrationTests(IndivoLiveServerTestCase):
    fixtures = ['machineApps', 'userApps', 'accountsWithRecords', 'statusNames', 'authSystems']

    ADMIN_CONSUMER_PARAMS = {"consumer_key": "admin_key",
                             "consumer_secret": "admin_secret"}
    CHROME_CONSUMER_PARAMS = {"consumer_key":"chrome_key",
                              "consumer_secret":"chrome_secret"}

    @classmethod
    def setUpClass(cls):
        super(AuditingIntegrationTests, cls).setUpClass()

    def setUp(self):
        super(AuditingIntegrationTests, self).setUp()
        server_params = {'api_base':self.live_server_url,
                         'authorization_base':'FAKE'}
        self.admin_client = IndivoClient(server_params, self.ADMIN_CONSUMER_PARAMS)
        self.chrome_client = IndivoClient(server_params, self.CHROME_CONSUMER_PARAMS)

    def test_auditing(self):
        record_id = 'dc10d0fd-a19a-404e-a3cc-1089dd8aa6e4'
        # set username and password
        resp, content = self.chrome_client.account_authsystem_add(account_email='testaccount@indivo.org',
                                                           body={'system':'password', 'username':'test',
                                                                 'password':'test_password'})
        self.assert_200(resp)

        resp, content = self.chrome_client.session_create({'username': 'test', 'password':'test_password'})
        self.assert_200(resp)
        params = dict(urlparse.parse_qsl(content))
        self.chrome_client.update_token(params)

        resp, content = self.chrome_client.record(record_id=record_id)
        self.assert_200(resp)

        resp, content = self.chrome_client.document_create(record_id=record_id, body=TEST_PROBLEMS[0])
        self.assert_200(resp)

        resp, content = self.chrome_client.record_document_list(record_id=record_id)
        self.assert_200(resp)

        root = etree.XML(content)
        docs = root.findall('Document')
        for doc in docs:
            doc_id = doc.attrib['id']
            resp, content = self.chrome_client.record_document(record_id=record_id, document_id=doc_id)
            self.assert_200(resp)

            # should have 4 items in the audit for this record
            resp, content = self.chrome_client.audit_query(record_id=record_id)
            self.assert_200(resp)
            self.assertEqual(len(etree.XML(content).findall('Report/Item/AuditEntry')), 4)

            # should have 1 item in the audit for this document
            resp, content = self.chrome_client.audit_query(record_id=record_id, body={'document_id':doc_id})
            self.assert_200(resp)
            self.assertEqual(len(etree.XML(content).findall('Report/Item/AuditEntry')), 1)

            # should have 1 item in the audit for this view
            resp, content = self.chrome_client.audit_query(record_id=record_id, body={'function_name':'record_document'})
            self.assert_200(resp)
            self.assertEqual(len(etree.XML(content).findall('Report/Item/AuditEntry')), 1)

            # should have 0 items in the audit for this view
            resp, content = self.chrome_client.audit_query(record_id=record_id, body={'function_name':'record_app_document'})
            self.assert_200(resp)
            self.assertEqual(len(etree.XML(content).findall('Report/Item/AuditEntry')), 0)
