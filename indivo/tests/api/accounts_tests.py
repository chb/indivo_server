import django.test
from indivo.models import *
from indivo.tests.internal_tests import InternalTests, TransactionInternalTests
from django.utils.http import urlencode
from indivo.tests.data import *

from lxml import etree
from indivo.lib import iso8601

def accountStateSetUp(test_cases_instance):
    _self = test_cases_instance
    super(_self.__class__, _self).setUp()

    # create an account
    _self.account = _self.createAccount(TEST_ACCOUNTS, 4)

    # create a record for the account
    _self.record = _self.createRecord(TEST_RECORDS, 0, owner=_self.account)

    # create a message, with an attachment
    _self.message = _self.createMessage(TEST_MESSAGES, 2, about_record=_self.record, account=_self.account,
                                        sender=_self.account, recipient=_self.account)
    _self.attachment = _self.createAttachment(TEST_ATTACHMENTS, 0, attachment_num=1, message=_self.message)

class TransactionAccountInternalTests(TransactionInternalTests):
    
    def setUp(self):
        return accountStateSetUp(self)
    
    def tearDown(self):
        super(TransactionAccountInternalTests,self).tearDown()

    def test_duplicate_message_ids(self):
        msg = TEST_MESSAGES[0]
        data = {'message_id': msg['message_id'],
                'body':msg['body'],
                'severity':msg['severity'],
                }

        # Send a message
        response = self.client.post('/accounts/%s/inbox/'%(self.account.email), 
                                    urlencode(data),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

        # Send it again, with the same message_id. Should break
        response = self.client.post('/accounts/%s/inbox/'%(self.account.email), 
                                    urlencode(data),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 400)


class AccountInternalTests(InternalTests):  

    def setUp(self):
        return accountStateSetUp(self)

    def tearDown(self):
        super(AccountInternalTests,self).tearDown()

    def test_forgot_password(self):
        url = '/accounts/%s/forgot-password'%(self.account.email)

        bad_methods = ['get', 'put', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)

    def test_create_accounts(self):
        email = "mymail2@mail.ma"
        response = self.client.post('/accounts/', urlencode({'account_id' : email,'full_name':'fl','contact_email':'contactemail','password':'pass','primary_secret_p':'primaryp','secondary_secret_p':'secondaryp'}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)        
        
    def test_change_password(self):
        response = self.client.post('/accounts/%s/authsystems/password/change'%(self.account.email), urlencode({'old':TEST_ACCOUNTS[4]['password'],'new':"newpassword"}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)
        
    def test_set_password(self): 
        response = self.client.post('/accounts/%s/authsystems/password/set'%(self.account.email), urlencode({'password':'newpassword'}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_set_username(self):
        response = self.client.post('/accounts/%s/authsystems/password/set-username'%(self.account.email), urlencode({'username':'newusername'}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_add_authsystem_to_accnt(self):
        response = self.client.post('/accounts/%s/authsystems/password/set'%(self.account.email), urlencode({'username':'someuser','password':'somepassword','system':'mychildrens'}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)        

    def test_check_secret(self):
        response = self.client.get('/accounts/%s/check-secrets/%s?secondary_secret=%s'%(self.account.email,self.account.primary_secret,self.account.secondary_secret))
        self.assertEquals(response.status_code, 200)

    def test_get_accountinfo(self):
        response = self.client.get('/accounts/%s'%(self.account.email))
        self.assertEquals(response.status_code, 200)    


    def test_add_archive(self):    
        response = self.client.post('/accounts/%s/inbox/%s/archive'%(self.account.email,self.message.id))
        self.assertEquals(response.status_code, 200)        

    def test_accept_attachment(self):
        response = self.client.post('/accounts/%s/inbox/%s/attachments/%s/accept'%(self.account.email,self.message.id,self.attachment.attachment_num))
        self.assertEquals(response.status_code, 200)

    def test_get_message(self):
        response = self.client.get('/accounts/%s/inbox/%s'%(self.account.email,self.message.id))
        self.assertEquals(response.status_code, 200)    

        # Insure that dates are in the proper format
        xml = etree.fromstring(response.content)
        received_at = xml.findtext('received_at')
        self.assertNotRaises(ValueError, self.validateIso8601, received_at)

        read_at = xml.findtext('read_at')
        self.assertNotRaises(ValueError, self.validateIso8601, read_at)

        archived_at = xml.findtext('archived_at')
        self.assertNotRaises(ValueError, self.validateIso8601, archived_at)

        # We should have gotten one attachemnt.
        # Insure that we got didn't get a doc id, as the doc wasn't saved
        attachments = xml.findall('attachment')
        self.assertEqual(len(attachments), 1)
        attachment_doc_id = attachments[0].get('doc_id')
        self.assertEqual(attachment_doc_id, None)

        # Now save the document and try again
        # We should get a doc id
        self.attachment.save_as_document(self.account)
        response = self.client.get('/accounts/%s/inbox/%s'%(self.account.email, self.message.id))
        self.assertEquals(response.status_code, 200)
        xml = etree.fromstring(response.content)
        attachment = xml.find('attachment')
        attachment_doc_id = attachment.get('doc_id')
        self.assertNotEqual(attachment_doc_id, None)

    def test_get_inbox(self):
        response = self.client.get('/accounts/%s/inbox/'%(self.account.email))
        self.assertEquals(response.status_code, 200)    

        # Insure that dates are in the proper format
        messages = etree.fromstring(response.content)
        for message in messages.iterfind('Message'):
            received_at = message.findtext('received_at')
            self.assertNotRaises(ValueError, self.validateIso8601, received_at)

            read_at = message.findtext('read_at')
            self.assertNotRaises(ValueError, self.validateIso8601, read_at)

            archived_at = message.findtext('archived_at')
            self.assertNotRaises(ValueError, self.validateIso8601, archived_at)

    def test_send_message_to_account(self):
        msg = TEST_MESSAGES[0]
        data = {'message_id': msg['message_id'],
                'body':msg['body'],
                'severity':msg['severity'],
                }
        response = self.client.post('/accounts/%s/inbox/'%(self.account.email), urlencode(data),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_update_account_info(self):
        response = self.client.post('/accounts/%s/info-set'%(self.account.email), urlencode({'contact_email':self.account.contact_email,'full_name':self.account.full_name}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_init_account(self):
        new_acct = self.createUninitializedAccount(TEST_ACCOUNTS, 0)
        url = '/accounts/%s/initialize/%s'%(new_acct.email,new_acct.primary_secret)
        response = self.client.post(url, urlencode({'secondary_secret':new_acct.secondary_secret}), 'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_get_notifications(self):
        response = self.client.get('/accounts/%s/notifications/'%(self.account.email))
        self.assertEquals(response.status_code, 200)    

        # Insure that dates are in the proper format
        notifications = etree.fromstring(response.content)
        for n in notifications.iterfind('Notification'):
            received_at = n.findtext('received_at')
            self.assertNotRaises(ValueError, self.validateIso8601, received_at)
        
    def test_get_permissions(self):
        response = self.client.get('/accounts/%s/permissions/'%(self.account.email))
        self.assertEquals(response.status_code, 200)

    def test_get_primary_secret(self):
        response = self.client.get('/accounts/%s/primary-secret'%(self.account.email))
        self.assertEquals(response.status_code, 200)

    def test_get_records(self):
        response = self.client.get('/accounts/%s/records/?status=active'%(self.account.email))
        self.assertEquals(response.status_code, 200)

    def test_account_reset(self):
        url = '/accounts/%s/reset'%(self.account.email)

        bad_methods = ['get', 'put', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)

    def test_get_secret(self):
        response = self.client.get('/accounts/%s/secret'%(self.account.email))
        self.assertEquals(response.status_code, 200)

    def test_resend_secret(self):
        url = '/accounts/%s/secret-resend'%(self.account.email)

        bad_methods = ['get', 'put', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)
        
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)

    def test_set_account_state(self):
        response = self.client.post('/accounts/%s/set-state'%(self.account.email), urlencode({'state':'active'}), 'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_search(self):
        response = self.client.get('/accounts/search?fullname=%s&contact_email=%s'%(self.account.full_name,self.account.email))
        self.assertEquals(response.status_code, 200)
        
        
