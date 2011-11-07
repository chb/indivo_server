from indivo.models import *
from indivo.tests.internal_tests import InternalTests, TransactionInternalTests
from indivo.tests.data import *

from django.utils.http import urlencode
import hashlib, uuid

DOCUMENT_TYPE = 'Lab'
AUDIT_FUNC_NAME = 'record_app_specific_document'
CARENET_LABEL = 'New Carenet'
REL = 'annotation'
STATUS = {'status':'void', 'reason':'because I CAN'}
LAB_CODE = 'HBA1C' # MAKE SURE TO ADD THESE MEASUREMENTS


def recordStateSetUp(test_cases_instance):
    _self = test_cases_instance
    super(_self.__class__, _self).setUp()
    
    # reset our state
    _self.ras_docs = []
    _self.rs_docs = []
    
    # Create an Account
    _self.account = _self.createAccount(TEST_ACCOUNTS, 4)
    
    # Create a record for the account
    _self.record = _self.createRecord(TEST_RECORDS, 0, owner=_self.account)

    # Create an App
    _self.pha = _self.createUserApp(TEST_USERAPPS, 0)

    # Add the app to a record
    share_args = {'record': _self.record,
                  'with_pha': _self.pha}
    _self.addAppToRecord(**share_args)

    # Create a record-app-specific doc
    _self.ras_docs.append(_self.createDocument(TEST_RA_DOCS, 0, record=_self.record, pha=_self.pha))

    # Create a record-specific doc
    _self.rs_docs.append(_self.createDocument(TEST_R_DOCS, 6, record = _self.record))

    # Create a record-specific doc with an external id
    _self.rs_docs.append(_self.createDocument(TEST_R_DOCS, 0, record=_self.record))

    # Create a contact and demographics doc
    _self.rs_docs.append(_self.createDocument(TEST_CONTACTS, 0, record=_self.record))

    _self.rs_docs.append(_self.createDocument(TEST_DEMOGRAPHICS, 0, record=_self.record))

    # Set our record's special docs
    _self.record.demographics = _self.rs_docs[3]
    _self.record.contact = _self.rs_docs[2]
    _self.record.save()

    # The message we will send (not yet in the DB)
    _self.message = TEST_MESSAGES[2]

    # An attachment to attach (not yet in the DB)
    _self.attachment = TEST_ATTACHMENTS[0]


class TransactionRecordInternalTests(TransactionInternalTests):

    ras_docs = []
    rs_docs = []

    def setUp(self):
        return recordStateSetUp(self)

    def tearDown(self):
        return super(TransactionRecordInternalTests,self).tearDown()
    
    def test_duplicate_ext_ids(self):

        # Test doc creation w/ duplicate ext_ids
        record_id = self.record.id
        ext_id = TEST_R_DOCS[1]['external_id']
        pha_email = self.pha.email
        url = '/records/%s/documents/external/%s/%s'%(record_id, pha_email, ext_id)
        response = self.client.put(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

        # Try twice with the same ext_id, expect 400
        response = self.client.put(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 400)

        #Test record_send_message w/ duplicate ext_ids
        record_id = self.record.id
        msg = self.message
        data = {'subject':msg['subject'],
                'body':msg['body'],
                'body_type':msg['body_type'],
                'num_attachments':msg['num_attachments'],
                'severity':msg['severity']}

        # Send a message
        url = '/records/%s/inbox/%s'%(record_id, msg['message_id'])
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

        # Attach to the message
        url = '/records/%s/inbox/%s/attachments/%s'%(record_id, msg['message_id'], self.attachment['attachment_num'])
        response = self.client.post(url, data=self.attachment['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

        # Attach again to the same attachment_num, should break
        url = '/records/%s/inbox/%s/attachments/%s'%(record_id, msg['message_id'], self.attachment['attachment_num'])
        response = self.client.post(url, data=self.attachment['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 400)        
        
        # Send message again to the same message_id, should break
        url = '/records/%s/inbox/%s'%(record_id, msg['message_id'])
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 400)


class RecordInternalTests(InternalTests):
    ras_docs = []
    rs_docs = []

    def setUp(self):
        return recordStateSetUp(self)

    def tearDown(self):
        super(RecordInternalTests,self).tearDown()

    def test_create_record_ext(self):
        principal_email = self.account.email
        url='/records/external/%s/%s'%(principal_email, TEST_RECORDS[5]['external_id'])
        response = self.client.put(url, data=TEST_CONTACTS[0]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)
        # Check for label, contact doc, etc.

    def test_create_record(self):
        url = '/records/' 
        response = self.client.post(url, data=TEST_CONTACTS[0]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)
        # Check for label, contact doc, etc.

    def test_list_record_apps(self):
        record_id = self.record.id
        url = '/records/%s/apps/'%(record_id) 
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # Make sure apps are correct!

    def test_get_record_app(self):
        record_id = self.record.id
        pha_email = self.pha.email
        url = '/records/%s/apps/%s'%(record_id, pha_email) 
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # Make sure app is correct!

    def test_delete_record_app(self):
        record_id = self.record.id
        pha_email = self.pha.email
        url = '/records/%s/apps/%s'%(record_id, pha_email) 
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)

    def test_record_app_specific_docs_ext(self):
        # Multiple calls, to avoid having to resolve ext_ids ourselves
        record_id = self.record.id
        pha_email = self.pha.email

        # Create a rec-app specific doc by ext_id, post
        url = '/records/%s/apps/%s/documents/external/%s'%(record_id, pha_email, TEST_RA_DOCS[1]['external_id'])
        response = self.client.post(url, data=TEST_RA_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)
        
        # Create by put (should overwrite doc)
        url = '/records/%s/apps/%s/documents/external/%s'%(record_id, pha_email, TEST_RA_DOCS[1]['external_id'])
        response = self.client.put(url, data=TEST_RA_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

        # Get Meta by ext_id
        url = '/records/%s/apps/%s/documents/external/%s/meta'%(record_id, pha_email, TEST_RA_DOCS[1]['external_id']) 
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # Check for correctness

    def test_get_record_app_specific_doc(self):
        record_id = self.record.id
        pha_email = self.pha.email
        doc_id = self.ras_docs[0].id
        url = '/records/%s/apps/%s/documents/%s'%(record_id, pha_email, doc_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # Check that we got the doc

    def test_delete_record_app_specific_doc(self):
        record_id = self.record.id
        pha_email = self.pha.email
        doc_id = self.ras_docs[0].id
        url = '/records/%s/apps/%s/documents/%s'%(record_id, pha_email, doc_id)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)

    def test_set_record_app_specific_doc_label(self):
        record_id = self.record.id
        pha_email = self.pha.email
        doc_id = self.ras_docs[0].id
        url = '/records/%s/apps/%s/documents/%s/label'%(record_id, pha_email, doc_id)
        response = self.client.put(url, data=TEST_RA_DOCS[0]['label'], content_type='text/plain')
        self.assertEquals(response.status_code, 200)

    def test_get_record_app_specific_doc_meta(self):
        record_id = self.record.id
        pha_email = self.pha.email
        doc_id = self.ras_docs[0].id
        url = '/records/%s/apps/%s/documents/%s/meta'%(record_id, pha_email, doc_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_list_record_app_specific_docs(self):
        record_id = self.record.id
        pha_email = self.pha.email
        url = '/records/%s/apps/%s/documents/'%(record_id, pha_email)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_create_record_app_specific_doc(self):
        record_id = self.record.id
        pha_email = self.pha.email
        url = '/records/%s/apps/%s/documents/'%(record_id, pha_email)
        response = self.client.post(url, data=TEST_RA_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

    def test_setup_record_app(self):
        record_id = self.record.id
        pha_email = self.pha.email
        url = '/records/%s/apps/%s/setup'%(record_id, pha_email)
        response = self.client.post(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)
    
    def test_get_view_function_audit(self):
        # Need to Create Audit Logs
        record_id = self.record.id
        doc_id = self.ras_docs[0].id
        func_name = AUDIT_FUNC_NAME
        url = '/records/%s/audits/documents/%s/functions/%s/'%(record_id, doc_id, func_name)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_document_audit(self):
        # Need to Create Audit logs
        record_id = self.record.id
        doc_id = self.ras_docs[0].id
        url = '/records/%s/audits/documents/%s/'%(record_id, doc_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_record_audit(self):
        # Need to create Audit logs
        record_id = self.record.id
        url = '/records/%s/audits/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_list_all_autoshares(self):
        # Need to create autoshares
        record_id = self.record.id
        url='/records/%s/autoshare/bytype/all'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_list_autoshares_by_type(self):
        #Need to create autoshares
        record_id = self.record.id
        type = DOCUMENT_TYPE
        url = '/records/%s/autoshare/bytype/'%(record_id)
        response = self.client.get(url, data={'type': type})
        self.assertEquals(response.status_code, 200)

    def test_autoshare_create(self):
        record_id = self.record.id
        data = {'type': DOCUMENT_TYPE}
        carenet_id = Carenet.objects.filter(record = self.record)[0].id
        url = '/records/%s/autoshare/carenets/%s/bytype/set'%(record_id, carenet_id)
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_autoshare_delete(self):
        record_id = self.record.id
        data = {'type': DOCUMENT_TYPE}
        carenet_id = Carenet.objects.filter(record = self.record)[0].id
        url = '/records/%s/autoshare/carenets/%s/bytype/unset'%(record_id, carenet_id)
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)
        # CREATE AUTOSHARE TO DELETE

    def test_list_record_carenets(self):
        record_id = self.record.id
        url = '/records/%s/carenets/'%(record_id) 
        response =self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_create_record_carenet(self):
        record_id = self.record.id
        url = '/records/%s/carenets/'%(record_id)
        data = {'name': CARENET_LABEL}
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_set_record_specific_doc_label_ext(self):
        record_id = self.record.id
        ext_id = TEST_R_DOCS[0]['external_id']
        pha_email = self.pha.email
        url= '/records/%s/documents/external/%s/%s/label'%(record_id, pha_email, ext_id)
        response = self.client.put(url, data=TEST_R_DOCS[0]['label'], content_type='text/plain')
        self.assertEquals(response.status_code, 200)

    def test_get_record_specific_doc_meta_ext(self):
        record_id = self.record.id
        ext_id = TEST_R_DOCS[0]['external_id']
        pha_email = self.pha.email
        url = '/records/%s/documents/external/%s/%s/meta'%(record_id, pha_email, ext_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_create_record_specific_doc_ext(self):
        record_id = self.record.id
        ext_id = TEST_R_DOCS[1]['external_id']
        pha_email = self.pha.email
        url = '/records/%s/documents/external/%s/%s'%(record_id, pha_email, ext_id)
        response = self.client.put(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

    def test_relate_existing_record_specific_docs(self):
        record_id = self.record.id
        rel = REL
        doc_id_0 = self.rs_docs[0].id
        doc_id_1 = self.rs_docs[1].id
        url = '/records/%s/documents/%s/rels/%s/%s'%(record_id, doc_id_0, rel, doc_id_1)
        response = self.client.put(url)
        self.assertEquals(response.status_code, 200)

    def test_create_record_specific_doc_by_rel_ext(self):
        record_id = self.record.id
        ext_id = TEST_R_DOCS[1]['external_id']
        rel = REL
        pha_email = self.pha.email
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/rels/%s/external/%s/%s'%(record_id, doc_id, rel, pha_email, ext_id)
        response = self.client.post(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

        # Test put as well, should create new doc
        ext_id = TEST_R_DOCS[2]['external_id']
        url = '/records/%s/documents/%s/rels/%s/external/%s/%s'%(record_id, doc_id, rel, pha_email, ext_id)
        response = self.client.put(url, data=TEST_R_DOCS[2]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

    def test_get_record_specific_docs_by_rel(self):
        record_id = self.record.id
        rel = REL
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/rels/%s/'%(record_id, doc_id, rel)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # CREATE RELS TO LOOK UP

    def test_create_record_specific_doc_by_rel(self):
        record_id = self.record.id
        rel = REL
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/rels/%s/'%(record_id, doc_id, rel)
        response = self.client.post(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)
        
    def test_get_record_specific_doc_carenets(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/carenets/'%(record_id, doc_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # PLACE DOC IN CARENETS

    def test_revert_record_specific_doc_autoshare(self):
        # NOT YET IMPLEMENTED!!        
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        carenet_id = Carenet.objects.filter(record = self.record)[0].id
        url = '/records/%s/documents/%s/carenets/%s/autoshare-revert'%(record_id, doc_id, carenet_id)
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)

    def test_place_record_specific_doc_in_carenet(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        carenet_id = Carenet.objects.filter(record = self.record)[0].id
        url = '/records/%s/documents/%s/carenets/%s'%(record_id, doc_id, carenet_id)
        response = self.client.put(url)
        self.assertEquals(response.status_code, 200)

    def test_remove_record_specific_doc_from_carenet(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        carenet_id = Carenet.objects.filter(record = self.record)[0].id
        url = '/records/%s/documents/%s/carenets/%s'%(record_id, doc_id, carenet_id)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)
        # CODE LOOKS FUNKY--MAKE SURE THIS WORKS FOR REAL

    def test_get_record_specific_doc(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s'%(record_id, doc_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_set_record_specific_doc_label(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/label'%(record_id, doc_id)
        response = self.client.post(url, data=TEST_R_DOCS[1]['label'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)
        
    def test_get_record_specific_doc_meta(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/meta'%(record_id, doc_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_update_record_specific_doc_meta(self):
        # Call does nothing.
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/meta'%(record_id, doc_id)
        response = self.client.put(url)
        self.assertEquals(response.status_code, 200)
        
    def test_set_record_specific_doc_nevershare(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/nevershare'%(record_id, doc_id)
        response = self.client.put(url)
        self.assertEquals(response.status_code, 200)
        
    def test_remove_record_specific_doc_nevershare(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/nevershare'%(record_id, doc_id)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)
        # ADD NEVERSHARE TO REMOVE

    def test_replace_record_specific_doc_ext(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        pha_email = self.pha.email
        ext_id = TEST_R_DOCS[1]['external_id']
        url = '/records/%s/documents/%s/replace/external/%s/%s'%(record_id, doc_id, pha_email, ext_id)
        response = self.client.put(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

    def test_replace_record_specific_doc(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/replace'%(record_id, doc_id)
        response = self.client.post(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)
        
    def test_set_record_specific_doc_status(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/set-status'%(record_id, doc_id)
        response = self.client.post(url, data=urlencode(STATUS), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_get_record_specific_doc_status_history(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/status-history'%(record_id, doc_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # CREATE STATUS HISTORY ON DOC

    def test_get_record_specific_doc_versions(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/versions/'%(record_id, doc_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # CREATE VERSIONS ON DOC

    def test_list_record_specific_docs(self):
        record_id = self.record.id
        url = '/records/%s/documents/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_create_record_specific_doc(self):
        record_id = self.record.id
        url = '/records/%s/documents/'%(record_id)
        response = self.client.post(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

    def test_delete_all_record_specific_docs(self):
        record_id = self.record.id
        url = '/records/%s/documents/'%(record_id)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)

    def test_get_special_doc(self):
        record_id = self.record.id
        for doc_type in SPECIAL_DOCS.keys():
            url = '/records/%s/documents/special/%s'%(record_id, doc_type)
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)

    def test_set_special_doc(self):
        record_id = self.record.id
        for doc_type, doc in SPECIAL_DOCS.iteritems():
            url = '/records/%s/documents/special/%s'%(record_id, doc_type)
            
            # post
            response = self.client.post(url, data=doc, content_type='text/xml')
            self.assertEquals(response.status_code, 200)

            # put, should have same behavior
            response = self.client.post(url, data=doc, content_type='text/xml')
            self.assertEquals(response.status_code, 200)

    def test_get_record_info(self):
        record_id = self.record.id
        url = '/records/%s'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_record_inbox(self):
        record_id = self.record.id
        url = '/records/%s/inbox/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # CREATE MESSAGES FOR INBOX

    def test_record_send_message(self):
        # Test send and attach together to avoid setup
        record_id = self.record.id
        msg = self.message
        data = {'subject':msg['subject'],
                'body':msg['body'],
                'body_type':msg['body_type'],
                'num_attachments':msg['num_attachments'],
                'severity':msg['severity']}

        # Send a message
        url = '/records/%s/inbox/%s'%(record_id, msg['message_id'])
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)
        
        # Attach to the message
        url = '/records/%s/inbox/%s/attachments/%s'%(record_id, msg['message_id'], self.attachment['attachment_num'])
        response = self.client.post(url, data=self.attachment['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

    def test_record_notify(self):
        record_id = self.record.id
        url = '/records/%s/notify'%(record_id)
        data = {'content':TEST_R_DOCS[1]['content'],
                'document_id':self.rs_docs[1].id}
        response =self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_get_record_owner(self):
        record_id = self.record.id
        url = '/records/%s/owner'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_set_record_owner(self):
        record_id = self.record.id
        url = '/records/%s/owner'%(record_id)
        response = self.client.post(url, data=self.pha.email, content_type='text/plain')
        self.assertEquals(response.status_code, 200)
        
        # Test put: should have same behavior
        response = self.client.put(url, data=self.pha.email, content_type='text/plain')
        self.assertEquals(response.status_code, 200)

    def test_reset_record_password(self):
        # records/%s/password_reset ['GET'] 
        # DOES NOTHING... Why does this call exist?
        pass

    def test_get_record_shares(self):
        record_id = self.record.id
        url = '/records/%s/shares/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # CREATE SHARES
        
    def test_add_record_share(self):
        record_id = self.record.id
        url = '/records/%s/shares/'%(record_id)
        data = {'account_id':self.account.email,
                'role_label':'NEW OWNER'}
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_remove_record_share(self):
        record_id = self.record.id
        other_account_id = self.account.email
        url = '/records/%s/shares/%s/delete'%(record_id, other_account_id)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)
        # CREATE SHARES

    def test_get_record_ccr(self):
        record_id = self.record.id
        url = '/records/%s/reports/experimental/ccr'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_allergies(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/allergies/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_equipment(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/equipment/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_immunizations(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/immunizations/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_labs(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/labs/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_measurements(self):
        record_id = self.record.id
        lab_code = LAB_CODE
        url = '/records/%s/reports/minimal/measurements/%s/'%(record_id, lab_code)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_medications(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/medications/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_problems(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/problems/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_procedures(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/procedures/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_simple_clinical_notes(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/simple-clinical-notes/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_vitals(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/vitals/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_vitals_by_category(self):
        # NOT IMPLEMENTED YET
        pass
