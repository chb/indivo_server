from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.tests.data.account import TEST_ACCOUNTS
from indivo.tests.data.carenet import TEST_CARENETS
from indivo.models import CarenetAccount
from django.db import IntegrityError, transaction

class CarenetAccountModelUnitTests(InternalTests):
    def setUp(self):
        super(CarenetAccountModelUnitTests, self).setUp()

        # An account
        self.account = self.createAccount(TEST_ACCOUNTS, 0)

        # A carenet
        self.carenet = self.createCarenet(TEST_CARENETS, 0)

    def tearDown(self):
        super(CarenetAccountModelUnitTests, self).tearDown()

    @enable_transactions
    def test_construction(self):

        # should construct normally
        try:
            ca = self.addAccountToCarenet(self.account, self.carenet)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not create CarenetAccount normally')
        else:
            sid = transaction.savepoint()
            self.assertEqual(ca, CarenetAccount.objects.get(pk=ca.pk))

        # shouldn't be able to add an account to the same carenet twice
        try:
            ca = self.addAccountToCarenet(self.account, self.carenet)
        except IntegrityError:
            transaction.savepoint_rollback(sid)
        else:
            self.fail('Added an account to the same carenet twice')

        # Even if one is read_only and one isn't
        try:
            ca = self.addAccountToCarenet(self.account, self.carenet, can_write=True)
        except IntegrityError:
            transaction.rollback()
        else:
            self.fail('Added the an account to the same carenet twice, once not read-only')
