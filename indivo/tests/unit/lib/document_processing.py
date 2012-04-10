import sys
from StringIO import StringIO
from lxml import etree
from indivo.models import *
from indivo.tests.data import TEST_DOCUMENT_PROCESSING_DOCS, TEST_SDMJ_SCHEMAS
from indivo.lib.simpledatamodel import SDMJSchema
from indivo.tests.internal_tests import TransactionInternalTests
from indivo.document_processing import *
from indivo.document_processing.document_processing import *


class DocumentProcessingUnitTests(TransactionInternalTests):
    def setUp(self):
        super(DocumentProcessingUnitTests, self).setUp()
        self.required_classes = []
        
        # Make sure the test class is in indivo.models, so we can find it
        indivo_models_module = sys.modules['indivo.models']
        model_definition = open(os.path.join(settings.APP_HOME, 'indivo/tests/data_models/test/testmodel/model.sdmj')).read()
        klasses = [k for k in SDMJSchema(model_definition).get_output()]
        self.required_classes = self.load_classes(klasses)
        
        # load the test schema
        self.loader = IndivoSchemaLoader(os.path.join(settings.APP_HOME, 'indivo/tests/schemas/test'))
        self.loader.import_schemas()        
        
        # create instance from a TestMed document
        self.instance = DocumentProcessing(TEST_DOCUMENT_PROCESSING_DOCS[0], 'application/xml')

    def tearDown(self):
        self.instance = None
        
        self.loader.unregister_all_schemas()
        
        # Unregister the classes, reset the DB
        self.unload_classes(self.required_classes)
        self.required_classes = []

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
        klassCount = {}        
        for klass in self.required_classes:
            klassCount[klass.__name__] = 0
        
        for fact in transformed_doc:
            if fact.__class__ in self.required_classes:
                klassCount[fact.__class__.__name__] += 1
            else:
                self.fail("unexpected fact %s" % fact.__class__)
        
        self.assertEquals(klassCount['TestMed'], 1)
        self.assertEquals(klassCount['TestPrescription'], 1)
        self.assertEquals(klassCount['TestFill'], 2)
        
    def test_process_p(self):
        self.assertTrue(self.instance.process_p)
        
    def test_validate_p(self):
        self.assertTrue(self.instance.validate_p)