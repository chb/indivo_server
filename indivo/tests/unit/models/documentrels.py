from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.document import TEST_R_DOCS
from indivo.models import DocumentRels, DocumentSchema

from django.db import IntegrityError, transaction

class DocumentRelsModelUnitTests(InternalTests):
    def setUp(self):
        super(DocumentRelsModelUnitTests, self).setUp()

        # A record
        self.record = self.createRecord(TEST_RECORDS, 0)

        # A couple test docs
        self.r_doc1 = self.createDocument(TEST_R_DOCS, 2, record=self.record)
        self.r_doc2 = self.createDocument(TEST_R_DOCS, 10, record=self.record)

        self.relationship = DocumentSchema.objects.get(type=DocumentSchema.expand_rel('annotation'))

    def tearDown(self):
        super(DocumentRelsModelUnitTests, self).tearDown()
        
    @enable_transactions
    def test_construction(self):

        # Should be able to construct normally
        try:
            self.relateDocs(self.r_doc1, self.r_doc2, self.relationship)
        except:
            self.fail('Unable to construct documentrels with standard arguments')

        # But not with missing arguments
        self.assertRaises(ValueError, DocumentRels, 
                          document_0=None, document_1=self.r_doc2, relationship=self.relationship)
        self.assertRaises(ValueError, DocumentRels, 
                          document_0=self.r_doc1, document_1=None, relationship=self.relationship)
        self.assertRaises(ValueError, DocumentRels,
                          document_0=self.r_doc1, document_1=self.r_doc2, relationship=None)
