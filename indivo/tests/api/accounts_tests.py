from indivo.models import *
from indivo.tests.internal_tests import InternalTests, TransactionInternalTests
from django.utils.http import urlencode
from django.conf import settings
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

    # Create an app, and add it to the record
    _self.pha = _self.createUserApp(TEST_USERAPPS, 0)
    _self.addAppToRecord(record=_self.record, with_pha=_self.pha)

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
        # check invalid email address
        email = "mybadmail2@mail.ma@"
        contact_email = "mymail2@mail.ma"
        response = self.client.post('/accounts/', urlencode({'account_id' : email,'full_name':'fl','contact_email':contact_email,'password':'pass','primary_secret_p':'primaryp','secondary_secret_p':'secondaryp'}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 400)
        
        # check invalid contact email address 
        email = "mymail2@mail.ma"
        contact_email = "mybadmail2"
        response = self.client.post('/accounts/', urlencode({'account_id' : email,'full_name':'fl','contact_email':contact_email,'password':'pass','primary_secret_p':'primaryp','secondary_secret_p':'secondaryp'}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 400)
        
        # valid email and contact addresses
        # Make sure DEMO_MODE = False works as expected
        prev_num_accounts = Account.objects.all().count()
        demo_mode = settings.DEMO_MODE
        settings.DEMO_MODE = False
        contact_email = "mymail2@mail.ma"

        # create an Account, normally: should be no records
        response = self.client.post('/accounts/', urlencode({'account_id' : email,'full_name':'fl','contact_email':contact_email,'password':'pass','primary_secret_p':'primaryp','secondary_secret_p':'secondaryp'}),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)        
        self.assertEqual(Account.objects.all().count(), prev_num_accounts+1)
        new_acct = Account.objects.get(email=email)
        self.assertEqual(list(new_acct.records_owned_by.all()), [])

        settings.DEMO_MODE = demo_mode

    def test_create_accounts_demo_mode(self):
        email = "mymail2@mail.ma"
        prev_num_accounts = Account.objects.all().count()

        # backup demo settings
        demo_mode = settings.DEMO_MODE
        demo_profiles = settings.DEMO_PROFILES
        data_dir = settings.SAMPLE_DATA_DIR

        # activate demo mode
        settings.DEMO_MODE = True
        settings.DEMO_PROFILES = { 'John Doe':'patient_1', 'John Doe 2':'patient_1',}
        settings.SAMPLE_DATA_DIR = settings.APP_HOME + '/indivo/tests/data/sample'

        # create an Account in demo mode: should see some populated records
        response = self.client.post('/accounts/', urlencode({'account_id':email, 'full_name':'fl','contact_email':'contactemail@me.com','password':'pass','primary_secret_p':'1','secondary_secret_p':'1'}), 'application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Account.objects.all().count(), prev_num_accounts+1)
        new_acct = Account.objects.get(email=email)
        recs = new_acct.records_owned_by.all()
        self.assertEqual(recs.count(), 2)
        self.assertEqual(set([r.label for r in recs]), set(['John Doe', 'John Doe 2']))
        for r in recs:
            self.assertNotEqual(Document.objects.filter(record=r).count(), 0)

        # restore demo settings
        settings.DEMO_MODE = demo_mode
        settings.DEMO_PROFILES = demo_profiles
        settings.SAMPLE_DATA_DIR = data_dir
        
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
                'subject':msg['subject'],
                'body':msg['body'],
                'body_type':'markdown',
                'severity':msg['severity'],
                }
        response = self.client.post('/accounts/%s/inbox/'%(self.account.email), urlencode(data),'application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)
        root = etree.XML(response.content)
        # check returned data
        message_id = root.get('id')
        self.assertTrue(message_id is not None and len(message_id) > 0, "Did not find message ID")
        subject = root.find('subject').text
        self.assertEqual(subject, msg['subject'], "subjects do not match")
        severity = root.find('severity').text
        self.assertEqual(severity, msg['severity'], "subjects do not match")

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

    def test_account_search(self):
        url = '/accounts/search?'

        # We should have only our own account in the system
        self.assertEqual(Account.objects.all().count(), 1)

        # Create one more, with customized search fields
        search_account = self.createAccount(TEST_ACCOUNTS, 3, 
                                            fullname='test fullname', 
                                            contact_email='test@contact.com')

        # run a search for the existing account by name
        response = self.client.get(url + 'fullname=%s'%(self.account.full_name))
        self.assertEquals(response.status_code, 200)

        # Make sure the results were as expected
        results = etree.XML(response.content).findall('Account')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get('id'), self.account.email)

        # run a search for the existing account by contact email
        response = self.client.get(url + 'contact_email=%s'%(self.account.contact_email))
        self.assertEquals(response.status_code, 200)

        # Make sure the results were as expected
        results = etree.XML(response.content).findall('Account')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get('id'), self.account.email)
        
        # run a search for the existing account by partial name
        response = self.client.get(url + 'fullname=%s'%(self.account.full_name[:-3]))
        self.assertEquals(response.status_code, 200)

        # Make sure the results were as expected
        results = etree.XML(response.content).findall('Account')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get('id'), self.account.email)

        # run a search for the existing account, passing a bogus contact email
        response = self.client.get(url + 'fullname=%s&contact_email=%s'%(self.account.full_name,
                                                                         'DEADBEEF'))
        self.assertEquals(response.status_code, 200)

        # Make sure the results were as expected
        results = etree.XML(response.content).findall('Account')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get('id'), self.account.email)

        # run a search that should return nothing
        response = self.client.get(url + 'fullname=DEADBEEF&contact_email=DEADBEEF')
        self.assertEqual(response.status_code, 200)
        
        # Check the results
        results = etree.XML(response.content).findall('Account')
        self.assertEqual(len(results), 0)

        # run a search that should return both
        response = self.client.get(url + 'contact_email=contact')
        self.assertEqual(response.status_code, 200)
        
        # Check the results
        results = etree.XML(response.content).findall('Account')
        self.assertEqual(len(results), 2)
        self.assertEqual(set([r.get('id') for r in results]), 
                         set([self.account.email, search_account.email]))
        
    def test_get_connect_credentials(self):

        # Test a valid call
        url = '/accounts/%s/apps/%s/connect_credentials'%(self.account.email, self.pha.email)
        data = {'record_id': self.record.id}
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 200)
        
        data = etree.XML(response.content)
        self.assertEqual(self.pha.email, data.find('App').get('id', None))
        self.assertEqual(settings.SITE_URL_PREFIX, data.findtext('APIBase'))

        ct = data.findtext('ConnectToken')
        cs = data.findtext('ConnectSecret')
        self.assertNotRaises(Exception, AccessToken.objects.get, token=ct, token_secret=cs, connect_auth_p=True)

        rt = data.findtext('RESTToken')
        rs = data.findtext('RESTSecret')
        self.assertNotRaises(Exception, AccessToken.objects.get, token=rt, token_secret=rs, connect_auth_p=False)

        db_rt = AccessToken.objects.get(token=rt)
        self.assertEqual(db_rt.expires_at, iso8601.parse_utc_date(data.findtext('ExpiresAt')))

        # Get a 404 for invalid accounts, apps, and records
        url = '/accounts/%s/apps/%s/connect_credentials'%('BOGUS_ACCOUNT', self.pha.email)
        data = {'record_id': self.record.id}
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 404)

        url = '/accounts/%s/apps/%s/connect_credentials'%(self.account.email, 'BOGUS_APP')
        data = {'record_id': self.record.id}
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 404)

        url = '/accounts/%s/apps/%s/connect_credentials'%(self.account.email, self.pha.email)
        data = {'record_id': 'BOGUS_RECORD'}
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 404)

    def test_get_user_preferences(self):
        url = '/accounts/%s/apps/%s/preferences'%(self.account.email, self.pha.email)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '') # No preferences
    
    def test_set_user_preferences(self):
        url = '/accounts/%s/apps/%s/preferences'%(self.account.email, self.pha.email)
        data = 'MYPREFERENCESDOC'
        response = self.client.put(url, data=data, content_type='text/plain')
        self.assertEqual(response.status_code, 200)

        # check that the preferences doc is in the database
        doc_id = Document.prepare_external_id("%s_USER_PREFERENCES"%self.account.id, 
                                              self.pha, pha_specific=True, record_specific=False)
        self.assertTrue(Document.objects.filter(external_id=doc_id, pha=self.pha).exists())
        self.assertEqual(Document.objects.get(external_id=doc_id, pha=self.pha).content, data)

    def test_delete_user_preferences(self):
        url = '/accounts/%s/apps/%s/preferences'%(self.account.email, self.pha.email)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

        # check that there is no preferences doc in the database
        doc_id = Document.prepare_external_id("%s_USER_PREFERENCES"%self.account.id, 
                                              self.pha, pha_specific=True, record_specific=False)
        self.assertFalse(Document.objects.filter(external_id=doc_id, pha=self.pha).exists())
