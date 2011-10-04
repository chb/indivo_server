from indivo.models import Carenet
from base import TestModel, raw_data_to_objs, ForeignKey

class TestCarenet(TestModel):
    model_fields = ['name', 'record']
    model_class = Carenet

    def __init__(self, name, record=None):
        self.name = name
        self.record = record

_TEST_CARENETS = [
    {'name': 'test_carenet', 
     'record': ForeignKey('record', 'TEST_RECORDS', 0),
     }
]

TEST_CARENETS = raw_data_to_objs(_TEST_CARENETS, TestCarenet)
