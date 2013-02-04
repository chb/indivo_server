from indivo.models import *
from indivo.tests.internal_tests import InternalTests
from indivo.tests.data import *
from lxml import etree
from urlparse import parse_qs
from django.utils import simplejson

class PHAInternalTests(InternalTests):

    def setUp(self):
        super(PHAInternalTests,self).setUp()

        # create app
        self.app = self.createUserApp(TEST_USERAPPS, 0)

        # and an autonomous app
        self.autonomous_app = self.createUserApp(TEST_AUTONOMOUS_APPS, 0)

        # create account
        self.account = self.createAccount(TEST_ACCOUNTS, 4)

        # create a record and bind the autonomous app to it
        self.record = self.createRecord(TEST_RECORDS, 0, owner=self.account)
        self.addAppToRecord(record=self.record, with_pha=self.autonomous_app)

        # create another record and don't bind the app to it.
        self.unbound_record = self.createRecord(TEST_RECORDS, 1, owner=self.account)
        
        # create app specific externally referenced doc
        self.external_doc = self.createDocument(TEST_A_DOCS, 1, pha=self.app)

        # create app specific doc
        self.doc = self.createDocument(TEST_A_DOCS, 0, pha=self.app)

    def tearDown(self):
        super(PHAInternalTests,self).tearDown()

    def test_get_smart_manifests(self):
        response = self.client.get('/apps/manifests/')
        self.assertEqual(response.status_code, 200)
        apps = simplejson.loads(response.content)
        self.assertEqual(len(apps), 2)
        app1, app2 = apps
        if app1['name'] == self.app.name:
            self.assertEqual(app1, self.app.to_manifest(smart_only=True, as_string=False))
            self.assertEqual(app2, self.autonomous_app.to_manifest(smart_only=True, as_string=False))
        else:
            self.assertEqual(app2, self.app.to_manifest(smart_only=True, as_string=False))
            self.assertEqual(app1, self.autonomous_app.to_manifest(smart_only=True, as_string=False))

    def test_get_smart_manifest(self):
        response = self.client.get('/apps/%s/manifest'%self.app.email)
        self.assertEqual(response.status_code, 200)
        app = simplejson.loads(response.content)
        self.assertEqual(app, self.app.to_manifest(smart_only=True, as_string=False))

    def test_list_apps(self):
        response = self.client.get('/apps/')
        self.assertEquals(response.status_code, 200)    

    def test_delete_app(self):
        response = self.client.delete('/apps/%s'%(self.app.email))
        self.assertEquals(response.status_code, 200)    
    
    def test_get_app(self):
        response = self.client.get('/apps/%s'%(self.app.email))
        self.assertEquals(response.status_code, 200)

    def test_get_external_document(self):
        response = self.client.get('/apps/%s/documents/external/%s'%(self.app.email,TEST_A_DOCS[1]['external_id']))
        self.assertEquals(response.status_code, 200)            
    
    def test_get_external_document_meta(self):
        response = self.client.get('/apps/%s/documents/external/%s/meta'%(self.app.email,TEST_A_DOCS[1]['external_id']))
        self.assertEquals(response.status_code, 200)            

    def test_put_external_document(self):
        response = self.client.put('/apps/%s/documents/external/%s'%(self.app.email, 'some_ext_id'))
        self.assertEquals(response.status_code, 200)

    def test_put_document_label(self):
        url = '/apps/%s/documents/%s/label'%(self.app.email,self.doc.id)
        newlabel = self.doc.label.upper()

        bad_methods = ['get','post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.put(url, data=newlabel, content_type='text/plain')
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

    def test_list_document(self):
        response = self.client.get('/apps/%s/documents/'%(self.app.email))        
        self.assertEquals(response.status_code, 200)            

    def test_create_document(self):
        response = self.client.post('/apps/%s/documents/'%(self.app.email))        
        self.assertEquals(response.status_code, 200)            

    def test_list_app_records(self):
        response = self.client.get('/apps/%s/records/'%(self.autonomous_app.email))
        self.assertEqual(response.status_code, 200)

        # Make sure we got our record back (and not the unbound record).
        xml = etree.XML(response.content)
        records = xml.findall('Record')
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].get('id'), self.record.id)
        self.assertEqual(records[0].get('label'), self.record.label)
        self.assertFalse(records[0].get('shared'))
        self.assertNotEqual(records[0].get('id'), self.unbound_record.id)
        self.assertNotEqual(records[0].get('label'), self.unbound_record.label)
        
    def test_post_autonomous_access_token(self):
        response = self.client.post('/apps/%s/records/%s/access_token' % (self.autonomous_app.email, self.record.id))
        self.assertEqual(response.status_code, 200)

        # Make sure we got something that looks like an access token
        content = parse_qs(response.content)
        self.assertTrue(content.has_key('oauth_token'))
        self.assertTrue(content.has_key('oauth_token_secret'))
        self.assertTrue(content.has_key('xoauth_indivo_record_id'))
