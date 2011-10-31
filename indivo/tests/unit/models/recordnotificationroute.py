from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.tests.data.account import TEST_ACCOUNTS
from indivo.tests.data.record import TEST_RECORDS
from indivo.models import RecordNotificationRoute
from django.db import IntegrityError, transaction

class RecordNotificationRouteModelUnitTests(InternalTests):
    def setUp(self):
        super(RecordNotificationRouteModelUnitTests,self).setUp()
        
        # An account
        self.account = self.createAccount(TEST_ACCOUNTS, 1)
        
        # A record for that account
        self.record = self.createRecord(TEST_RECORDS, 1, owner=self.account)

        # A notifiable account
        self.n_account = self.createAccount(TEST_ACCOUNTS, 2)

        # And its record
        self.n_record = self.createRecord(TEST_RECORDS, 1, owner=self.n_account)

    def tearDown(self):
        super(RecordNotificationRouteModelUnitTests,self).tearDown()

    @enable_transactions
    def test_construction(self):
        
        # should construct normally
        args = {'record':self.n_record,
                'account':self.account}
        try:
            rnr = RecordNotificationRoute.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not create RecordNotificationRoute normally')
        else:
            self.assertEqual(rnr, RecordNotificationRoute.objects.get(pk=rnr.pk))
        
        # should fail without a record or an account
        args['record'] = None
        self.assertRaises(ValueError, RecordNotificationRoute.objects.create, **args)
        
        args['account'] = None
        args['record'] = self.n_record
        self.assertRaises(ValueError, RecordNotificationRoute.objects.create, **args)
 
        # should fail on an attempt to create two notification routes from a single record to the same account
        args['account'] = self.account
        try:
            rnr = RecordNotificationRoute.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
        else:
            self.fail('Created two RecordNotificationRoutes between the same record and account')
