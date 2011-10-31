from indivo.tests.internal_tests import InternalTests
from indivo.models import DocumentStatusHistory, StatusName
from indivo.tests.data.account import TEST_ACCOUNTS
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.document import TEST_R_DOCS

class DocumentStatusHistoryModelUnitTests(InternalTests):
    def setUp(self):
        super(DocumentStatusHistoryModelUnitTests, self).setUp()

        # A status to set
        self.status = StatusName.objects.all()[0]
        
        # A record
        self.record = self.createRecord(TEST_RECORDS, 0)
        
        # A doc
        self.doc = self.createDocument(TEST_R_DOCS, 0, record=self.record)

        # A principal
        self.principal = self.createAccount(TEST_ACCOUNTS, 0)

    def tearDown(self):
        super(DocumentStatusHistoryModelUnitTests, self).tearDown()
        
    def test_construction(self):
        required_args = {
            'status':self.status,
            'reason':'The best reason there is',
            }
        optional_args = {
            'document':self.doc.id,
            'record':self.record.id,
            'proxied_by_principal': self.principal.email,
            'effective_principal':self.principal.email
            }

        # Should be able to construct with no optional args
        try:
            dsh = DocumentStatusHistory(**required_args)
        except:
            self.fail('Unable to construct documentstatushistory with standard arguments')

        # And with all args specified
        required_args.update(optional_args)
        try:
            dsh = DocumentStatusHistory(**required_args)
        except:
            self.fail('Unable to construct documentstatushistory with standard arguments')
