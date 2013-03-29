from rdflib import Graph

from indivo.models import Medication, Fill
from indivo.rdf.transforms.medication import MedicationTransform

from indivo.tests.internal_tests import InternalTests
from indivo.tests.data.rdfxml import SMART_MEDICATION_RDF_XML, TEST_MODEL_RDF_XML

class MedicationTransformUnitTests(InternalTests):

    def setUp(self):
        super(MedicationTransformUnitTests, self).setUp()

    def test_to_facts(self):
        graph = Graph()
        graph.parse(data=SMART_MEDICATION_RDF_XML[0])
        facts = MedicationTransform()(graph)

        self.assertIsNotNone(facts)
        self.assertEqual(len(facts), 1)

        comparison_med = Medication(
            endDate='2013-09-18',
            frequency_unit='/d',
            frequency_value='2',
            instructions='TAKE 1 TABLET TWICE DAILY WITH MEALS',
            name_code_identifier='206206',
            name_code_system='http://purl.bioontology.org/ontology/RXNORM/',
            name_code_title='Prevacid 30 MG Enteric Coated Capsule',
            name_provenance_source_code='http://fda.gov/NDC/00300304613',
            name_provenance_title='PREVACID 30 MG CAPSULE',
            name_provenance_translation_fidelity='http://smartplatforms.org/terms/codes/TranslationFidelity#automated',
            name_title='PREVACID 30 MG CAPSULE',
            provenance_identifier='1234',
            provenance_system='ProvenanceSystem',
            provenance_title='ProvenanceTitle',
            quantity_unit='{tablet}',
            quantity_value='2',
            startDate='2013-02-18',
            )
        comparison_med.save()

        fields_to_check = comparison_med.filter_fields
        fields_to_check.pop('created_at')

        for fact in facts:
            self.assertTrue(isinstance(fact, Medication))
            for field in fields_to_check.keys():
                actual = getattr(fact, field)
                expected = getattr(comparison_med, field)
                self.assertEqual(actual, expected, 'field %s does not match expected: %s != %s'%(field, str(actual), str(expected)))

    def test_to_facts_with_fill(self):
        graph = Graph()
        graph.parse(data=SMART_MEDICATION_RDF_XML[1])
        facts = MedicationTransform()(graph)

        self.assertIsNotNone(facts)
        self.assertEqual(len(facts), 2)

        for fact in facts:
            self.assertTrue(isinstance(fact, Medication) or isinstance(fact, Fill))

    def test_to_facts_no_meds(self):
        graph = Graph()
        graph.parse(data=TEST_MODEL_RDF_XML[0])
        facts = MedicationTransform()(graph)

        self.assertIsNone(facts)
