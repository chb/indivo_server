from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.models import PHA
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.app import TEST_USERAPPS, TEST_AUTONOMOUS_APPS
from indivo.tests.data.account import TEST_ACCOUNTS

from django.db import IntegrityError, transaction

class PHAModelUnitTests(InternalTests):
    def setUp(self):
        super(PHAModelUnitTests, self).setUp()

        # A userapp
        self.app = self.createUserApp(TEST_USERAPPS, 0)

        # An account
        self.account = self.createAccount(TEST_ACCOUNTS, 0)

        # A record, and one of its builtin carenets
        self.record = self.createRecord(TEST_RECORDS, 0, owner=self.account)
        self.carenet = self.record.carenet_set.all()[0]
        
    def tearDown(self):
        super(PHAModelUnitTests, self).tearDown()
     
    @enable_transactions
    def test_construction(self):

        # Should be able to construct normally, autonomous or not
        try:
            a = self.createUserApp(TEST_USERAPPS, 1)
        except:
            self.fail('Unable to construct UserApp with standard args')
        else:
            self.assertEqual(a, PHA.objects.get(pk=a.pk))

        try:
            a2 = self.createUserApp(TEST_AUTONOMOUS_APPS, 0)
        except:
            self.fail('Unable to construct Autonomous UserApp with standard args')
        else:
            sid = transaction.savepoint()
            self.assertEqual(a2, PHA.objects.get(pk=a2.pk))

        # Should not be able to construct two apps with same email
        try:
            a3 = self.createUserApp(TEST_USERAPPS, 1, force_create=True)
        except:
            transaction.savepoint_rollback(sid)
        else:
            self.fail('Constructed two UserApps with the same email')

        # Even if one is autonomous
        try:
            overrides = {'is_autonomous':True}
            a4 = self.createUserApp(TEST_USERAPPS, 1, force_create=True, **overrides)
        except:
            transaction.rollback()
        else:
            self.fail('Constructed a UserApp and an AutonomousUserApp with the same email')

    def test_accesscontrol(self):
        
        # test isInCarenet
        self.assertFalse(self.app.isInCarenet(self.carenet))
        
        # add it to the carenet
        self.addAppToCarenet(self.app, self.carenet)
        
        # re-assert
        self.assertTrue(self.app.isInCarenet(self.carenet))
