from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.tests.data.account import TEST_ACCOUNTS
from indivo.tests.data.record import TEST_RECORDS
from indivo.models.accounts import UNINITIALIZED, ACTIVE, DISABLED, RETIRED
from indivo.models import Record, AccountAuthSystem, Account
from django.db import IntegrityError, transaction
import string

class AccountModelUnitTests(InternalTests):
    def setUp(self):
        super(AccountModelUnitTests,self).setUp()
        
        # An Account
        self.account = self.createAccount(TEST_ACCOUNTS, 1)
        
        # A record for that account
        self.record = self.createRecord(TEST_RECORDS, 1, owner=self.account)

        # An uninitialized account
        self.u_account = self.createUninitializedAccount(TEST_ACCOUNTS, 2)

        # And its record
        self.u_record = self.createRecord(TEST_RECORDS, 1, owner=self.u_account)

        # A fully shared record
        self.fs_record = self.createRecord(TEST_RECORDS, 5) # owned by TEST_ACCOUNTS[0] by default
        self.shareRecordFull(self.fs_record, self.account)

    def tearDown(self):
        super(AccountModelUnitTests,self).tearDown()

    @enable_transactions
    def test_construction(self):
        test_account_list = TEST_ACCOUNTS
        test_account_index = 3
        
        # should fail without a fullname
        overrides = {'fullname':None}
        try:
            self.createTestItem(test_account_list, test_account_index, overrides)
        except IntegrityError:
            transaction.rollback()
        else:
            self.fail('Created Account with no full_name')
        
        # should fail without a contact_email
        overrides = {'contact_email': None}
        try:
            self.createTestItem(test_account_list, test_account_index, overrides)
        except IntegrityError:
            transaction.rollback()
        else:
            self.fail('Created Account with no contact_email')
 
        # should save normally with proper data            
        try:
            a = self.createTestItem(test_account_list, test_account_index)
        except IntegrityError as e:
            transaction.rollback()
            self.fail(str(e))
        
        # Make sure it saved to the DB properly
        self.assertEqual(a, Account.objects.get(pk=a.pk))

    def test_retired(self):
        self.account.set_state("retired")
        self.assertRaises(Exception, lambda: self.account.set_state("active"))

    def test_password(self):
        
        # Can't set a username on uninitialized account
        self.assertRaises(Exception, lambda: self.u_account.set_username(username='foobar'))

        # Set up the account
        self.u_account.set_username_and_password(username='foobar', password='baz')

        # make sure it worked
        pw_info = self.u_account.password_info
        self.assertTrue(isinstance(pw_info, AccountAuthSystem))
        self.assertEqual(pw_info.username, 'foobar')
        self.assertTrue(self.u_account.password_check('baz'))
        self.assertFalse(self.u_account.password_check('foob'))

        # now we should be able to set the username
        self.u_account.set_username(username='foobar2')
        self.assertEqual(self.u_account.password_info.username, 'foobar2')

    def test_failed_login(self):

        # we start out active
        self.assertEqual(self.account.state, ACTIVE)

        # login
        self.account.on_successful_login()
        self.assertEqual(self.account.total_login_count, 1)
        self.assertEqual(self.account.failed_login_count, 0)
        
        # typo
        self.account.on_failed_login()
        self.assertEqual(self.account.total_login_count, 1)
        self.assertEqual(self.account.failed_login_count, 1)

        # typo
        self.account.on_failed_login()
        self.assertEqual(self.account.total_login_count, 1)
        self.assertEqual(self.account.failed_login_count, 2)

        # login: should reset failed count
        self.account.on_successful_login()
        self.assertEqual(self.account.total_login_count, 2)
        self.assertEqual(self.account.failed_login_count, 0)

        # typo: SHOULDN'T DISABLE ACCOUNT
        self.account.on_failed_login()
        self.assertEqual(self.account.total_login_count, 2)
        self.assertEqual(self.account.failed_login_count, 1)
        self.assertNotEqual(self.account.state, DISABLED)

        # typo
        self.account.on_failed_login()
        self.assertEqual(self.account.total_login_count, 2)
        self.assertEqual(self.account.failed_login_count, 2)

        # typo: DISABLES ACCOUNT
        self.account.on_failed_login()
        self.assertEqual(self.account.total_login_count, 2)
        self.assertEqual(self.account.failed_login_count, 3)
        self.assertEqual(self.account.state, DISABLED)

        # we're inactive
        self.assertFalse(self.account.is_active)

        # reactivate
        self.account.set_state(ACTIVE)
        self.failed_login_count = 0
        self.account.save()

        # one more login
        self.account.on_successful_login()
        self.assertEqual(self.account.total_login_count, 3)
        self.assertEqual(self.account.failed_login_count, 0)

    def test_generate_secrets(self):
        self.account.primary_secret = None
        self.account.secondary_secret = None
        self.account.generate_secrets()
        
        # Primary secret should be 16 random characters
        self.assertNotEqual(self.account.primary_secret, None)
        self.assertEqual(len(self.account.primary_secret), 16)

        # Secondary secret should be 6 random digits
        self.assertNotEqual(self.account.secondary_secret, None)
        self.assertEqual(len(self.account.secondary_secret), 6)
        for digit in self.account.secondary_secret:
            self.assertTrue(digit in string.digits)

    def test_save(self):
        '''Account save should force emails to lowercase.'''
        self.account.email = 'miXedCase@mc.coM'
        self.account.save()
        self.assertEqual(self.account.email, 'mixedcase@mc.com')
    
    def test_accesscontrol(self):
        ''' Make sure all of the roles work appropriately '''
        
        # test ownsRecord
        owned_rs = Record.objects.filter(owner=self.account)
        for r in owned_rs:
            self.assertTrue(self.account.ownsRecord(r))

        unowned_rs = Record.objects.exclude(owner=self.account)
        for r in unowned_rs:
            self.assertFalse(self.account.ownsRecord(r))

        # test fullySharesRecord
        self.assertTrue(self.account.fullySharesRecord(self.fs_record)) 
        self.assertFalse(self.account.fullySharesRecord(self.record)) # not fully shared, because we own it
        self.assertFalse(self.account.fullySharesRecord(self.u_record)) # not fully shared because it hasn't been shared

        # test isInCarenet
        self.assertFalse(self.account.isInCarenet(self.u_record.carenet_set.all()[0])) # not added yet
        self.addAccountToCarenet(self.account, self.u_record.carenet_set.all()[0])
        self.assertTrue(self.account.isInCarenet(self.u_record.carenet_set.all()[0])) # now we've added it
        self.assertFalse(self.account.isInCarenet(self.u_record.carenet_set.all()[1])) # but not to a different carenet
    
    def test_disable(self):
        self.assertEqual(self.account.state, ACTIVE)
        self.account.disable()
        self.assertEqual(self.account.state, DISABLED)

    def test_send_secret(self):
        pass # ideally, we should set up a test mail_server to look at emails...

    def test_notify_account_of_new_message(self):
        pass # ideally, we should set up a test mail_server to look at emails...

    def send_welcome_email(self):
        pass # ideally, we should set up a test mail_server to look at emails...
        
    def test_records_administered(self):
        self.assertEqual(list(self.account.records_administered.all()), list(Record.objects.filter(owner=self.account)))
