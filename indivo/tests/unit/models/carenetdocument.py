from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.tests.data.document import TEST_R_DOCS
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.carenet import TEST_CARENETS
from indivo.models import CarenetDocument
from django.db import IntegrityError, transaction

class CarenetDocumentModelUnitTests(InternalTests):
    def setUp(self):
        super(CarenetDocumentModelUnitTests, self).setUp()

        # A record
        self.record = self.createRecord(TEST_RECORDS, 0)

        # A document for the record
        self.doc = self.createDocument(TEST_R_DOCS, 0, record=self.record)

        # A carenet
        self.carenet = self.createCarenet(TEST_CARENETS, 0)

    def tearDown(self):
        super(CarenetDocumentModelUnitTests, self).tearDown()

    @enable_transactions
    def test_construction(self):

        # should construct normally
        try:
            cd = self.addDocToCarenet(self.doc, self.carenet)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not create CarenetDocument normally')
        else:
            sid = transaction.savepoint()
            self.assertEqual(cd, CarenetDocument.objects.get(pk=cd.pk))

        # shouldn't be able to share the same document with the same carenet twice
        try:
            cd = self.addDocToCarenet(self.doc, self.carenet)
        except IntegrityError:
            transaction.savepoint_rollback(sid)
        else:
            self.fail('Added the same document to the same carenet twice')

        # Especially with the share_p flags flipped
        try:
            cd = self.addDocToCarenet(self.doc, self.carenet, share_p=False)
        except IntegrityError:
            transaction.rollback()
        else:
            self.fail('Added the same document to the same carenet twice, once with share_p False')
