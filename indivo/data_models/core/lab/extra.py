from indivo.serializers import DataModelSerializers
from indivo.validators import ValueInSetValidator, ExactValueValidator, NonNullValidator
from indivo.data_models.options import DataModelOptions
from indivo.lib.rdf import PatientGraph

LAB_INTERP_URI="http://smartplatforms.org/terms/codes/LabResultInterpretation#"
LAB_STATUS_URI="http://smartplatforms.org/terms/codes/LabStatus#"
LOINC_URI="http://purl.bioontology.org/ontology/LNC/"

VALID_INTERPS = [
    'normal',
    'critical',
    'abnormal',
]

VALID_STATUSES = [
    'correction',
    'preliminary',
    'final',
]

class LabSerializers(DataModelSerializers):
    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        graph.addLabList(queryset.iterator())
        return graph.toRDF()

class LabOptions(DataModelOptions):
    model_class_name = 'LabResult'
    serializers = LabSerializers
    field_validators = {
        'abnormal_interpretation_system': [ExactValueValidator(LAB_INTERP_URI, nullable=True)],
        'abnormal_interpretation_identifier': [ValueInSetValidator(VALID_INTERPS, nullable=True)],
        'test_name_system': [ExactValueValidator(LOINC_URI)],
        'test_name_identifier': [NonNullValidator()],
        'test_name_title': [NonNullValidator()],
        'status_system': [ExactValueValidator(LAB_STATUS_URI, nullable=True)],
        'status_identifier': [ValueInSetValidator(VALID_STATUSES, nullable=True)],
        }
