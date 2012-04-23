from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.tests.data.app import TEST_USERAPPS
from indivo.tests.data.carenet import TEST_CARENETS
from indivo.models import CarenetPHA
from django.db import IntegrityError, transaction

class CarenetPHAModelUnitTests(InternalTests):
    def setUp(self):
        super(CarenetPHAModelUnitTests, self).setUp()

        # An app
        self.app = self.createUserApp(TEST_USERAPPS, 0)

        # A carenet
        self.carenet = self.createCarenet(TEST_CARENETS, 0)

    def tearDown(self):
        super(CarenetPHAModelUnitTests, self).tearDown()

    @enable_transactions
    def test_construction(self):

        # should construct normally
        try:
            cp = self.addAppToCarenet(self.app, self.carenet)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not create CarenetPHA normally')
        else:
            self.assertEqual(cp, CarenetPHA.objects.get(pk=cp.pk))

        # shouldn't be able to share an app with the same carenet twice
        try:
            cp = self.addAppToCarenet(self.app, self.carenet)
        except IntegrityError:
            transaction.rollback()
        else:
            self.fail('Added an app to the same carenet twice')
