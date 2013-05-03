from rdflib import Graph
from rdflib.exceptions import UniquenessError

from indivo.models import Fill
from indivo.rdf.transforms.medication import FulfillmentTransform
from indivo.lib import iso8601

from indivo.tests.internal_tests import InternalTests
from indivo.tests.data.rdfxml import SMART_FULFILLMENT_RDF_XML, TEST_MODEL_RDF_XML

class FulfillmentTransformUnitTests(InternalTests):

    def setUp(self):
        super(FulfillmentTransformUnitTests, self).setUp()

    def test_to_facts(self):
        graph = Graph()
        graph.parse(data=SMART_FULFILLMENT_RDF_XML[0])
        facts = FulfillmentTransform()(graph)

        comparison_fill = Fill(
            date=iso8601.parse_iso8601_datetime('2010-05-12T04:00:00Z'),
            dispenseDaysSupply='30',
            pbm='T00000000001011',
            pharmacy_adr_city='WonderCity',
            pharmacy_adr_country='Australia',
            pharmacy_adr_postalcode='5555',
            pharmacy_adr_region='test_region',
            pharmacy_adr_street='111 Lake Drive',
            pharmacy_ncpdpid='5235235',
            pharmacy_org='CVS #588',
            provider_adr_city='test_locality',
            provider_adr_country='test_country',
            provider_adr_postalcode='test_postal',
            provider_adr_region='test_region',
            provider_adr_street='test_address',
            provider_bday='1945-01-01',
            provider_dea_number='325555555',
            provider_email='test@stuff.com',
            provider_ethnicity='test_ethnicity',
            provider_gender='male',
            provider_name_family='Mandel',
            provider_name_given='Joshua',
            provider_name_middle='test_additinal_name',
            provider_name_prefix='test_prefix',
            provider_name_suffix='test_suffix',
            provider_npi_number='5235235',
            provider_preferred_language='test_preferred_language',
            provider_race='test_race',
            provider_tel_1_number='555-5555',
            provider_tel_1_preferred_p='',
            provider_tel_1_type='',
            provider_tel_2_number='800-555-1212',
            provider_tel_2_preferred_p='',
            provider_tel_2_type='',
            quantityDispensed_unit='{tablet}',
            quantityDispensed_value='60',
            )
        comparison_fill.save()

        fields_to_check = comparison_fill.filter_fields
        fields_to_check.pop('created_at')
        # There is no ordering on SMART RDF/XML, so we can't test fact.tel_1 == comparison_fill.tel_1
        fields_to_check.pop('provider_tel_1_number')
        fields_to_check.pop('provider_tel_1_preferred_p')
        fields_to_check.pop('provider_tel_1_type')
        fields_to_check.pop('provider_tel_2_number')
        fields_to_check.pop('provider_tel_2_preferred_p')
        fields_to_check.pop('provider_tel_2_type')
        # we can only store a single email
        fields_to_check.pop('provider_email')

        self.assertIsNotNone(facts)
        self.assertEqual(len(facts), 1)

        for fact in facts:
            self.assertTrue(isinstance(fact, Fill))
            for field in fields_to_check.keys():
                actual = getattr(fact, field)
                expected = getattr(comparison_fill, field)
                self.assertEqual(actual, expected, 'field %s does not match expected: %s != %s'%(field, str(actual), str(expected)))

            # test the telephone numbers
            expected_tels = [comparison_fill.provider_tel_1_number, comparison_fill.provider_tel_2_number]
            self.assertIn(fact.provider_tel_1_number, expected_tels)
            self.assertIn(fact.provider_tel_2_number, expected_tels)

            # test email
            expected_emails = [comparison_fill.provider_email, 'other@stuff.com']
            self.assertIn(fact.provider_email, expected_emails)

    def test_to_facts_duplicate_id(self):
        graph = Graph()
        graph.parse(data=SMART_FULFILLMENT_RDF_XML[1])
        self.assertRaises(UniquenessError, FulfillmentTransform(),graph)

    def test_to_facts_no_fills(self):
        graph = Graph()
        graph.parse(data=TEST_MODEL_RDF_XML[0])
        facts = FulfillmentTransform()(graph)

        self.assertIsNone(facts)
