from rdflib import Graph

from indivo.rdf.transforms.base import BaseRDFTransform
from indivo.tests.internal_tests import InternalTests
from indivo.tests.data.rdfxml.testmodel import TEST_MODEL_RDF_XML
from indivo.tests.data.rdfxml.medication import SMART_MEDICATION_RDF_XML

class BaseRDFTransformUnitTests(InternalTests):

    def setUp(self):
        super(BaseRDFTransformUnitTests, self).setUp()

    def test_smart_classes_to_params(self):
        self.graph = Graph()
        self.graph.parse(data=SMART_MEDICATION_RDF_XML[0])
        transform = BaseRDFTransform()
        smart_medication_class = transform.smart_class_dictionary['Medication']
        results = transform.smart_classes_to_params(self.graph, smart_medication_class)
        self.assertEqual(len(results), 1)

    def test_smart_classes_to_params_nonexistent(self):
        self.graph = Graph()
        self.graph.parse(data=TEST_MODEL_RDF_XML[0])
        transform = BaseRDFTransform()
        smart_medication_class = transform.smart_class_dictionary['Medication']
        results = transform.smart_classes_to_params(self.graph, smart_medication_class)
        self.assertEqual(len(results), 0)