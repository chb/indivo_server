from rdflib import Graph

from indivo.tests.internal_tests import InternalTests
from indivo.rdf.sparql import SMARTSPARQLQuery, SPARQLOptionalBlock
from indivo.tests.data.rdfxml.testmodel import TEST_MODEL_RDF_XML

TEST_MODEL_COUNT = 3

class SMARTSPARQLUnitTests(InternalTests):

    def setUp(self):
        super(SMARTSPARQLUnitTests, self).setUp()
        self.graph = Graph()
        self.graph.parse(data=TEST_MODEL_RDF_XML[0])
        self.query = SMARTSPARQLQuery('TestModel')

    def test_base_query_string(self):
        query_string = self.query.generate_query_string()
        self.assertIsNotNone(query_string)

        # base query should find 3 TestModels
        results = self.graph.query(query_string, initNs=self.query.NS)
        self.assertEqual(len(results), TEST_MODEL_COUNT)

    def test_simple(self):
        expected = ['TEST STRING 1', 'TEST STRING 2', 'TEST STRING 3']
        self.query.add_simple('simpleStringElement')
        query_string = self.query.generate_query_string()

        results = self.graph.query(query_string, initNs=self.query.NS)
        self.assertEqual(len(results), TEST_MODEL_COUNT)

        for row in results:
            self.assertIn(str(row[1]), expected)

    def test_simple_required(self):
        expected = ['optional']
        self.query.add_simple('optionalSimpleStringElement')
        query_string = self.query.generate_query_string()

        results = self.graph.query(query_string, initNs=self.query.NS)
        self.assertEqual(len(results), 1)

        for row in results:
            self.assertIn(str(row[1]), expected)

    def test_simple_optional(self):
        expected = ['None', 'optional']
        self.query.add_simple('optionalSimpleStringElement', optional=True)
        query_string = self.query.generate_query_string()

        results = self.graph.query(query_string, initNs=self.query.NS)
        self.assertEqual(len(results), TEST_MODEL_COUNT)

        for row in results:
            self.assertIn(str(row[1]), expected)


    def test_value_and_unit(self):
        expected_value_and_units = [('1', '{tablet}'),('2', '{tablet}')]

        self.query.add_value_and_unit("quantity")
        query_string = self.query.generate_query_string()
        results = self.graph.query(query_string, initNs=self.query.NS)

        self.assertEqual(len(results), 2)

        for row in results:
            self.assertIn((str(row[1]), str(row[2])), expected_value_and_units)

    def test_value_and_unit_optional(self):
        expected_value_and_units = [('None','None'), ('1', '{tablet}'),('2', '{tablet}')]

        self.query.add_value_and_unit("quantity", optional=True)
        query_string = self.query.generate_query_string()
        results = self.graph.query(query_string, initNs=self.query.NS)

        self.assertEqual(len(results), TEST_MODEL_COUNT)

        for row in results:
            self.assertIn((str(row[1]), str(row[2])), expected_value_and_units)

    def test_coded_value(self):
        expected_values = [('Test Title 1',
                            'Test Title 2',
                            '1',
                            'http://test.org/ontology/TEST/',
                            'Test Title 3',
                            'http://provenance.test.org/ontology/TEST/1',
                            'http://smartplatforms.org/terms/codes/TranslationFidelity#automated'),
                           ('Test Title 4',
                            'Test Title 5',
                            '2',
                            'http://test.org/ontology/TEST/',
                            'Test Title 6',
                            'http://provenance.test.org/ontology/TEST/2',
                            'http://smartplatforms.org/terms/codes/TranslationFidelity#automated'),
        ]

        self.query.add_coded_value("name", "name")
        query_string = self.query.generate_query_string()
        results = self.graph.query(query_string, initNs=self.query.NS)

        self.assertEqual(len(results), 2)

        for row in results:
            self.assertIn((str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]), str(row[7])), expected_values)

    def test_coded_value_optional(self):
        expected_values = [('Test Title 1',
                            'Test Title 2',
                            '1',
                            'http://test.org/ontology/TEST/',
                            'Test Title 3',
                            'http://provenance.test.org/ontology/TEST/1',
                            'http://smartplatforms.org/terms/codes/TranslationFidelity#automated'),
                           ('Test Title 4',
                            'Test Title 5',
                            '2',
                            'http://test.org/ontology/TEST/',
                            'Test Title 6',
                            'http://provenance.test.org/ontology/TEST/2',
                            'http://smartplatforms.org/terms/codes/TranslationFidelity#automated'),
                           ('None',
                            'None',
                            'None',
                            'None',
                            'None',
                            'None',
                            'None'),
                           ]

        self.query.add_coded_value("name", "name", optional=True)
        query_string = self.query.generate_query_string()
        results = self.graph.query(query_string, initNs=self.query.NS)

        self.assertEqual(len(results), TEST_MODEL_COUNT)

        for row in results:
            self.assertIn((str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]), str(row[7])), expected_values)

class SPARQLOptionalBlockUnitTests(InternalTests):

    def test_optional_block_empty(self):
        queries = []
        block = SPARQLOptionalBlock(queries)
        self.assertEqual(block.to_query_string(), '')
