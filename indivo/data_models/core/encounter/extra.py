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
    def to_rdf(query, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        resultOrder = graph.addEncounterList(query.results.iterator(), True if query.limit else False)
        graph.addResponseSummary(query, resultOrder)
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

