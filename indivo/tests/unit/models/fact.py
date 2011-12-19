from indivo.tests.internal_tests import InternalTests
from indivo.models import Fact
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.document import TEST_R_DOCS

class FactModelUnitTests(InternalTests):
    def setUp(self):
        super(FactModelUnitTests, self).setUp()

        # A record
        self.record = self.createRecord(TEST_RECORDS, 0)
        
        # A doc
        self.doc = self.createDocument(TEST_R_DOCS, 0, record=self.record)

    def tearDown(self):
        super(FactModelUnitTests, self).tearDown()
        
    def test_construction(self):
        args = {
            'document':self.doc,
            'record':self.record,
            }

        # Should be able to construct normally
        try:
            f_obj = Fact(**args)
        except:
            self.fail('Unable to construct Fact with standard args')

        # id should have been created
        self.assertTrue(hasattr(f_obj, 'id'))
