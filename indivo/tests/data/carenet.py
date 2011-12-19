from indivo.models import Carenet
from base import *

class TestCarenet(TestModel):
    model_fields = ['name', 'record']
    model_class = Carenet

    def _setupargs(self, name, record=None):
        self.name = name
        self.record = record

_TEST_CARENETS = [
    {'name': 'test_carenet', 
     'record': ForeignKey('record', 'TEST_RECORDS', 0),
     }
]
TEST_CARENETS = scope(_TEST_CARENETS, TestCarenet)
