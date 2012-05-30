from indivo.serializers import DataModelSerializers
from indivo.data_models import DataModelOptions
from indivo.validators import ExactValueValidator, ValueInSetValidator

class TestFillSerializers(DataModelSerializers):
    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        return '''TestFill RDF SHOULD GO HERE. But we don't need to test that here.'''

class TestFillOptions(DataModelOptions):
    model_class_name = 'TestFill'
    serializers = TestFillSerializers
    field_validators = {
        'supply_days': [ExactValueValidator(30)],
        }


class TestMedSerializers(DataModelSerializers):
    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        return '''TestMed RDF SHOULD GO HERE. But we don't need to test that here.'''

class TestMedOptions(DataModelOptions):
    model_class_name = 'TestMed'
    serializers = TestMedSerializers
    field_validators = {
        'name': [ValueInSetValidator(['med1', 'med2'], nullable=True)],
        }


class TestPrescriptionSerializers(DataModelSerializers):
    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        return '''TestPrescription RDF SHOULD GO HERE. But we don't need to test that here.'''

class TestPrescriptionOptions(DataModelOptions):
    model_class_name = 'TestPrescription'
    serializers = TestPrescriptionSerializers
