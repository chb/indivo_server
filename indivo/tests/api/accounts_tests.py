import django.test
from indivo.models import *
from indivo.tests.internal_tests import InternalTests
from django.utils.http import urlencode
from indivo.tests.data.account import TEST_ACCOUNTS

MESSAGE_ID, MESSAGE_SEVERITY, MESSAGE_SUBJ, MESSAGE_TYPE, MESSAGE_BODY = ('message_id', 'low', 'subj', 'plaintext', 'message body')

class AccountInternalTests(InternalTests):  

    def setUp(self):
        super(AccountInternalTests,self).setUp()

        # create account
        self.account = self.createAccount(TEST_ACCOUNTS[4])

        # create message
        message_args = {'id':MESSAGE_ID, \
                            'account':self.account, \
                            'sender':self.account, \
                            'about_record':self.account.default_record, \
                            'recipient':self.account, \
                            'severity':MESSAGE_SEVERITY, \
                            'subject':MESSAGE_SUBJ, \
                            'body_type':MESSAGE_TYPE, \
                            'body':MESSAGE_BODY}        
        self.message = self.createMessage(**message_args)                                    
    
    def tearDown(self):
        super(AccountInternalTests,self).tearDown()

    def test_forgot_password(self):
        response = self.client.get("/accounts/forgot-password?contact_email=%s"%(self.account.contact_email))
        self.assertEquals(response.status_code, 200)

    def test_create_accounts(self):
        email = "mymail2@mail.ma"
        response = self.client.post('/accounts/', urlencode({'account_id' : email,'full_name':'fl','contact_email':'contactemail','password':'pass','primary_secret_p':'primaryp','secondary_secret_p':'secondaryp'}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)        
        
    def test_change_password(self):
        response = self.client.post('/accounts/%s/authsystems/password/change'%(self.account.email), urlencode({'old':TEST_ACCOUNTS[4].password,'new':"newpassword"}),'application/x-www-form-urlencoded')
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
        response = self.client.post('/accounts/%s/inbox/%s/archive'%(self.account.email,MESSAGE_ID))
        self.assertEquals(response.status_code, 200)        

    def test_add_attachment(self):
        attachment_num = 0
        self.message.add_attachment(attachment_num, '<?xml version="1.0" ?><body></body>')
        response = self.client.post('/accounts/%s/inbox/%s/attachments/%s/accept'%(self.account.email,MESSAGE_ID,attachment_num))
        self.assertEquals(response.status_code, 200)

    def test_get_message(self):
        response = self.client.get('/accounts/%s/inbox/%s'%(self.account.email,MESSAGE_ID))
        self.assertEquals(response.status_code, 200)    

    def test_get_inbox(self):
        response = self.client.get('/accounts/%s/inbox/'%(self.account.email))
        self.assertEquals(response.status_code, 200)    

    def test_send_message_to_account(self):
        response = self.client.post('/accounts/%s/inbox/'%(self.account.email), urlencode({'message_id':MESSAGE_ID,'body':MESSAGE_BODY,'severity':MESSAGE_SEVERITY}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_update_account_info(self):
        response = self.client.post('/accounts/%s/info-set'%(self.account.email), urlencode({'contact_email':self.account.contact_email,'full_name':self.account.full_name}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_init_account(self):
        new_acct = self.createUninitializedAccount(TEST_ACCOUNTS[0])
        url = '/accounts/%s/initialize/%s'%(new_acct.email,new_acct.primary_secret)
        response = self.client.post(url, urlencode({'secondary_secret':self.account.secondary_secret}), 'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_get_notifications(self):
        response = self.client.get('/accounts/%s/notifications/'%(self.account.email))
        self.assertEquals(response.status_code, 200)    
        
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
        response = self.client.get('/accounts/%s/reset'%(self.account.email))
        self.assertEquals(response.status_code, 200)

    def test_get_secret(self):
        response = self.client.get('/accounts/%s/secret'%(self.account.email))
        self.assertEquals(response.status_code, 200)

    def test_resend_secret(self):
        response = self.client.get('/accounts/%s/secret-resend'%(self.account.email))
        self.assertEquals(response.status_code, 200)

    def test_set_account_state(self):
        response = self.client.post('/accounts/%s/set-state'%(self.account.email), urlencode({'state':'active'}), 'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_search(self):
        response = self.client.get('/accounts/search?fullname=%s&contact_email=%s'%(self.account.full_name,self.account.email))
        self.assertEquals(response.status_code, 200)
        
        
