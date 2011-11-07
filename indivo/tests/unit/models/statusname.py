from indivo.tests.internal_tests import InternalTests, enable_transactions
from indivo.models import StatusName
from django.db import IntegrityError, transaction

class StatusNameModelUnitTests(InternalTests):
    def setUp(self):
        super(StatusNameModelUnitTests,self).setUp()
        
    def tearDown(self):
        super(StatusNameModelUnitTests,self).tearDown()

    @enable_transactions
    def test_construction(self):
        
        # should construct normally
        try:
            sn = StatusName.objects.create(name='defunct', id=4)
        except IntegrityError:
            transaction.rollback()
            self.fail('Could not create StatusName normally')
        else:
            self.assertEqual(sn, StatusName.objects.get(pk=sn.pk))

