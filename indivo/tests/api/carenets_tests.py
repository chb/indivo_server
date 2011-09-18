import django.test
from indivo.models import *
from indivo.tests.internal_tests import InternalTests
from django.utils.http import urlencode
import hashlib

EMAIL, FULLNAME, CONTACT_EMAIL, USERNAME, PASSWORD, RECORDS = ("mymail@mail.ma","full name","contact@con.con","user","pass",("the mom", "the dad", "the son", "the daughter"))

EMAIL2 = "mymail2@mail.ma"
USER2 = "user2"

EMAIL3 = "mymail3@mail.ma"
USER3 = "user3"

DOCUMENT = '''<DOC>HERE'S MY CONTENT</DOC>'''
DOCUMENT2 = '''<DOC>HERE'S MY CONTENT 2!</DOC>'''
DOC_LABEL = 'A Document!'

CONTACT = '''<Contact id="5326" xmlns="http://indivo.org/vocab/xml/documents#"> <name> <fullName>Sebastian Rockwell Cotour</fullName> <givenName>Sebastian</givenName> <familyName>Cotour</familyName> </name> <email type="personal"> <emailAddress>scotour@hotmail.com</emailAddress> </email> <email type="work"> <emailAddress>sebastian.cotour@childrens.harvard.edu</emailAddress> </email> <address type="home"> <streetAddress>15 Waterhill Ct.</streetAddress> <postalCode>53326</postalCode> <locality>New Brinswick</locality> <region>Montana</region> <country>US</country> <timeZone>-7GMT</timeZone> </address> <location type="home"> <latitude>47N</latitude> <longitude>110W</longitude> </location> <phoneNumber type="home">5212532532</phoneNumber> <phoneNumber type="work">6217233734</phoneNumber> <instantMessengerName protocol="aim">scotour</instantMessengerName> </Contact>'''

DEMOGRAPHICS = '''<Demographics xmlns="http://indivo.org/vocab/xml/documents#"> <foo>bar</foo></Demographics>'''

SPECIAL_DOCS = {'contact':CONTACT, 'demographics':DEMOGRAPHICS}

LAB_CODE = 'HBA1C' # MAKE SURE TO ADD THESE MEASUREMENTS

CARENET_NAME = 'NEWNAME'

class CarenetInternalTests(InternalTests):
    accounts = []
    records = []
    carenets = []
    phas = []
    docs = []
    special_docs = []

    def setUp(self):
        super(CarenetInternalTests,self).setUp()

        # reset our state
        self.accounts = []
        self.records = []
        self.carenets = []
        self.phas = []
        self.docs = []
        self.special_docs = []

        # Create an account, with some records that can be shared and their default carenets
        # Don't track this account, since it can't share with itself
        acct_args = {'email':EMAIL, 'full_name':FULLNAME, 'contact_email':CONTACT_EMAIL}
        self.createAccount(USERNAME, PASSWORD, RECORDS, **acct_args)

        # Track the records we created
        for r in Record.objects.all():
            self.records.append(r)

        # Create a test carenet on a record
        carenet_args = {'name': 'test_carenet', 'record': self.records[0]}
        self.carenets.append(self.createCarenet(**carenet_args))

        # Create another account to share our records
        acct_args['email'] = EMAIL2
        self.accounts.append(self.createAccount(USER2, PASSWORD, [], **acct_args))
        
        # Add the account to the test carenet
        self.addAccountToCarenet(self.accounts[0], self.carenets[0])

        # Add a third account that doesn't share anything yet
        acct_args['email'] = EMAIL3
        self.accounts.append(self.createAccount(USER3, PASSWORD, [], **acct_args))

        # Create a pha
        pha_args = {'name' : 'myApp',
                    'email' : 'myApp@my.com',
                    'consumer_key' : 'myapp',
                    'secret' : 'myapp',
                    'has_ui' : True,
                    'frameable' : True,
                    'is_autonomous' : False,
                    'autonomous_reason' : '',
                    'start_url_template' : 'http://myapp.com/start',
                    'callback_url' : 'http://myapp.com/afterauth',
                    'description' : 'ITS MY APP',
                    }
        self.phas.append(self.createPHA(**pha_args))

        # Add the pha to the test carenet
        self.addAppToCarenet(self.phas[0], self.carenets[0])

        # Create another pha that doesn't share anything yet
        pha_args['name'] = 'myApp2'
        pha_args['email'] = 'myApp2@my.com'
        pha_args['consumer_key'] = 'myapp2'
        pha_args['secret'] = 'myapp2'
        self.phas.append(self.createPHA(**pha_args))

        # But share it with the record so we can add it to carenets easily
        self.addAppToRecord(record=self.records[0], with_pha=self.phas[1])

        #Create a record-specific doc
        md = hashlib.sha256()
        md.update(DOCUMENT)
        doc_args = {'record':self.records[0],
                    'content':DOCUMENT,
                    'size':len(DOCUMENT),
                    'digest': md.hexdigest(),
                    'label': DOC_LABEL, 
                    'creator': self.accounts[0]}
        self.docs.append(self.createDocument(**doc_args))

        # Add it to a carenet
        self.addDocToCarenet(self.docs[0], self.carenets[0])

        #Create another record-specific doc that isn't shared yet
        md.update(DOCUMENT2)
        doc_args = {'record':self.records[0],
                    'content':DOCUMENT2,
                    'size':len(DOCUMENT2),
                    'digest': md.hexdigest(),
                    'label': DOC_LABEL, 
                    'creator': self.accounts[0]}
        self.docs.append(self.createDocument(**doc_args))

        # Set up our record's sepcial docs and add them to our carenet
        md.update(CONTACT)
        doc_args = {'record':self.records[0],
                    'content':CONTACT,
                    'size':len(CONTACT),
                    'digest': md.hexdigest(),
                    'label': DOC_LABEL, 
                    'creator': self.accounts[0]}
        contact = self.createDocument(**doc_args)

        md.update(DEMOGRAPHICS)
        doc_args = {'record':self.records[0],
                    'content':DEMOGRAPHICS,
                    'size':len(DEMOGRAPHICS),
                    'digest': md.hexdigest(),
                    'label': DOC_LABEL, 
                    'creator': self.accounts[0]}
        demographics = self.createDocument(**doc_args)
        
        self.records[0].demographics = demographics
        self.records[0].contact = contact
        self.records[0].save()

        self.addDocToCarenet(demographics, self.carenets[0])
        self.addDocToCarenet(contact, self.carenets[0])

    def tearDown(self):
        super(CarenetInternalTests,self).tearDown()

    def test_delete_carenet(self):
        c_id = self.carenets[0].id
        url = '/carenets/%s'%(c_id)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)

    def test_rename_carenet(self):
        c_id = self.carenets[0].id
        url = '/carenets/%s/rename'%(c_id)
        data = {'name': CARENET_NAME}
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_remove_account_from_carenet(self):
        c_id = self.carenets[0].id
        a_id = self.accounts[0].email
        url = '/carenets/%s/accounts/%s'%(c_id, a_id)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)

    def test_get_account_permissions_in_carenet(self):
        c_id = self.carenets[0].id
        a_id = self.accounts[0].email
        url = '/carenets/%s/accounts/%s/permissions'%(c_id, a_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_list_carenet_accounts(self):
        c_id = self.carenets[0].id
        url = '/carenets/%s/accounts/'%(c_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_add_account_to_carenet(self):
        c_id = self.carenets[0].id
        url = '/carenets/%s/accounts/'%(c_id)
        data = {'account_id': self.accounts[1].email, 'write':'true'}
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_list_carenet_apps(self):
        c_id = self.carenets[0].id
        url = '/carenets/%s/apps/'%(c_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
       
    def test_get_carenet_app_permissions(self):
        c_id = self.carenets[0].id
        app_id = self.phas[0].email
        url = '/carenets/%s/apps/%s/permissions'%(c_id, app_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_add_app_to_carenet(self):
        c_id = self.carenets[0].id
        app_id = self.phas[1].email
        url = '/carenets/%s/apps/%s'%(c_id, app_id)
        response = self.client.put(url)
        self.assertEquals(response.status_code, 200)
        
    def test_remove_app_from_carenet(self):
        c_id = self.carenets[0].id
        app_id = self.phas[0].email
        url = '/carenets/%s/apps/%s'%(c_id, app_id)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_record(self):
        c_id = self.carenets[0].id
        url = '/carenets/%s/record'%(c_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_list_carenet_documents(self):
        c_id = self.carenets[0].id
        url = '/carenets/%s/documents/'%(c_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_document(self):
        c_id = self.carenets[0].id
        d_id = self.docs[0].id
        url = '/carenets/%s/documents/%s'%(c_id, d_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_document_meta(self):
        c_id = self.carenets[0].id
        d_id = self.docs[0].id
        url = '/carenets/%s/documents/%s/meta'%(c_id, d_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_special_document(self):
        c_id = self.carenets[0].id
        for doc_type, doc in SPECIAL_DOCS.iteritems():
            url = '/carenets/%s/documents/special/%s'%(c_id, doc_type)
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)

    # ADD REPORTS FOR ALL CALLS            
    def test_get_carenet_allergies(self):
        c_id = self.carenets[0].id
        url = '/carenets/%s/reports/minimal/allergies/'%(c_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_equipment(self):
        c_id = self.carenets[0].id
        url = '/carenets/%s/reports/minimal/equipment/'%(c_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_immunizations(self):
        c_id = self.carenets[0].id
        url = '/carenets/%s/reports/minimal/immunizations/'%(c_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_measurements(self):
        c_id = self.carenets[0].id
        lab_code = LAB_CODE
        url = '/carenets/%s/reports/minimal/measurements/%s/'%(c_id, lab_code)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_medications(self):
        c_id = self.carenets[0].id
        url = '/carenets/%s/reports/minimal/medications/'%(c_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_problems(self):
        c_id = self.carenets[0].id
        url = '/carenets/%s/reports/minimal/problems/'%(c_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_procedures(self):
        c_id = self.carenets[0].id
        url = '/carenets/%s/reports/minimal/procedures/'%(c_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_vitals(self):
        c_id = self.carenets[0].id
        url = '/carenets/%s/reports/minimal/vitals/'%(c_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_vitals_by_category(self):
        # NOT IMPLEMENTED YET
        pass
