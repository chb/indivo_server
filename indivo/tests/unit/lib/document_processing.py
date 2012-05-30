import sys
from StringIO import StringIO
from lxml import etree
from indivo.models import *
from indivo.tests.data import TEST_DOCUMENT_PROCESSING_DOCS, TEST_SDML_DOCS
from indivo.tests.internal_tests import TransactionInternalTests
from indivo.document_processing import *
from indivo.document_processing.document_processing import *


class DocumentProcessingUnitTests(TransactionInternalTests):
    def setUp(self):
        super(DocumentProcessingUnitTests, self).setUp()
        
        # Load the test datamodels
        self.load_model_dir(self.TEST_MODEL_DIR)

        # load the test schema
        self.loader = IndivoSchemaLoader(os.path.join(settings.APP_HOME, 'indivo/tests/schemas/test'))
        self.loader.import_schemas()        
        
        # create instance from a TestMed document
        self.instance = DocumentProcessing(TEST_DOCUMENT_PROCESSING_DOCS[0], 'application/xml')

    def tearDown(self):
        self.instance = None
        
        # Unload the test schema
        self.loader.unregister_all_schemas()
        
        # Unregister the classes, reset the DB
        self.unload_model_dir(self.TEST_MODEL_DIR)

        super(DocumentProcessingUnitTests, self).tearDown()     
        
    def test_expand_schemas(self):
        self.assertEquals(self.instance.expand_schema('TestMed'), 'http://indivo.org/vocab/xml/documents#TestMed');
        
    def test_base_name(self):
        self.assertEquals(self.instance.basename, 'TestMed')
        
    def test_fqn(self):
        self.assertEquals(self.instance.fqn, 'http://indivo.org/vocab/xml/documents#TestMed')
        
    def test_xml_syntax_validation(self):
        self.assertNotRaises(ValueError, self.instance.validate_xml_syntax)
        
    def test_xml_validation(self):
        self.assertNotRaises(ValueError, self.instance.validate_xml)
        
    def test_content_etree(self):
        root = self.instance.content_etree
        self.assertFalse(root is None, "content_etree is None")
        self.assertTrue(isinstance(root, etree._ElementTree))
        
    def test_validation_func_existence(self):
        self.assertFalse(self.instance.validation_func is None, "validation_fucn is None")
        
    def test_transform_func_existence(self):
        self.assertFalse(self.instance.transform_func is None, "transform_func is None")
        
    def test_transformed_doc(self):
        transformed_doc = self.instance.transformed_doc
        
        # make sure not empty
        self.assertFalse(transformed_doc is None, "transformed_doc is None")
        
        # should transform to 4 Facts
        self.assertEquals(len(transformed_doc), 4)
        
        # check Class types and count        
        test_classes = ('TestMed', 'TestPrescription', 'TestFill')
        klassCount = dict.fromkeys(test_classes, 0)
        
        for fact in transformed_doc:
            if fact.__class__.__name__ in test_classes:
                klassCount[fact.__class__.__name__] += 1
            else:
                self.fail("unexpected fact %s" % fact.__class__.__name__)
        
        self.assertEquals(klassCount['TestMed'], 1)
        self.assertEquals(klassCount['TestPrescription'], 1)
        self.assertEquals(klassCount['TestFill'], 2)
        
    def test_process_p(self):
        self.assertTrue(self.instance.process_p)
        
    def test_validate_p(self):
        self.assertTrue(self.instance.validate_p)
