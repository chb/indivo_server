from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.models import PHA
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.app import TEST_USERAPPS, TEST_AUTONOMOUS_APPS
from indivo.tests.data.app import TEST_SMART_MANIFESTS, TEST_USERAPP_MANIFESTS 
from indivo.tests.data.account import TEST_ACCOUNTS

try:
    from django.utils import simplejson
except ImportError:
    try:
        import simplejson
    except ImportError:
        raise ImportError("Couldn't find an installation of SimpleJSON")

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

    def test_from_manifest(self):    
        all_manifests = TEST_SMART_MANIFESTS + TEST_USERAPP_MANIFESTS
        
        # test that save=False works
        for manifest, credentials in all_manifests:
            num_phas = PHA.objects.count()
            app = PHA.from_manifest(manifest, credentials, save=False)
            self.assertEqual(num_phas, PHA.objects.count())
            
        # should work with a SMART manifest
        for manifest, credentials in TEST_SMART_MANIFESTS:
            parsed_m, parsed_c, app = self.buildAppFromManifest(PHA, manifest, credentials)
            self.assertValidUserAppManifest(parsed_m, parsed_c, app)

        # Or with Indivo-specific manifest extensions
        for manifest, credentials in TEST_USERAPP_MANIFESTS:
            parsed_m, parsed_c, app = self.buildAppFromManifest(PHA, manifest, credentials)
            self.assertValidUserAppManifest(parsed_m, parsed_c, app)

    def test_to_manifest(self):
        for manifest, credentials in TEST_SMART_MANIFESTS:
            app = PHA.from_manifest(manifest, credentials, save=False)
            parsed_m = simplejson.loads(manifest)
            reparsed_m = simplejson.loads(app.to_manifest(smart_only=True))

            # The reparsed manifest should contain AT LEAST as much info as the original
            for k, v in parsed_m.iteritems():
                self.assertEqual(v, reparsed_m.get(k, None))

        for manifest, credentials in TEST_USERAPP_MANIFESTS:
            app = PHA.from_manifest(manifest, credentials, save=False)
            parsed_m = simplejson.loads(manifest)
            reparsed_m = simplejson.loads(app.to_manifest())

            # The reparsed manifest should contain AT LEAST as much info as the original
            for k, v in parsed_m.iteritems():
                self.assertEqual(v, reparsed_m.get(k, None))
            
    def buildAppFromManifest(self, model_cls, manifest, credentials):
        parsed_m = simplejson.loads(manifest)
        parsed_c = simplejson.loads(credentials)
        num_apps = model_cls.objects.count()
        app = model_cls.from_manifest(manifest, credentials)
        self.assertEqual(num_apps + 1, model_cls.objects.count())
        return (parsed_m, parsed_c, app)
    
    def assertValidUserAppManifest(self, parsed_m, parsed_c, app):
        self.assertEqual(parsed_c['consumer_key'], app.consumer_key)
        self.assertEqual(parsed_c['consumer_secret'], app.secret)
        self.assertEqual(parsed_m['name'], app.name)
        self.assertEqual(parsed_m['id'], app.email)
        self.assertEqual(parsed_m.get('index', ''), app.start_url_template)
        self.assertEqual(parsed_m.get('oauth_callback_url',''), app.callback_url) # SMART apps won't define this
        autonomous_p = parsed_m.get('mode', '') == 'background'
        self.assertEqual(autonomous_p, app.is_autonomous)
        self.assertEqual(parsed_m.get('autonomous_reason', ''), app.autonomous_reason) # SMART apps won't define this
        has_ui_p = parsed_m['has_ui'] if parsed_m.has_key('has_ui') else parsed_m.has_key('index')
        self.assertEqual(has_ui_p, app.has_ui)
        frameable_p = parsed_m['frameable'] if parsed_m.has_key('frameable') else parsed_m.has_key('index')
        self.assertEqual(frameable_p, app.frameable)
        self.assertEqual(parsed_m.get('description', ''), app.description)
        self.assertEqual(parsed_m.get('author', ''), app.author)
        self.assertEqual(parsed_m.get('version', ''), app.version)
        self.assertEqual(parsed_m.get('icon', ''), app.icon_url)
        self.assertEqual(parsed_m.get('requires', {}), simplejson.loads(app.requirements))
