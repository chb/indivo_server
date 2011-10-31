from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.tests.data.record import TEST_RECORDS
from indivo.tests.data.carenet import TEST_CARENETS
from indivo.models import CarenetAutoshare, Carenet, DocumentSchema
from django.db import IntegrityError, transaction

class CarenetAutoshareModelUnitTests(InternalTests):
    def setUp(self):
        super(CarenetAutoshareModelUnitTests, self).setUp()

        # An record
        self.record = self.createRecord(TEST_RECORDS, 0)

        # A carenet
        self.carenet = Carenet.objects.filter(record = self.record)[0]

    def tearDown(self):
        super(CarenetAutoshareModelUnitTests, self).tearDown()

    @enable_transactions
    def test_construction(self):

        # should construct normally
        args = {'carenet':self.carenet,
                'record':self.record,
                'type':DocumentSchema.objects.get(type='http://indivo.org/vocab/xml/documents#Medication'),
                }
        try:
            ca = CarenetAutoshare.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not create CarenetAutoshare normally')
        else:
            self.assertEqual(ca, CarenetAutoshare.objects.get(pk=ca.pk))

        # shouldn't be able to autoshare the same doctype with the same carenet twice
        try:
            ca = CarenetAutoshare.objects.create(**args)
        except IntegrityError:
            transaction.rollback()
        else:
            self.fail('Autoshared the same doctype with the same carenet twice')
