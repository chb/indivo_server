import django.test
from indivo.models import *
from indivo.tests.internal_tests import InternalTests
from indivo.tests.data.account import TEST_ACCOUNTS
from indivo.tests.data.app import TEST_USERAPPS
from indivo.tests.data.document import TEST_A_DOCS

class PHAInternalTests(InternalTests):

    def setUp(self):
        super(PHAInternalTests,self).setUp()

        # create app
        self.app = self.createUserApp(TEST_USERAPPS[0])

        # create account
        self.account = self.createAccount(TEST_ACCOUNTS[4])
        
        # create app specific externally referenced doc
        self.external_doc = self.createDocument(TEST_A_DOCS[1], pha=self.app)

        # create app specific doc
        self.doc = self.createDocument(TEST_A_DOCS[0], pha=self.app)

    def tearDown(self):
        super(PHAInternalTests,self).tearDown()

    def test_list_apps(self):
        response = self.client.get('/apps/')
        self.assertEquals(response.status_code, 200)    

    def test_delete_app(self):
        response = self.client.delete('/apps/%s'%(self.app.email))
        self.assertEquals(response.status_code, 200)    
    
    def test_get_app(self):
        response = self.client.get('/apps/%s'%(self.app.email))
        self.assertEquals(response.status_code, 200)

    def test_get_external_document_meta(self):
        response = self.client.get('/apps/%s/documents/external/%s/meta'%(self.app.email,TEST_A_DOCS[1].local_external_id))
        self.assertEquals(response.status_code, 200)            

    def test_put_external_document(self):
        response = self.client.put('/apps/%s/documents/external/%s'%(self.app.email, 'some_ext_id'))
        self.assertEquals(response.status_code, 200)

    def test_get_document_label(self):
        response = self.client.get('/apps/%s/documents/%s/label'%(self.app.email,self.doc.id))
        self.assertEquals(response.status_code, 200)            

    def test_get_document_meta(self):
        response = self.client.get('/apps/%s/documents/%s/meta'%(self.app.email,self.doc.id))
        self.assertEquals(response.status_code, 200)            

    def test_put_document(self):
        response = self.client.put('/apps/%s/documents/%s'%(self.app.email,self.doc.id))        
        self.assertEquals(response.status_code, 200)            

    def test_get_document(self):
        response = self.client.get('/apps/%s/documents/%s'%(self.app.email,self.doc.id))        
        self.assertEquals(response.status_code, 200)            

    def test_delete_document(self):
        response = self.client.delete('/apps/%s/documents/%s'%(self.app.email, self.doc.id))
        self.assertEquals(response.status_code, 200)

    def test_put_document(self):
        response = self.client.get('/apps/%s/documents/%s/update'%(self.app.email,self.doc.id))
        self.assertEquals(response.status_code, 200)            

    def test_list_document(self):
        response = self.client.get('/apps/%s/documents/'%(self.app.email))        
        self.assertEquals(response.status_code, 200)            

    def test_create_document(self):
        response = self.client.post('/apps/%s/documents/'%(self.app.email))        
        self.assertEquals(response.status_code, 200)            
