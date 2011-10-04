import django.test
from indivo.models import *
from indivo.tests.internal_tests import InternalTests
from indivo.tests.data.account import TEST_ACCOUNTS
from indivo.tests.data.app import TEST_USERAPPS
from indivo.tests.data.document import TEST_R_DOCS, TEST_CONTACTS, TEST_DEMOGRAPHICS, SPECIAL_DOCS
from indivo.tests.data.carenet import TEST_CARENETS
from django.utils.http import urlencode
import hashlib

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
        self.createAccount(TEST_ACCOUNTS[4])

        # Track the records we created
        for r in Record.objects.all():
            self.records.append(r)

        # Create a test carenet on a record
        self.carenets.append(self.createCarenet(TEST_CARENETS[0], record=self.records[0]))

        # Create another account to share our records
        self.accounts.append(self.createAccount(TEST_ACCOUNTS[0]))
        
        # Add the account to the test carenet
        self.addAccountToCarenet(self.accounts[0], self.carenets[0])

        # Add a third account that doesn't share anything yet
        self.accounts.append(self.createAccount(TEST_ACCOUNTS[1]))

        # Create a pha
        self.phas.append(self.createUserApp(TEST_USERAPPS[0]))

        # Add the pha to the test carenet
        self.addAppToCarenet(self.phas[0], self.carenets[0])

        # Create another pha that doesn't share anything yet
        self.phas.append(self.createUserApp(TEST_USERAPPS[1]))

        # But share it with the record so we can add it to carenets easily
        self.addAppToRecord(record=self.records[0], with_pha=self.phas[1])

        #Create a record-specific doc
        self.docs.append(self.createDocument(TEST_R_DOCS[6], record=self.records[0]))

        # Add it to a carenet
        self.addDocToCarenet(self.docs[0], self.carenets[0])

        #Create another record-specific doc that isn't shared yet
        self.docs.append(self.createDocument(TEST_R_DOCS[7], record=self.records[0]))

        # Set up our record's sepcial docs and add them to our carenet
        contact = self.createDocument(TEST_CONTACTS[0], record=self.records[0])
        demographics = self.createDocument(TEST_DEMOGRAPHICS[0], record=self.records[0])
        
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
        for doc_type in SPECIAL_DOCS.keys():
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
