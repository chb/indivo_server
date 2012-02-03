from indivo.tests.internal_tests import InternalTests, TransactionInternalTests
from indivo.tests.data import *
from indivo.lib.sample_data import IndivoDataLoader
from indivo.models import Record, Document
from django.conf import settings
import glob

TEST_SAMPLEDATA_DIR = settings.APP_HOME + '/indivo/tests/data/sample'

def sampleDataSetUp(test_cases_instance):
    _self = test_cases_instance
    super(_self.__class__, _self).setUp()

    # An admin app, to be the 'creator' of our sample data
    _self.creator = _self.createMachineApp(TEST_ADMINAPPS, 0)
    
    # An account, to own our sample record
    _self.account = _self.createAccount(TEST_ACCOUNTS, 4)
    
    # A record, to load our sample data into
    _self.record = _self.createRecord(TEST_RECORDS, 0, owner=_self.account)
    
    # make sure it got no data to begin with
    try:
        c = _self.record.contact
        d = _self.record.demographics
        _self.record.contact = None
        _self.record.demographics = None
        _self.record.save()
        c.delete()
        d.delete()
        _self.assertEqual(Document.objects.filter(record=_self.record).count(), 0)
    except Exception, e:
        pass

    # Use test sample_data
    _self.old_sampledata_dir = settings.SAMPLE_DATA_DIR
    settings.SAMPLE_DATA_DIR = TEST_SAMPLEDATA_DIR

    # Some common test profiles
    _self.normal_profile_dir = settings.SAMPLE_DATA_DIR + '/patient_1'
    _self.no_contact_profile_dir = settings.SAMPLE_DATA_DIR + '/nocontact'
    _self.no_demo_profile_dir = settings.SAMPLE_DATA_DIR + '/nodemo'
    
    # create a loader for use in tests
    _self.loader = IndivoDataLoader(_self.creator)

def sampleDataTearDown(test_cases_instance):
    _self = test_cases_instance
    settings.SAMPLE_DATA_DIR = _self.old_sampledata_dir
    super(_self.__class__, _self).tearDown()

class SampleDataUnitTests(InternalTests):
    def setUp(self):
        sampleDataSetUp(self)

    def tearDown(self):
        sampleDataTearDown(self)

    def test_loader_construction(self):
        
        # class should construct with valid args
        try:
            loader = IndivoDataLoader(self.creator)

        except Exception, e:
            self.fail('Could not create with standard args: %s'%str(e))

        # and with a custom data_dir
        try:
            loader = IndivoDataLoader(self.creator, self.old_sampledata_dir)
        except Exception, e:
            self.fail('Could not create with custom data dir: %s'%str(e))
        else:
            self.assertEqual(loader.data_dir, self.old_sampledata_dir)

    def test_loader_get_named_doc(self):
        
        # pull back data from our test data
        doc = self.loader._get_named_doc(self.normal_profile_dir, 'Contact.xml')
        self.assertTrue(doc)
        with open(self.normal_profile_dir + '/Contact.xml', 'r') as f:
            self.assertEqual(f.read(), doc)

        # try a nonexistent file
        doc2 = self.loader._get_named_doc(self.normal_profile_dir, 'DEADBEEF.xml')
        self.assertEqual(doc2, None)

        # try a nonexistent directory
        doc3 = self.loader._get_named_doc(settings.SAMPLE_DATA_DIR + '/patient_deadbeef/',
                                          'Contact.xml')
        self.assertEquals(doc3, None)

    def test_loader_load_special_docs(self):

        # Initial state
        self.assertEqual(self.record.contact, None)
        self.assertEqual(self.record.demographics, None)

        # Load the docs, but don't save
        self.loader.load_special_docs(self.normal_profile_dir, self.record, save=False)
        
        # State should have changed in memory
        self.assertNotEqual(self.record.contact, None)
        self.assertNotEqual(self.record.demographics, None)

        # But not in the DB
        db_record = Record.objects.get(id=self.record.id)
        self.assertEqual(db_record.contact, None)
        self.assertEqual(db_record.demographics, None)

        # reset
        self.record.contact = None
        self.record.demographics = None

        # Load the docs again, and save this time
        self.loader.load_special_docs(self.normal_profile_dir, self.record)

        # State should have changed in memory
        self.assertNotEqual(self.record.contact, None)
        self.assertNotEqual(self.record.demographics, None)
        
        # AND in the DB
        db_record = Record.objects.get(id=self.record.id)
        self.assertNotEqual(db_record.contact, None)
        self.assertNotEqual(db_record.demographics, None)

        # Now check that the docs got set correctly
        with open(self.normal_profile_dir + '/Contact.xml', 'r') as f:
            contact_raw = f.read()
        self.assertEqual(self.record.contact.content, contact_raw)
                            
        with open(self.normal_profile_dir + '/Demographics.xml', 'r') as f:
            demo_raw = f.read()
        self.assertEqual(self.record.demographics.content, demo_raw)

        # reset
        self.record.contact = None
        self.record.demographics = None

        # Now check that things still work with missing documents
        self.loader.load_special_docs(self.no_contact_profile_dir, self.record)
        self.assertEqual(self.record.contact, None)
        with open(self.no_contact_profile_dir + '/Demographics.xml', 'r') as f:
            demo_raw = f.read()
        self.assertEqual(self.record.demographics.content, demo_raw)

        self.record.contact = None
        self.record.demographics = None

        self.loader.load_special_docs(self.no_demo_profile_dir, self.record)
        self.assertEqual(self.record.demographics, None)
        with open(self.no_demo_profile_dir + '/Contact.xml', 'r') as f:
            contact_raw = f.read()
        self.assertEqual(self.record.contact.content, contact_raw)

    def test_loader_get_all_docs(self):
        # Get the docs
        docs = [doc for doc in self.loader.get_all_docs(self.normal_profile_dir)]

        # Make sure all of the xml docs were fetched
        required_files = glob.glob(self.normal_profile_dir + '/doc_*.xml')
        for filepath in required_files:
            with open(filepath, 'r') as f:
                data = (f.read(), 'application/xml')
            self.assertTrue(data in docs, filepath)
            
        # Make sure the pdf doc was fetched
        with open(self.normal_profile_dir + '/doc_pdf.pdf', 'rb') as f:
            data = (f.read(), 'application/pdf')
        self.assertTrue(data in docs)

        # Make sure none of the special docs were fetched
        with open(self.normal_profile_dir + '/Contact.xml', 'r') as f:
            data = (f.read(), 'application/xml')
        self.assertFalse(data in docs)

        with open(self.normal_profile_dir + '/Demographics.xml', 'r') as f:
            data = (f.read(), 'application/xml')
        self.assertFalse(data in docs)

        # Make sure docs with unknown extensions weren't fetched
        with open(self.normal_profile_dir + '/doc_beef.deadbeef', 'rb') as f:
            data = f.read()
        self.assertFalse(data in [doc[0] for doc in docs])
        

class TransactionSampleDataUnitTests(TransactionInternalTests):
    def setUp(self):
        sampleDataSetUp(self)

    def tearDown(self):
        sampleDataTearDown(self)

    def test_loader_load_profile(self):

        # Try loading an invalid profile
        self.assertRaises(Exception, self.loader.load_profile, 
                          self.record, 'patient_invalid')

        # Make sure we didn't create any documents (transactions worked)
        self.assertEqual(Document.objects.filter(record=self.record).count(), 0)

        db_record = Record.objects.get(id=self.record.id)
        self.assertEqual(db_record.contact, None)
        self.assertEqual(db_record.demographics, None)

        # Now load a valid profile
        self.loader.load_profile(self.record, 'patient_1')
        
        # Make sure our docs got created
        n_docs = len(glob.glob(self.loader.data_dir + '/patient_1/doc_*'))
        n_docs += 2 # Contact/Demographics docs
        n_docs -= 1 # Unknown doctype doc
        self.assertEqual(Document.objects.filter(record=self.record).count(), n_docs)

        # test_loader_load_special_docs tests the content of these
        self.assertNotEqual(self.record.contact, None)
        self.assertNotEqual(self.record.demographics, None) 

