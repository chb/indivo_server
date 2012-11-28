from indivo.tests.internal_tests import InternalTests
from indivo.data_models import IndivoDataModelLoader, MODULE_NAME, MODULE_EXTENSIONS
from indivo.models import Fact, Record
from indivo.validators import ExactValueValidator, ValueInSetValidator

from django.core.exceptions import ValidationError
from django.conf import settings

import sys, os

TEST_MODULE = sys.modules[__name__]

CORE_MODELS = (
    'Allergy',
    'AllergyExclusion',
    'Equipment',
    'Encounter',
    'Fill',
    'Immunization',
    'LabResult',
    'Measurement',
    'Medication',
    'Problem',
    'Procedure',
    'ClinicalNote',
    'VitalSigns',
    )

CORE_DIRS = (
    'allergy',
    'equipment',
    'immunization',
    'lab',
    'measurement',
    'medication',
    'problem',
    'procedure',
    'clinical_note',
    'vitals',
    )

TEST_MODELS = (
    'TestMed',
    'TestPrescription',
    'TestFill',
    'TestFill2',
    'TestMedication2',
    'TestPrescription2',
    'TestModelA',
    'TestModelB',
    'TestModelC',
    'TestModelD',
    )

TEST_MODELS_WITH_EXTRAS = (
    'TestMed',
    'TestPrescription',
    'TestFill',
    )

TEST_DIRS = (
    'testmodel',
    )

INVALID_TEST_DIRS = (
    'badmodel',
)

class DataModelLoaderUnitTests(InternalTests):
    def setUp(self):
        super(DataModelLoaderUnitTests, self).setUp()
        self.test_dir = os.path.join(settings.APP_HOME, 'indivo/tests/data_models/test')
        self.test_loader = IndivoDataModelLoader(self.test_dir)

    def tearDown(self):
        super(DataModelLoaderUnitTests,self).tearDown()

    def test_import_data_models(self):
        
        # get the core modules, and make sure we imported them all
        self.assertModuleContains(TEST_MODULE, CORE_MODELS)

        # get the test modules, and make sure we imported them all
        self.test_loader.import_data_models(TEST_MODULE)
        self.assertModuleContains(TEST_MODULE, TEST_MODELS)

        # make sure the serializers were loaded correctly
        for model_name  in TEST_MODELS_WITH_EXTRAS:
            model_cls = getattr(TEST_MODULE, model_name, None)
            rdf_ser = getattr(model_cls, 'to_rdf', None)
            self.assertTrue(rdf_ser)

            # Dummy input to the serializers, which produce dummy output
            rdf_output = rdf_ser(model_cls.objects.none(), 0, Record())
            self.assertTrue(rdf_output.startswith(model_name))
        

        def _find_indivo_validator(validators, validator_class):
            for v in validators:
                if isinstance(v, validator_class):
                    return v

        # make sure the field validators were loaded correctly

        # validator on TestMed.name should accept 'med1', 'med2', or None
        test_med_class = getattr(TEST_MODULE, 'TestMed')
        field = test_med_class._meta.get_field('name')
        validator = _find_indivo_validator(field.validators, ValueInSetValidator)
        self.assertNotRaises(ValidationError, validator, 'med1')
        self.assertNotRaises(ValidationError, validator, 'med2')
        self.assertNotRaises(ValidationError, validator, None)
        self.assertRaises(ValidationError, validator, 'med3')

        # validator on TestFill.supply_days should accept 30
        test_med_class = getattr(TEST_MODULE, 'TestFill')
        field = test_med_class._meta.get_field('supply_days')
        validator = _find_indivo_validator(field.validators, ExactValueValidator)
        self.assertNotRaises(ValidationError, validator, 30)
        self.assertRaises(ValidationError, validator, 29)
        self.assertRaises(ValidationError, validator, '30')
        self.assertRaises(ValidationError, validator, None)

    def test_detect_model_dir(self):
        
        # Make sure we can detect all of our valid model dirs
        # Note: the problem model has an sdml definition, so we're testing python and sdml here
        for model_dir in CORE_DIRS:
            dir_path = os.path.join(settings.CORE_DATAMODEL_DIRS[0], model_dir)
            valid_p, module_name, ext = IndivoDataModelLoader.detect_model_dir(dir_path)
            self.assertTrue(valid_p)
            self.assertEqual(module_name, MODULE_NAME)
            self.assertTrue(ext in MODULE_EXTENSIONS)

        for model_dir in TEST_DIRS:
            dir_path = os.path.join(self.test_dir, model_dir)
            valid_p, module_name, ext = IndivoDataModelLoader.detect_model_dir(dir_path)
            self.assertTrue(valid_p)
            self.assertEqual(module_name, MODULE_NAME)
            self.assertTrue(ext in MODULE_EXTENSIONS)
            
        # Make sure we can detect an invalid dir
        for model_dir in INVALID_TEST_DIRS:
            dir_path = os.path.join(self.test_dir, model_dir)
            valid_p, module_name, ext = IndivoDataModelLoader.detect_model_dir(dir_path)
            self.assertFalse(valid_p)
            self.assertEqual(module_name, None)
            self.assertEqual(ext, None)

    def test_discover_data_models(self):
        
        # Make sure we got all the test datamodels, and they are all Fact subclasses
        test_models = dict([(name, cls) for name, cls in self.test_loader.discover_data_models()])
        self.assertEqual(set(test_models.keys()), set(TEST_MODELS))
        for cls in test_models.values():
            self.assertTrue(issubclass(cls, Fact))

    def assertModuleContains(self, module, member_list):
        self.assertNotRaises(ImportError, __import__, module, fromlist=member_list)
                
    
        
