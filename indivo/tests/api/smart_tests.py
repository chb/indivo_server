from indivo.tests.internal_tests import InternalTests

class SMARTInternalTests(InternalTests):
    def setUp(self):
        super(SMARTInternalTests, self).setUp()

    def tearDown(self):
        super(SMARTInternalTests, self).tearDown()

    def test_get_smart_ontology(self):
        response = self.client.get('/ontology')
        self.assertEqual(response.status_code, 200)
