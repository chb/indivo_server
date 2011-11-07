from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.account import TEST_ACCOUNTS
from indivo.models import AccountFullShare
from django.db import IntegrityError, transaction

class AccountFullShareModelUnitTests(InternalTests):
    def setUp(self):
        super(AccountFullShareModelUnitTests, self).setUp()

        # An account
        self.account = self.createAccount(TEST_ACCOUNTS, 1)

        # A record for the account
        self.record = self.createRecord(TEST_RECORDS, 0, owner=self.account)

        # A recipient account
        self.with_account = self.createAccount(TEST_ACCOUNTS, 2)

    def tearDown(self):
        super(AccountFullShareModelUnitTests, self).tearDown()

    @enable_transactions
    def test_construction(self):

        # Should construct normally
        args = {'record': self.record,
                'with_account': self.with_account,
                'role_label': 'Guardian',
                }
        try:
            afs = AccountFullShare.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not construct account full share')
        else:
            self.assertEqual(afs, AccountFullShare.objects.get(pk=afs.pk))

        # Should break if the same record is shared twice with the same account
        try:
            afs = AccountFullShare.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
        else:
            self.fail('Shared a record with the same account twice')
        
