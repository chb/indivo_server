from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.demographics import TEST_DEMOGRAPHICS
from indivo.tests.data.document import TEST_R_DOCS
from indivo.tests.data.carenet import TEST_CARENETS
from indivo.models import Carenet
from django.db import IntegrityError, transaction

class CarenetModelUnitTests(InternalTests):
    def setUp(self):
        super(CarenetModelUnitTests, self).setUp()

        # A record for tests that should work, and one for tests that should break
        # test demographics documents are not associated with a record by default, 
        # so we add it in here TODO: better way
        self.good_record = self.createRecord(TEST_RECORDS, 0)
        self.good_record.demographics.document.record = self.good_record
        self.bad_record = self.createRecord(TEST_RECORDS, 1)
        self.bad_record.demographics.document.record = self.bad_record

        # Carenets for each of them
        self.good_carenet = Carenet.objects.filter(record=self.good_record)[0]
        self.bad_carenet = Carenet.objects.filter(record=self.bad_record)[0]

        self.good_doc = self.createDocument(TEST_R_DOCS, 0, record=self.good_record)

    def tearDown(self):
        super(CarenetModelUnitTests, self).tearDown()

    @enable_transactions
    def test_construction(self):

        # should construct normally
        try:
            cn = self.createCarenet(TEST_CARENETS, 0)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not create Carenet normally')
        else:
            self.assertEqual(cn, Carenet.objects.get(pk=cn.pk))

        # shouldn't be able to create two carenets with the same name on the same record
        try:
            cn = self.createCarenet(TEST_CARENETS, 0, force_create=True)
        except IntegrityError:
            transaction.rollback()
        else:
            self.fail('Added two carenets with the same name to the same record')

    def test_manage_docs(self):

        # No docs should be in the carenet yet.
        self.assertFalse(self.good_carenet.contains_doc(self.good_record.demographics.document))
        self.assertFalse(self.good_carenet.contains_doc(self.good_doc))
        self.assertEqual(self.good_carenet.demographics, None)

        self.assertFalse(self.bad_carenet.contains_doc(self.good_record.demographics.document))
        self.assertFalse(self.bad_carenet.contains_doc(self.good_doc))
        self.assertEqual(self.bad_carenet.demographics, None)

        # Add all of our docs to the good carenet
        self.good_carenet.add_doc(self.good_record.demographics.document)
        self.good_carenet.add_doc(self.good_doc)
                                   
        # Now they should be in there
        self.assertTrue(self.good_carenet.contains_doc(self.good_record.demographics.document))
        self.assertTrue(self.good_carenet.contains_doc(self.good_doc))
        self.assertTrue(self.good_carenet.demographics.document)
        self.assertEqual(self.good_carenet.demographics.document, self.good_record.demographics.document)

        # Fail to add a bunch of docs to the bad carenet
        self.assertRaises(ValueError, self.bad_carenet.add_doc, self.good_record.demographics.document)
        self.assertRaises(ValueError, self.bad_carenet.add_doc, self.good_doc)

        # Those docs better not be in the bad carenet
        self.assertFalse(self.bad_carenet.contains_doc(self.good_record.demographics.document))
        self.assertFalse(self.bad_carenet.contains_doc(self.good_doc))
        self.assertEqual(self.bad_carenet.demographics, None)

        # Now let's remove the docs from the good carenet
        self.good_carenet.remove_doc(self.good_record.demographics.document)
        self.good_carenet.remove_doc(self.good_doc)

        # Now they shouldn't be in the good carenet anymore, either.
        self.assertFalse(self.good_carenet.contains_doc(self.good_record.demographics.document))
        self.assertFalse(self.good_carenet.contains_doc(self.good_doc))
        self.assertEqual(self.good_carenet.demographics, None)
