import django.test
from indivo.models import *
from internal_tests import InternalTests
from django.utils.http import urlencode

EMAIL, FULLNAME, CONTACT_EMAIL, USERNAME, PASSWORD, RECORDS, PRIMARY_SECRET, SECONDARY_SECRET = ("mymail@mail.ma","full name","contact@con.con","user","pass",("the mom", "the dad", "the son", "the daughter"), '010101', '010101')
MESSAGE_ID, MESSAGE_SEVERITY, MESSAGE_SUBJ, MESSAGE_TYPE, MESSAGE_BODY = ('message_id', 'low', 'subj', 'plaintext', 'message body')

class AccountInternalTests(InternalTests):  

    def setUp(self):
        super(AccountInternalTests,self).setUp()

        # create account
        acct_args = {'email':EMAIL, 'full_name':FULLNAME, 'contact_email':CONTACT_EMAIL, 'primary_secret':PRIMARY_SECRET, 'secondary_secret':SECONDARY_SECRET}
        self.accounts = self.createAccount(USERNAME, PASSWORD, RECORDS, **acct_args)

        # create message
        message_args = {'id':MESSAGE_ID, \
                            'account':self.accounts, \
                            'sender':self.accounts, \
                            'about_record':self.accounts.default_record, \
                            'recipient':self.accounts, \
                            'severity':MESSAGE_SEVERITY, \
                            'subject':MESSAGE_SUBJ, \
                            'body_type':MESSAGE_TYPE, \
                            'body':MESSAGE_BODY}        
        self.message = self.createMessage(**message_args)                                    
    
    def tearDown(self):
        super(AccountInternalTests,self).tearDown()

    def test_forgot_password(self):
        response = self.client.get("/accounts/forgot-password?contact_email=%s"%(CONTACT_EMAIL))
        self.assertEquals(response.status_code, 200)

    def test_create_accounts(self):
        email = "mymail2@mail.ma"
        response = self.client.post('/accounts/', urlencode({'account_id' : email,'full_name':'fl','contact_email':'contactemail','password':'pass','primary_secret_p':'primaryp','secondary_secret_p':'secondaryp'}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)        
        
    def test_change_password(self):
        response = self.client.post('/accounts/%s/authsystems/password/change'%(EMAIL), urlencode({'old':PASSWORD,'new':"newpassword"}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)
        
    def test_set_password(self): 
        response = self.client.post('/accounts/%s/authsystems/password/set'%(EMAIL), urlencode({'password':'newpassword'}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_set_username(self):
        response = self.client.post('/accounts/%s/authsystems/password/set-username'%(EMAIL), urlencode({'username':'newusername'}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_add_authsystem_to_accnt(self):
        response = self.client.post('/accounts/%s/authsystems/password/set'%(EMAIL), urlencode({'username':'someuser','password':'somepassword','system':'mychildrens'}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)        

    def test_check_secret(self):
        response = self.client.get('/accounts/%s/check-secrets/%s?secondary_secret=%s'%(EMAIL,PRIMARY_SECRET,SECONDARY_SECRET))
        self.assertEquals(response.status_code, 200)

    def test_get_accountinfo(self):
        response = self.client.get('/accounts/%s'%(EMAIL))
        self.assertEquals(response.status_code, 200)    


    def test_add_archive(self):    
        response = self.client.post('/accounts/%s/inbox/%s/archive'%(EMAIL,MESSAGE_ID))
        self.assertEquals(response.status_code, 200)        

    def test_add_attachment(self):
        attachment_num = 0
        self.message.add_attachment(attachment_num, '<?xml version="1.0" ?><body></body>')
        response = self.client.post('/accounts/%s/inbox/%s/attachments/%s/accept'%(EMAIL,MESSAGE_ID,attachment_num))
        self.assertEquals(response.status_code, 200)

    def test_get_message(self):
        response = self.client.get('/accounts/%s/inbox/%s'%(EMAIL,MESSAGE_ID))
        self.assertEquals(response.status_code, 200)    

    def test_get_inbox(self):
        response = self.client.get('/accounts/%s/inbox/'%(EMAIL))
        self.assertEquals(response.status_code, 200)    

    def test_send_message_to_account(self):
        response = self.client.post('/accounts/%s/inbox/'%(EMAIL), urlencode({'message_id':MESSAGE_ID,'body':MESSAGE_BODY,'severity':MESSAGE_SEVERITY}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_update_account_info(self):
        response = self.client.post('/accounts/%s/info-set'%(EMAIL), urlencode({'contact_email':CONTACT_EMAIL,'full_name':FULLNAME}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_init_account(self):
        NEW_EMAIL = 'someemail@another.com'
        acct_args = {'email':NEW_EMAIL, 'full_name':'new name', 'contact_email':'new@email.com', 'primary_secret':PRIMARY_SECRET, 'secondary_secret':SECONDARY_SECRET}
        account = self.createUninitializedAccount(RECORDS, **acct_args)
        url = '/accounts/%s/initialize/%s'%(NEW_EMAIL,PRIMARY_SECRET)
        response = self.client.post(url, urlencode({'secondary_secret':SECONDARY_SECRET}), 'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_get_notifications(self):
        response = self.client.get('/accounts/%s/notifications/'%(EMAIL))
        self.assertEquals(response.status_code, 200)    
        
    def test_get_permissions(self):
        response = self.client.get('/accounts/%s/permissions/'%(EMAIL))
        self.assertEquals(response.status_code, 200)

    def test_get_primary_secret(self):
        response = self.client.get('/accounts/%s/primary-secret'%(EMAIL))
        self.assertEquals(response.status_code, 200)

    def test_get_records(self):
        response = self.client.get('/accounts/%s/records/?status=active'%(EMAIL))
        self.assertEquals(response.status_code, 200)

    def test_account_reset(self):
        response = self.client.get('/accounts/%s/reset'%(EMAIL))
        self.assertEquals(response.status_code, 200)

    def test_get_secret(self):
        response = self.client.get('/accounts/%s/secret'%(EMAIL))
        self.assertEquals(response.status_code, 200)

    def test_resend_secret(self):
        response = self.client.get('/accounts/%s/secret-resend'%(EMAIL))
        self.assertEquals(response.status_code, 200)

    def test_set_account_state(self):
        response = self.client.post('/accounts/%s/set-state'%(EMAIL), urlencode({'state':'active'}), 'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_search(self):
        response = self.client.get('/accounts/search?fullname=%s&contact_email=%s'%(FULLNAME,EMAIL))
        self.assertEquals(response.status_code, 200)
        
        
