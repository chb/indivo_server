from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.models import MachineApp
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.app import TEST_ADMINAPPS, TEST_UIAPPS
from indivo.tests.data.app import TEST_ADMINAPP_MANIFESTS, TEST_UIAPP_MANIFESTS
from indivo.tests.data.account import TEST_ACCOUNTS

try:
    from django.utils import simplejson
except ImportError:
    try:
        import simplejson
    except ImportError:
        raise ImportError("Couldn't find an installation of SimpleJSON")

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

    def test_from_manifest(self):
        all_manifests = TEST_ADMINAPP_MANIFESTS + TEST_UIAPP_MANIFESTS

        # test that save=False works
        for manifest, credentials in all_manifests:
            num_phas = MachineApp.objects.count()
            app = MachineApp.from_manifest(manifest, credentials, save=False)
            self.assertEqual(num_phas, MachineApp.objects.count())
                        
        # Should work with admin apps
        for manifest, credentials in TEST_ADMINAPP_MANIFESTS:
            parsed_m, parsed_c, app = self.buildAppFromManifest(MachineApp, manifest, credentials)
            self.assertValidAdminAppManifest(parsed_m, parsed_c, app, ui=False)

        # Or with UI apps
        for manifest, credentials in TEST_UIAPP_MANIFESTS:
            parsed_m, parsed_c, app = self.buildAppFromManifest(MachineApp, manifest, credentials)
            self.assertValidAdminAppManifest(parsed_m, parsed_c, app, ui=True)

    def buildAppFromManifest(self, model_cls, manifest, credentials):
        parsed_m = simplejson.loads(manifest)
        parsed_c = simplejson.loads(credentials)
        num_apps = model_cls.objects.count()
        app = model_cls.from_manifest(manifest, credentials)
        self.assertEqual(num_apps + 1, model_cls.objects.count())
        return (parsed_m, parsed_c, app)

    def assertValidAdminAppManifest(self, parsed_m, parsed_c, app, ui=True):
        self.assertEqual(parsed_c['consumer_key'], app.consumer_key)
        self.assertEqual(parsed_c['consumer_secret'], app.secret)
        self.assertEqual(parsed_m['name'], app.name)
        self.assertEqual(parsed_m['id'], app.email)
        app_type = 'chrome' if ui else 'admin'
        self.assertEqual(app_type, app.app_type)
        self.assertEqual(parsed_m.get('description', ''), app.description)
        self.assertEqual(parsed_m.get('author', ''), app.author)
        self.assertEqual(parsed_m.get('version', ''), app.version)

