import django.test
from indivo.models import *
from internal_tests import InternalTests

#app vars
APP_EMAIL,ASDF = ('myApp@my.com', 'asdf')
#account vars
EMAIL, FULLNAME, CONTACT_EMAIL, USERNAME, PASSWORD, RECORDS, PRIMARY_SECRET, SECONDARY_SECRET = ("mymail@mail.ma","full name","contact@con.con","user","pass",("the mom", "the dad", "the son", "the daughter"), 'psecret', 'ssecret')
#doc vars
DOCUMENT, DOC_LABEL, EXT_ID = ('''<DOC>HERE'S MY CONTENT</DOC>''', 'A Document!', 'ext_id')

class PHAInternalTests(InternalTests):

    def setUp(self):
        super(PHAInternalTests,self).setUp()
        # create app
        pha_args = {'name' : 'myApp', \
                        'email' : APP_EMAIL, \
                        'consumer_key' : 'myapp', \
                        'secret' : 'myapp', \
                        'has_ui' : True, \
                        'frameable' : True, \
                        'is_autonomous' : False, \
                        'autonomous_reason' : '', \
                        'start_url_template' : 'http://myapp.com/start', \
                        'callback_url' : 'http://myapp.com/afterauth', \
                        'description' : 'ITS MY APP'}
        self.pha = self.createPHA(**pha_args)

        # create account
        acct_args = {'email':EMAIL, 'full_name':FULLNAME, 'contact_email':CONTACT_EMAIL, 'primary_secret':PRIMARY_SECRET, 'secondary_secret':SECONDARY_SECRET}
        self.accounts = self.createAccount(USERNAME, PASSWORD, RECORDS, **acct_args)
        
        # create app specific externally referenced doc
        md = hashlib.sha256()
        md.update(DOCUMENT)
        doc_args = {'content':DOCUMENT,
                    'pha':self.pha,
                    'size':len(DOCUMENT),
                    'digest': md.hexdigest(),
                    'label': DOC_LABEL, 
                    'creator': self.accounts,
                    'external_id' : Document.prepare_external_id(EXT_ID, self.pha, pha_specific=True, record_specific=False) }
        self.external_doc = self.createDocument(**doc_args)
        # create app specific doc
        doc_args = {'content':DOCUMENT,
                    'pha':self.pha,
                    'size':len(DOCUMENT),
                    'digest': md.hexdigest(),
                    'label': DOC_LABEL, 
                    'creator': self.accounts }
        self.doc = self.createDocument(**doc_args)

    def tearDown(self):
        super(PHAInternalTests,self).tearDown()

    def test_list_apps(self):
        response = self.client.get('/apps/')
        self.assertEquals(response.status_code, 200)    

    def test_delete_app(self):
        response = self.client.delete('/apps/%s'%(APP_EMAIL))
        self.assertEquals(response.status_code, 200)    
    
    def test_get_app(self):
        response = self.client.get('/apps/%s'%(APP_EMAIL))
        self.assertEquals(response.status_code, 200)

    def test_get_external_document_meta(self):
        response = self.client.get('/apps/%s/documents/external/%s/meta'%(APP_EMAIL,EXT_ID))
        self.assertEquals(response.status_code, 200)            

    def test_put_external_document(self):
        response = self.client.put('/apps/%s/documents/external/%s'%(APP_EMAIL, 'some_ext_id'))
        self.assertEquals(response.status_code, 200)

    def test_get_document_label(self):
        response = self.client.get('/apps/%s/documents/%s/label'%(APP_EMAIL,self.doc.id))
        self.assertEquals(response.status_code, 200)            

    def test_get_document_meta(self):
        response = self.client.get('/apps/%s/documents/%s/meta'%(APP_EMAIL,self.doc.id))
        self.assertEquals(response.status_code, 200)            

    def test_put_document(self):
        response = self.client.put('/apps/%s/documents/%s'%(APP_EMAIL,self.doc.id))        
        self.assertEquals(response.status_code, 200)            

    def test_get_document(self):
        response = self.client.get('/apps/%s/documents/%s'%(APP_EMAIL,self.doc.id))        
        self.assertEquals(response.status_code, 200)            

    def test_put_document(self):
        response = self.client.get('/apps/%s/documents/%s/update'%(APP_EMAIL,self.doc.id))
        self.assertEquals(response.status_code, 200)            

    def test_list_document(self):
        response = self.client.get('/apps/%s/documents/'%(APP_EMAIL))        
        self.assertEquals(response.status_code, 200)            

    def test_create_document(self):
        response = self.client.post('/apps/%s/documents/'%(APP_EMAIL))        
        self.assertEquals(response.status_code, 200)            
