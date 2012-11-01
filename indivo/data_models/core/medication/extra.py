from indivo.serializers import DataModelSerializers
from indivo.validators import ValueInSetValidator, ExactValueValidator, NonNullValidator
from indivo.data_models.options import DataModelOptions
from indivo.lib.rdf import PatientGraph

RXN_URI="http://purl.bioontology.org/ontology/RXNORM/"
MED_PROV_URI="http://smartplatforms.org/terms/codes/MedicationProvenance#"

MED_PROVS = [
    'prescription',
    'fulfillment',
    'administration',
    'reconciliation',
    'patientReport',
]

class MedicationSerializers(DataModelSerializers):
    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        graph.addMedList(queryset.iterator())
        return graph.toRDF()

class MedicationOptions(DataModelOptions):
    model_class_name = 'Medication'
    serializers = MedicationSerializers
    field_validators = {
        'name_code_system': [ExactValueValidator(RXN_URI)],
        'name_code_identifier': [NonNullValidator()],
        'name_code_title': [NonNullValidator()],
        'provenance_code_system': [ExactValueValidator(MED_PROV_URI, nullable=True)],
        'provenance_code_identifier': [ValueInSetValidator(MED_PROVS, nullable=True)],
        'startDate': [NonNullValidator()],
        }


class FillSerializers(DataModelSerializers):
    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record

        graph = PatientGraph(record)
        graph.addFillList(queryset.iterator())
        return graph.toRDF()

class FillOptions(DataModelOptions):
    model_class_name = 'Fill'
    serializers = FillSerializers
    field_validators = {
        'date': [NonNullValidator()],
        'dispenseDaysSupply': [NonNullValidator()],
        }
