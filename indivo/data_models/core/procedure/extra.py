from indivo.serializers import DataModelSerializers
from indivo.data_models.options import DataModelOptions
from indivo.lib.rdf import PatientGraph
from indivo.validators import ExactValueValidator, NonNullValidator

SNOMED_URI = 'http://purl.bioontology.org/ontology/SNOMEDCT/'

class ProcedureSerializers(DataModelSerializers):

    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        graph.addProcedureList(queryset.iterator())
        return graph.toRDF()        

class ProcedureOptions(DataModelOptions):
    model_class_name = 'Procedure'
    serializers = ProcedureSerializers
    field_validators = {
        'name_code_system': [ExactValueValidator(SNOMED_URI)],
        'name_code_identifier': [NonNullValidator()],
        'name_code_title': [NonNullValidator()],
        }
