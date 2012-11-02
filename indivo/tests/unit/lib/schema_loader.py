from indivo.tests.internal_tests import InternalTests
from indivo.document_processing import IndivoSchemaDir, IndivoSchemaLoader

from django.conf import settings

import os

NS = 'http://indivo.org/vocab/xml/documents#'

VALID_CORE_SCHEMAS = {
    'equipment': NS+'Equipment',
    }

INVALID_CORE_SCHEMAS = (
    'demographics',
    )

class IndivoSchemaDirUnitTests(InternalTests):
    
    def setUp(self):
        super(IndivoSchemaDirUnitTests, self).setUp()

        # A valid directory
        self.valid_instance = IndivoSchemaDir(os.path.join(settings.CONTRIB_SCHEMA_DIRS[0], 'valid'))

        # A valid directory with a python transform
        self.valid_instance_py = IndivoSchemaDir(os.path.join(settings.CONTRIB_SCHEMA_DIRS[0], 'valid_py'))

        # An invalid directory having a schema but no transform
        self.invalid_instance_schema = IndivoSchemaDir(os.path.join(settings.CORE_SCHEMA_DIRS[0], 'demographics'))

        # An invalid directory having neither a schema nor a transform
        self.invalid_instance_empty = IndivoSchemaDir(os.path.join(settings.CONTRIB_SCHEMA_DIRS[0], 'bad_dir'))

    def test_construction(self):

        # Test that our objects got instantiated correctly
        self.assertEqual(self.valid_instance.schema_filename, 'schema')
        self.assertEqual(self.valid_instance.schema_ext, '.xsd')
        self.assertEqual(self.valid_instance.transform_filename, 'transform')
        self.assertEqual(self.valid_instance.transform_ext, '.xsl')

        self.assertEqual(self.valid_instance_py.schema_filename, 'schema')
        self.assertEqual(self.valid_instance_py.schema_ext, '.xsd')
        self.assertEqual(self.valid_instance_py.transform_filename, 'transform')
        self.assertEqual(self.valid_instance_py.transform_ext, '.py')
        
        self.assertEqual(self.invalid_instance_schema.schema_filename, 'schema')
        self.assertEqual(self.invalid_instance_schema.schema_ext, '.xsd')
        self.assertEqual(self.invalid_instance_schema.transform_filename, None)
        self.assertEqual(self.invalid_instance_schema.transform_ext, None)

        self.assertEqual(self.invalid_instance_empty.schema_filename, None)
        self.assertEqual(self.invalid_instance_empty.schema_ext, None)
        self.assertEqual(self.invalid_instance_empty.transform_filename, None)
        self.assertEqual(self.invalid_instance_empty.transform_ext, None)
        
    def test_is_valid(self):
        self.assertTrue(self.valid_instance.is_valid())
        self.assertTrue(self.valid_instance_py.is_valid())
        self.assertFalse(self.invalid_instance_schema.is_valid())
        self.assertFalse(self.invalid_instance_empty.is_valid())

    def test_get_full_schema_path(self):
        schema_path = os.path.join(settings.CONTRIB_SCHEMA_DIRS[0], 'valid/schema.xsd')
        self.assertEqual(self.valid_instance.get_full_schema_path(), schema_path)

        schema_path = os.path.join(settings.CONTRIB_SCHEMA_DIRS[0], 'valid_py/schema.xsd')
        self.assertEqual(self.valid_instance_py.get_full_schema_path(), schema_path)
        
        schema_path = os.path.join(settings.CORE_SCHEMA_DIRS[0], 'demographics/schema.xsd')
        self.assertEqual(self.invalid_instance_schema.get_full_schema_path(), schema_path)

        self.assertEqual(self.invalid_instance_empty.get_full_schema_path(), None)
    
    def test_get_full_transform_path(self):
        transform_path = os.path.join(settings.CONTRIB_SCHEMA_DIRS[0], 'valid/transform.xsl')
        self.assertEqual(self.valid_instance.get_full_transform_path(), transform_path)

        transform_path = os.path.join(settings.CONTRIB_SCHEMA_DIRS[0], 'valid_py/transform.py')
        self.assertEqual(self.valid_instance_py.get_full_transform_path(), transform_path)
        
        self.assertEqual(self.invalid_instance_schema.get_full_transform_path(), None)

        self.assertEqual(self.invalid_instance_empty.get_full_transform_path(), None)

class SchemaLoaderUnitTests(InternalTests):
    def setUp(self):
        super(SchemaLoaderUnitTests, self).setUp()
        self.loader = IndivoSchemaLoader(settings.CORE_SCHEMA_DIRS[0])

    def test_detect_schema_dir(self):
        
        # Make sure we can detect all of the core schemas
        for dirname in VALID_CORE_SCHEMAS.keys():
            schema_dir = IndivoSchemaLoader.detect_schema_dir(os.path.join(settings.CORE_SCHEMA_DIRS[0], dirname))
            self.assertTrue(schema_dir.is_valid())

        # Make sure the core schemas without transforms (demographics, etc.) don't show up
        # as valid document processing schemas
        for dirname in INVALID_CORE_SCHEMAS:
            schema_dir = IndivoSchemaLoader.detect_schema_dir(os.path.join(settings.CORE_SCHEMA_DIRS[0], dirname))
            self.assertFalse(schema_dir.is_valid())

        # Make sure our empty directory isn't a valid schema directory
        bad_dir = os.path.join(settings.CONTRIB_SCHEMA_DIRS[0], 'bad_dir')
        self.assertFalse(IndivoSchemaLoader.detect_schema_dir(bad_dir).is_valid())

    def test_discover_schema_dirs(self):
        
        # Make sure we got all the right schema directories
        schema_dirs = dict([(fqn, (validation_func, transformation_func))
                            for fqn, validation_func, transformation_func in self.loader.discover_schema_dirs()])
        self.assertEqual(set(schema_dirs.keys()), set(VALID_CORE_SCHEMAS.values()))    
