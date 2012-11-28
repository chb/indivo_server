from indivo.serializers import DataModelSerializers
from indivo.validators import ValueInSetValidator, ExactValueValidator, NonNullValidator
from indivo.data_models.options import DataModelOptions
from indivo.lib.rdf import PatientGraph

ENC_TYPE_URI="http://smartplatforms.org/terms/codes/EncounterType#"
ENC_TYPES = [
    'home',
    'emergency',
    'ambulatory',
    'inpatient',
    'field',
    'virtual',
]

class EncounterSerializers(DataModelSerializers):
    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        graph.addEncounterList(queryset.iterator())
        return graph.toRDF()

class EncounterOptions(DataModelOptions):
    model_class_name = 'Encounter'
    serializers = EncounterSerializers
    field_validators = {
        'type_code_system': [ExactValueValidator(ENC_TYPE_URI)],
        'type_code_identifier': [ValueInSetValidator(ENC_TYPES)],
        'type_code_title': [NonNullValidator()],
        'startDate': [NonNullValidator()],
        }

