from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.models import MachineApp
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.app import TEST_ADMINAPPS, TEST_UIAPPS
from indivo.tests.data.account import TEST_ACCOUNTS

from django.db import IntegrityError, transaction

class MachineAppModelUnitTests(InternalTests):
    def setUp(self):
        super(MachineAppModelUnitTests, self).setUp()

        # A machineapp
        self.m_app = self.createMachineApp(TEST_ADMINAPPS, 0)
    
        # A UI app
        self.ui_app = self.createMachineApp(TEST_UIAPPS, 0)

        # An account
        self.account = self.createAccount(TEST_ACCOUNTS, 0)

        # A record
        self.record = self.createRecord(TEST_RECORDS, 0, owner=self.account)
        
    def tearDown(self):
        super(MachineAppModelUnitTests, self).tearDown()
     
    @enable_transactions
    def test_construction(self):

        # Should be able to construct normally, UI or Admin
        try:
            ma = self.createMachineApp(TEST_ADMINAPPS, 1)
        except:
            self.fail('Unable to construct AdminApp with standard args')
        else:
            self.assertEqual(ma, MachineApp.objects.get(pk=ma.pk))

        try:
            ma2 = self.createMachineApp(TEST_UIAPPS, 1)
        except:
            self.fail('Unable to construct UIApp with standard args')
        else:
            sid = transaction.savepoint()
            self.assertEqual(ma2, MachineApp.objects.get(pk=ma2.pk))

        # Should not be able to construct two apps with same email
        try:
            ma3 = self.createMachineApp(TEST_ADMINAPPS, 1, force_create=True)
        except:
            transaction.savepoint_rollback(sid)
        else:
            self.fail('Constructed two AdminApps with the same email')

        # Even if they are different app types
        try:
            overrides = {'app_type':'chrome'}
            ma4 = self.createMachineApp(TEST_ADMINAPPS, 1, force_create=True, **overrides)
        except:
            transaction.rollback()
        else:
            self.fail('Constructed an AdminApp and a ChromeApp with the same email')

    def test_accesscontrol(self):
        
        # test isType
        self.assertTrue(self.m_app.isType('admin'))
        self.assertFalse(self.m_app.isType('chrome'))
        self.assertTrue(self.m_app.isType('MachineApp'))
        
        self.assertTrue(self.ui_app.isType('chrome'))
        self.assertFalse(self.ui_app.isType('admin'))
        self.assertTrue(self.ui_app.isType('MachineApp'))

        # test createdAccount
        self.account.creator = self.m_app
        self.assertTrue(self.m_app.createdAccount(self.account))
        self.assertFalse(self.ui_app.createdAccount(self.account))

        # test createdRecord
        self.record.creator = self.ui_app
        self.assertTrue(self.ui_app.createdRecord(self.record))
        self.assertFalse(self.m_app.createdRecord(self.record))
