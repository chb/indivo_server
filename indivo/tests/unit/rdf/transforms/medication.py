from rdflib import Graph

from indivo.models import Medication
from indivo.rdf.transforms.medication import MedicationTransform

from indivo.tests.internal_tests import InternalTests
from indivo.tests.data.rdfxml import SMART_MEDICATION_RDF_XML

class MedicationTransformUnitTests(InternalTests):

    def setUp(self):
        super(MedicationTransformUnitTests, self).setUp()
        self.graph = Graph()
        self.graph.parse(data=SMART_MEDICATION_RDF_XML[0])

    def test_to_facts(self):
        facts = MedicationTransform()(self.graph)

        self.assertIsNotNone(facts)
        self.assertEqual(len(facts), 1)

        for fact in facts:
            self.assertTrue(isinstance(fact, Medication))

