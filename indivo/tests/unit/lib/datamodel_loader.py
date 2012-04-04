from indivo.tests.internal_tests import InternalTests
from indivo.data_models import IndivoDataModelLoader, MODULE_NAME, MODULE_EXTENSIONS
from indivo.models import Fact

from django.conf import settings

import sys, os

TEST_MODULE = sys.modules[__name__]

CORE_MODELS = (
    'Allergy',
    'Equipment',
    'Immunization',
    'Lab',
    'Measurement',
    'Medication',
    'Problem',
    'Procedure',
    'SimpleClinicalNote',
    'Vitals',
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
    'simple_clinical_note',
    'vitals',
    )

CONTRIB_MODELS = (
    'TestMed',
    'TestPrescription',
    'TestFill',
    )

CONTRIB_DIRS = (
    'testmodel',
    )

INVALID_CONTRIB_DIRS = (
    'badmodel',
)

class DataModelLoaderUnitTests(InternalTests):
    def setUp(self):
        super(DataModelLoaderUnitTests, self).setUp()
        self.core_loader = IndivoDataModelLoader(settings.CORE_DATAMODEL_DIRS[0])
        self.contrib_loader = IndivoDataModelLoader(settings.CONTRIB_DATAMODEL_DIRS[0])

    def test_import_data_models(self):
        
        # get the core modules, and make sure we imported them all
        self.core_loader.import_data_models(TEST_MODULE)
        self.assertModuleContains(TEST_MODULE, CORE_MODELS)

        # get the contrib modules, and make sure we imported them all
        self.contrib_loader.import_data_models(TEST_MODULE)
        self.assertModuleContains(TEST_MODULE, CONTRIB_MODELS)

    def test_detect_model_dir(self):
        
        # Make sure we can detect all of our valid model dirs
        # Note: the problem model has an sdmj definition, so we're testing python and sdmj here
        for model_dir in CORE_DIRS:
            dir_path = os.path.join(settings.CORE_DATAMODEL_DIRS[0], model_dir)
            valid_p, module_name, ext = IndivoDataModelLoader.detect_model_dir(dir_path)
            self.assertTrue(valid_p)
            self.assertEqual(module_name, MODULE_NAME)
            self.assertTrue(ext in MODULE_EXTENSIONS)

        for model_dir in CONTRIB_DIRS:
            dir_path = os.path.join(settings.CONTRIB_DATAMODEL_DIRS[0], model_dir)
            valid_p, module_name, ext = IndivoDataModelLoader.detect_model_dir(dir_path)
            self.assertTrue(valid_p)
            self.assertEqual(module_name, MODULE_NAME)
            self.assertTrue(ext in MODULE_EXTENSIONS)
            
        # Make sure we can detect an invalid dir
        for model_dir in INVALID_CONTRIB_DIRS:
            dir_path = os.path.join(settings.CONTRIB_DATAMODEL_DIRS[0], model_dir)
            valid_p, module_name, ext = IndivoDataModelLoader.detect_model_dir(dir_path)
            self.assertFalse(valid_p)
            self.assertEqual(module_name, None)
            self.assertEqual(ext, None)

    def test_discover_data_models(self):
        
        # Make sure we got all the core datamodels, and they are all Fact subclasses
        core_models = dict([(name, cls) for name, cls in self.core_loader.discover_data_models()])
        self.assertEqual(set(core_models.keys()), set(CORE_MODELS))
        for cls in core_models.values():
            self.assertTrue(issubclass(cls, Fact))

        # Make sure we got all the contrib datamodels, and they are all Fact subclasses
        contrib_models = dict([(name, cls) for name, cls in self.contrib_loader.discover_data_models()])
        self.assertEqual(set(contrib_models.keys()), set(CONTRIB_MODELS))
        for cls in contrib_models.values():
            self.assertTrue(issubclass(cls, Fact))

    def assertModuleContains(self, module, member_list):
        self.assertNotRaises(ImportError, __import__, module, fromlist=member_list)
                
    
        
