import sys
from indivo.lib import iso8601
from indivo.tests.internal_tests import TransactionInternalTests, InternalTests
from indivo.tests.data import TEST_SDML_DOCS, TEST_SDMJ_DOCS, TEST_SDMX_DOCS
from indivo.tests.data import INVALID_TEST_SDML_DOCS, INVALID_TEST_SDMJ_DOCS, INVALID_TEST_SDMX_DOCS
from indivo.lib.simpledatamodel import SDML, SDMJData, SDMXData, SDMException
from django.db import models
from lxml import etree
from StringIO import StringIO

class SDMLUnitTests(InternalTests):
    def setUp(self):
        super(SDMLUnitTests, self).setUp()
        self.instance = SDML(TEST_SDML_DOCS[0])

    def tearDown(self):
        self.remove_model_from_cache('TestMedication2')
        self.remove_model_from_cache('TestPrescription2')
        self.remove_model_from_cache('TestFill2')
        self.instance = None
        super(SDMLUnitTests, self).tearDown()

    def test_get_output(self):
        output_classes = [obj for obj in self.instance.get_output()]
        self.assertEqual(len(output_classes), 3) # Three models in the definition
        
        med_klass = scrip_klass = fill_klass = None
        for klass in output_classes:
            klass_name = klass.__name__
            if klass_name == 'TestMedication2':
                med_klass = klass
            elif klass_name == 'TestPrescription2':
                scrip_klass = klass
            elif klass_name == 'TestFill2':
                fill_klass = klass
            else:
                self.fail('SDML parsing produced an invalid class %s'%klass_name)
                
        if not med_klass:
            self.fail('SDML parsing did not produce a TestMedication2 class')
        if not scrip_klass:
            self.fail('SDML parsing did not produce a TestPrescription2 class')
        if not fill_klass:
            self.fail('SDML parsing did not produce a TestFill2 class')

        # Make sure the testmedication2 class parsed as expected
        med_expected_fields = {
            'name': models.CharField,
            'date_started': models.DateTimeField,
            'date_stopped': models.DateTimeField,
            'brand_name': models.CharField,
            'route': models.CharField,
            }
        self.check_class_fields(med_klass, med_expected_fields)

        # The 'prescription' field should be a OneToOne field, pointing at TestPrescription2
        prescription_field = med_klass._meta.get_field('prescription')
        self.assertTrue(isinstance(prescription_field, models.OneToOneField))
        self.assertEqual(prescription_field.rel.to, scrip_klass)

        # The 'fills' field should be the reverse side of a ForeignKey from TestFill2 to TestMedication2
        fills_field = med_klass.fills
        self.assertTrue(isinstance(fills_field, models.fields.related.ForeignRelatedObjectsDescriptor))
        self.assertEqual(fills_field.related.model, fill_klass)

        # Make sure the testprescription2 class parsed as expected
        scrip_expected_fields = {
            'prescribed_by_name': models.CharField,
            'prescribed_by_institution': models.CharField,
            'prescribed_on': models.DateTimeField,
            'prescribed_stop_on': models.DateTimeField,
            }
        self.check_class_fields(scrip_klass, scrip_expected_fields)

        # The TestPrescription2 model should have a 'testmedication2' field pointing to the Medication class
        # (the reverse link of the OneToOne from the TestMedication2)
        scrip_parent_link = scrip_klass.testmedication2
        self.assertTrue(isinstance(scrip_parent_link, models.fields.related.SingleRelatedObjectDescriptor))
        self.assertEqual(scrip_parent_link.related.model, med_klass)

        # Make sure the testfill2 class parsed as expected
        fill_expected_fields = {
            'date_filled': models.DateField,
            'supply_days': models.FloatField,
            'filled_at_name': models.CharField,
            'code_identifier': models.CharField, # CodedValues should be expanded
            'code_title': models.CharField,
            'code_system': models.CharField,
            'quantity_value': models.CharField, # ValueAndUnit fields should be expanded
            'quantity_unit': models.CharField,
            'pharmacy_ncpdpid': models.CharField, # Pharmacy fields should be expanded
            'pharmacy_org': models.CharField,
            'pharmacy_adr_country': models.CharField, # Address fields should be expanded (recursively, from Pharmacy)
            'pharmacy_adr_city': models.CharField,
            'pharmacy_adr_postalcode': models.CharField,
            'pharmacy_adr_region': models.CharField,
            'pharmacy_adr_street': models.CharField,
            'provider_dea_number': models.CharField, # Provider fields should be expanded
            'provider_ethnicity': models.CharField,
            'provider_npi_number': models.CharField,
            'provider_preferred_language': models.CharField,
            'provider_race': models.CharField,
            'provider_adr_country': models.CharField, # Address fields should be expanded (recursively, from Provider)
            'provider_adr_city': models.CharField,
            'provider_adr_postalcode': models.CharField,
            'provider_adr_region': models.CharField,
            'provider_adr_street': models.CharField,
            'provider_bday': models.DateField,
            'provider_email': models.EmailField,
            'provider_name_family': models.CharField, # Name fields should be expanded (recursively, from Provider)
            'provider_name_given': models.CharField,
            'provider_name_prefix': models.CharField,
            'provider_name_suffix': models.CharField,
            'provider_gender': models.CharField,
            'provider_tel_1_type': models.CharField, # Telephone fields should be expanded (recursively, from Provider)
            'provider_tel_1_number': models.CharField, 
            'provider_tel_1_preferred_p': models.BooleanField,
            'provider_tel_2_type': models.CharField,
            'provider_tel_2_number': models.CharField,
            'provider_tel_2_preferred_p': models.BooleanField,               
            }
        self.check_class_fields(fill_klass, fill_expected_fields)

        # The TestFill2 model should have a ForeignKey field named 'testmedication2' pointing to the Medication class
        fill_parent_link = fill_klass._meta.get_field('testmedication2')
        self.assertTrue(isinstance(fill_parent_link, models.ForeignKey))
        self.assertEqual(fill_parent_link.rel.to, med_klass)

    def test_invalid_schemas(self):
        def cause_exception(doc):
            parser = SDML(doc)
            output = [obj for obj in parser.get_output()]

        for doc in INVALID_TEST_SDML_DOCS:
            self.assertRaises(SDMException, cause_exception, doc)

    def check_class_fields(self, klass, expected_fields):
        for field_name, field_class in expected_fields.iteritems():
            try:
                field = klass._meta.get_field(field_name)
            except FieldDoesNotExist:
                self.fail('SDML parsing did not produce field %s on % class'%(field_name, klass.__name__))
            self.assertTrue(isinstance(field, field_class))
            
class SDMJDataUnitTests(TransactionInternalTests):
    def setUp(self):
        super(SDMJDataUnitTests, self).setUp()
        self.instance = SDMJData(TEST_SDMJ_DOCS[0])
        self.required_classes = []
        
        # Load test Classes
        self.required_classes = self.load_classes_from_sdml(TEST_SDML_DOCS[0])

    def tearDown(self):
        self.instance = None

        # Unregister the classes, reset the DB
        self.unload_classes(self.required_classes)
        self.required_classes = []

        super(SDMJDataUnitTests, self).tearDown()        

    def test_get_output(self):
        output_objects = [obj for obj in self.instance.get_output()]
        self.assertEqual(len(output_objects), 4) # Three models in the definition
    
        med_obj = scrip_obj = None
        fill_objs = []
        for obj in output_objects:
            klass_name = obj.__class__.__name__
            if klass_name == 'TestMedication2':
                med_obj = obj
            elif klass_name == 'TestPrescription2':
                scrip_obj = obj
            elif klass_name == 'TestFill2':
                fill_objs.append(obj)
            else:
                self.fail('SDMJ Document parsing produced aniinstance of an invalid class %s'%klass_name)
                
        if not med_obj:
            self.fail('SDMJ Document parsing did not produce an instance of TestMedication2')
        if not scrip_obj:
            self.fail('SDMJ Document parsing did not produce an instance of TestPrescription2')
        if not fill_objs or len(fill_objs) != 2:
            self.fail('SDMJ Document parsing did not produce two instances of TestFill2')

        # Make sure the testmedication2 object parsed as expected
        med_expected_fields = {
            'name': 'ibuprofen',
            'date_started': iso8601.parse_utc_date('2010-10-01T00:00:00Z'),
            'date_stopped': iso8601.parse_utc_date('2010-10-31T00:00:00Z'),
            'brand_name': 'Advil',
            'route': 'Oral',
            }
        self.check_object_fields(med_obj, med_expected_fields)

        # The 'prescription' field should be a OneToOne field, pointing at the prescription object
        self.assertEqual(med_obj.prescription, scrip_obj)

        # The 'fills' field should be a manager for fills objects
        # We can't test whether they match up because we aren't saving them to the database
        # So currently 'med_obj.fills' will raise a DoesNotExist exception

        # Make sure the testprescription2 class parsed as expected
        scrip_expected_fields = {
            'prescribed_by_name': 'Kenneth D. Mandl',
            'prescribed_by_institution': 'Children\'s Hospital Boston',
            'prescribed_on': iso8601.parse_utc_date('2010-09-30T00:00:00Z'),
            'prescribed_stop_on': iso8601.parse_utc_date('2010-10-31T00:00:00Z'),
            }
        self.check_object_fields(scrip_obj, scrip_expected_fields)

        # The TestPrescription2 object should have a 'testmedication2' field pointing to the Medication class
        # (the reverse link of the OneToOne from the TestMedication2)
        # We can't test this because we aren't saving object to the database.
        # If we were, we should test this with: self.assertEqual(scrip_obj.testmedication2, med_obj)

        # Make sure the testfill2 class parsed as expected
        fill_expected_fields = {
            'supply_days': 15,
            'filled_at_name': 'CVS',
            }
        fill_dates = set([iso8601.parse_utc_date('2010-10-01T00:00:00Z'), 
                          iso8601.parse_utc_date('2010-10-16T00:00:00Z')])
        for fill_obj in fill_objs:
            self.check_object_fields(fill_obj, fill_expected_fields)
            self.assertEqual(fill_obj.testmedication2, med_obj)
        self.assertEqual(set([o.date_filled for o in fill_objs]), fill_dates)

    def test_invalid_schemas(self):
        def cause_exception(doc):
            parser = SDMJData(doc)
            output = [obj for obj in parser.get_output()]

        for doc in INVALID_TEST_SDMJ_DOCS:
            self.assertRaises(SDMException, cause_exception, doc)


    def check_object_fields(self, obj, expected_fields):
        for field_name, expected_val in expected_fields.iteritems():
            actual_val = getattr(obj, field_name, None)
            self.assertEqual(actual_val, expected_val)

class SDMXDataUnitTests(TransactionInternalTests):
    def setUp(self):
        super(SDMXDataUnitTests, self).setUp()
        self.instance = SDMXData(etree.parse(StringIO(TEST_SDMX_DOCS[0])))
        self.required_classes = []
        
        # Load test Classes
        self.required_classes = self.load_classes_from_sdml(TEST_SDML_DOCS[0])

    def tearDown(self):
        self.instance = None

        # Unregister the classes, reset the DB
        self.unload_classes(self.required_classes)
        self.required_classes = []

        super(SDMXDataUnitTests, self).tearDown()        

    def test_get_output(self):
        output_objects = [obj for obj in self.instance.get_output()]
        self.assertEqual(len(output_objects), 4) # Three models in the definition
    
        med_obj = scrip_obj = None
        fill_objs = []
        for obj in output_objects:
            klass_name = obj.__class__.__name__
            if klass_name == 'TestMedication2':
                med_obj = obj
            elif klass_name == 'TestPrescription2':
                scrip_obj = obj
            elif klass_name == 'TestFill2':
                fill_objs.append(obj)
            else:
                self.fail('SDMX Document parsing produced an instance of an invalid class %s'%klass_name)
                
        if not med_obj:
            self.fail('SDMX Document parsing did not produce an instance of TestMedication2')
        if not scrip_obj:
            self.fail('SDMX Document parsing did not produce an instance of TestPrescription2')
        if not fill_objs or len(fill_objs) != 2:
            self.fail('SDMX Document parsing did not produce two instances of TestFill2')

        # Make sure the testmedication2 object parsed as expected
        med_expected_fields = {
            'name': 'ibuprofen',
            'date_started': iso8601.parse_utc_date('2010-10-01T00:00:00Z'),
            'date_stopped': iso8601.parse_utc_date('2010-10-31T00:00:00Z'),
            'brand_name': 'Advil',
            'route': 'Oral',
            }
        self.check_object_fields(med_obj, med_expected_fields)

        # The 'prescription' field should be a OneToOne field, pointing at the prescription object
        self.assertEqual(med_obj.prescription, scrip_obj)

        # The 'fills' field should be a manager for fills objects
        # We can't test whether they match up because we aren't saving them to the database
        # So currently 'med_obj.fills' will raise a DoesNotExist exception

        # Make sure the testprescription2 class parsed as expected
        scrip_expected_fields = {
            'prescribed_by_name': 'Kenneth D. Mandl',
            'prescribed_by_institution': 'Children\'s Hospital Boston',
            'prescribed_on': iso8601.parse_utc_date('2010-09-30T00:00:00Z'),
            'prescribed_stop_on': iso8601.parse_utc_date('2010-10-31T00:00:00Z'),
            }
        self.check_object_fields(scrip_obj, scrip_expected_fields)

        # The TestPrescription2 object should have a 'testmedication2' field pointing to the Medication class
        # (the reverse link of the OneToOne from the TestMedication2)
        # We can't test this because we aren't saving object to the database.
        # If we were, we should test this with: self.assertEqual(scrip_obj.testmedication2, med_obj)

        # Make sure the testfill2 class parsed as expected
        fill_expected_fields = {
            'supply_days': 15,
            'filled_at_name': 'CVS',
            }
        fill_dates = set([iso8601.parse_utc_date('2010-10-01T00:00:00Z'), 
                          iso8601.parse_utc_date('2010-10-16T00:00:00Z')])
        for fill_obj in fill_objs:
            self.check_object_fields(fill_obj, fill_expected_fields)
            self.assertEqual(fill_obj.testmedication2, med_obj)
        self.assertEqual(set([o.date_filled for o in fill_objs]), fill_dates)

    def test_invalid_schemas(self):
        def cause_exception(doc):
            parser = SDMXData(etree.parse(StringIO(doc)))
            output = [obj for obj in parser.get_output()]

        for doc in INVALID_TEST_SDMX_DOCS:
            self.assertRaises(SDMException, cause_exception, doc)

    def check_object_fields(self, obj, expected_fields):
        for field_name, expected_val in expected_fields.iteritems():
            actual_val = getattr(obj, field_name, None)
            self.assertEqual(actual_val, expected_val)

