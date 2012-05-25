from indivo.serializers import DataModelSerializers
from indivo.data_models import DataModelOptions

class TestFillSerializers(DataModelSerializers):
    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        return '''TestFill RDF SHOULD GO HERE. But we don't need to test that here.'''

class TestFillOptions(DataModelOptions):
    model_class_name = 'TestFill'
    serializers = TestFillSerializers


class TestMedSerializers(DataModelSerializers):
    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        return '''TestMed RDF SHOULD GO HERE. But we don't need to test that here.'''

class TestMedOptions(DataModelOptions):
    model_class_name = 'TestMed'
    serializers = TestMedSerializers


class TestPrescriptionSerializers(DataModelSerializers):
    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        return '''TestPrescription RDF SHOULD GO HERE. But we don't need to test that here.'''

class TestPrescriptionOptions(DataModelOptions):
    model_class_name = 'TestPrescription'
    serializers = TestPrescriptionSerializers
