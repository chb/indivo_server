from indivo.models import *
from indivo.tests.internal_tests import InternalTests
from indivo.tests.data import *

from django.utils.http import urlencode
import hashlib

LAB_CODE = 'HBA1C' # MAKE SURE TO ADD THESE MEASUREMENTS
CARENET_NAME = 'NEWNAME'

class CarenetInternalTests(InternalTests):

    def setUp(self):
        super(CarenetInternalTests,self).setUp()

        # Create an account which will own the data being shared
        self.shared_account = self.createAccount(TEST_ACCOUNTS, 4)

        # Create a record for the account to share with our other accounts
        self.shared_record = self.createRecord(TEST_RECORDS, 0, owner=self.shared_account)

        # Create a test carenet on the new record
        self.shared_carenet = self.createCarenet(TEST_CARENETS, 0, record=self.shared_record)

        # Create another account to receive the shared data
        self.receiving_account = self.createAccount(TEST_ACCOUNTS, 0)
        
        # Add the account to the test carenet
        self.addAccountToCarenet(self.receiving_account, self.shared_carenet)

        # Add a third account that doesn't share anything yet
        self.unshared_account = self.createAccount(TEST_ACCOUNTS, 1)

        # Create a pha to be shared
        self.shared_pha = self.createUserApp(TEST_USERAPPS, 1)

        # Add the pha to the test carenet
        self.addAppToCarenet(self.shared_pha, self.shared_carenet)

        # Create another pha that doesn't share anything yet
        self.unshared_pha = self.createUserApp(TEST_USERAPPS, 2)

        # But add it to the record so we can add it to carenets easily
        self.addAppToRecord(record=self.shared_record, with_pha=self.unshared_pha)

        #Create a record-specific doc
        self.shared_doc = self.createDocument(TEST_R_DOCS, 6, record=self.shared_record)

        # Share it in our carenet
        self.addDocToCarenet(self.shared_doc, self.shared_carenet)

        #Create another record-specific doc that isn't shared yet
        self.unshared_doc = self.createDocument(TEST_R_DOCS, 7, record=self.shared_record)

        # Set up our record's sepcial docs and add them to our carenet
        contact = self.createDocument(TEST_CONTACTS, 0, record=self.shared_record)
        demographics = self.createDocument(TEST_DEMOGRAPHICS, 0, record=self.shared_record)
        
        self.shared_record.demographics = demographics
        self.shared_record.contact = contact
        self.shared_record.save()

        self.addDocToCarenet(demographics, self.shared_carenet)
        self.addDocToCarenet(contact, self.shared_carenet)

    def tearDown(self):
        super(CarenetInternalTests,self).tearDown()

    def test_delete_carenet(self):
        c_id = self.shared_carenet.id
        url = '/carenets/%s'%(c_id)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)

    def test_rename_carenet(self):
        c_id = self.shared_carenet.id
        url = '/carenets/%s/rename'%(c_id)
        data = {'name': CARENET_NAME}
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_remove_account_from_carenet(self):
        c_id = self.shared_carenet.id
        a_id = self.receiving_account.email
        url = '/carenets/%s/accounts/%s'%(c_id, a_id)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)

    def test_get_account_permissions_in_carenet(self):
        c_id = self.shared_carenet.id
        a_id = self.shared_account.email
        url = '/carenets/%s/accounts/%s/permissions'%(c_id, a_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_list_carenet_accounts(self):
        c_id = self.shared_carenet.id
        url = '/carenets/%s/accounts/'%(c_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_add_account_to_carenet(self):
        c_id = self.shared_carenet.id
        url = '/carenets/%s/accounts/'%(c_id)
        data = {'account_id': self.unshared_account.email, 'write':'true'}
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_list_carenet_apps(self):
        c_id = self.shared_carenet.id
        url = '/carenets/%s/apps/'%(c_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
       
    def test_get_carenet_app_permissions(self):
        c_id = self.shared_carenet.id
        app_id = self.shared_pha.email
        url = '/carenets/%s/apps/%s/permissions'%(c_id, app_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_add_app_to_carenet(self):
        c_id = self.shared_carenet.id
        app_id = self.unshared_pha.email
        url = '/carenets/%s/apps/%s'%(c_id, app_id)
        response = self.client.put(url)
        self.assertEquals(response.status_code, 200)
        
    def test_remove_app_from_carenet(self):
        c_id = self.shared_carenet.id
        app_id = self.shared_pha.email
        url = '/carenets/%s/apps/%s'%(c_id, app_id)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_record(self):
        c_id = self.shared_carenet.id
        url = '/carenets/%s/record'%(c_id)
        
        bad_methods = ['post', 'put','delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_list_carenet_documents(self):
        c_id = self.shared_carenet.id
        url = '/carenets/%s/documents/'%(c_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_document(self):
        c_id = self.shared_carenet.id
        d_id = self.shared_doc.id
        url = '/carenets/%s/documents/%s'%(c_id, d_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_document_meta(self):
        c_id = self.shared_carenet.id
        d_id = self.shared_doc.id
        url = '/carenets/%s/documents/%s/meta'%(c_id, d_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_special_document(self):
        c_id = self.shared_carenet.id
        for doc_type in SPECIAL_DOCS.keys():
            url = '/carenets/%s/documents/special/%s'%(c_id, doc_type)
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)

    # ADD REPORTS FOR ALL CALLS            
    def test_get_carenet_allergies(self):
        c_id = self.shared_carenet.id
        url = '/carenets/%s/reports/minimal/allergies/'%(c_id)

        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_equipment(self):
        c_id = self.shared_carenet.id
        url = '/carenets/%s/reports/minimal/equipment/'%(c_id)

        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_immunizations(self):
        c_id = self.shared_carenet.id
        url = '/carenets/%s/reports/minimal/immunizations/'%(c_id)

        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_measurements(self):
        c_id = self.shared_carenet.id
        lab_code = LAB_CODE
        url = '/carenets/%s/reports/minimal/measurements/%s/'%(c_id, lab_code)

        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_procedures(self):
        c_id = self.shared_carenet.id
        url = '/carenets/%s/reports/minimal/procedures/'%(c_id)

        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_vitals(self):
        c_id = self.shared_carenet.id
        url = '/carenets/%s/reports/minimal/vitals/'%(c_id)

        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_simple_clinical_notes(self):
        c_id = self.shared_carenet.id
        url = '/carenets/%s/reports/minimal/simple-clinical-notes/'%(c_id)

        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_labs(self):
        c_id = self.shared_carenet.id
        url = '/carenets/%s/reports/minimal/labs/'%(c_id)

        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_carenet_vitals_by_category(self):
        # NOT IMPLEMENTED YET
        pass
