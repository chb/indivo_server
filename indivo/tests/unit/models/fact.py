from django.conf import settings
from indivo.tests.internal_tests import InternalTests
from indivo.models import Fact
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.document import TEST_R_DOCS
from indivo.fields import CodedValueField
from django.db import models

class FactModelUnitTests(InternalTests):
    def setUp(self):
        super(FactModelUnitTests, self).setUp()

        # A record
        self.record = self.createRecord(TEST_RECORDS, 0)
        
        # A doc
        self.doc = self.createDocument(TEST_R_DOCS, 0, record=self.record)

    def tearDown(self):
        super(FactModelUnitTests, self).tearDown()
        
    def test_construction(self):
        args = {
            'document':self.doc,
            'record':self.record,
            }

        # Should be able to construct normally
        try:
            f_obj = Fact(**args)
        except:
            self.fail('Unable to construct Fact with standard args')

        # id should have been created
        self.assertTrue(hasattr(f_obj, 'id'))
        
    def test_metaclass(self):
        fact_subclass_attrs = {
            '__module__': 'tmp.models',
            'not_coded': models.IntegerField(),
            'coded': CodedValueField(),
            }
        
        # generate a subclass of fact
        FactSubclass = type("FactSubclass", (Fact,), fact_subclass_attrs)

        # Since 'coded' was a CodedValueField, we should see nine new fields on the subclass
        valid_fields = {
            'fact_ptr': models.OneToOneField, # pointer to the parent class
            'not_coded': models.IntegerField, # original integer field, preserved
            'coded_code_identifier': models.CharField, # New fields substituted for the DummyField
            'coded_code_system': models.CharField,
            'coded_code_title': models.CharField,
            'coded_title': models.CharField,
            'coded_provenance_source_code': models.CharField,
            'coded_provenance_title': models.CharField,
            'coded_provenance_translation_fidelity': models.CharField,
            }
        self.assertEqual(len(valid_fields.keys()), len(FactSubclass._meta.local_fields))
        for field in FactSubclass._meta.local_fields:
            self.assertTrue(valid_fields.has_key(field.name))
            self.assertTrue(isinstance(field, valid_fields[field.name]))

    def test_uri(self):
        args = {'record':self.record}
        instance = Fact(**args)
        instance.save() # because we'll need the fact to have an id
        
        # URI should have 'facts' in it by default
        self.assertEqual(instance.uri(), settings.SITE_URL_PREFIX + "/records/%s/facts/%s"%(self.record.id, instance.id))

        # But we can override it
        self.assertEqual(instance.uri('medications'), settings.SITE_URL_PREFIX + "/records/%s/medications/%s"%(self.record.id, instance.id))
                         
