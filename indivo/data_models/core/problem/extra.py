from indivo.serializers import DataModelSerializers
from indivo.data_models.options import DataModelOptions
from indivo.lib.rdf import PatientGraph
from indivo.validators import ValueInSetValidator, ExactValueValidator, NonNullValidator

SNOMED_URI = 'http://purl.bioontology.org/ontology/SNOMEDCT/'

class ProblemSerializers(DataModelSerializers):

    def to_rdf(query, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        resultOrder = graph.addProblemList(query.results.iterator(), True if query.limit else False)
        graph.addResponseSummary(query, resultOrder)
        return graph.toRDF()        

class ProblemOptions(DataModelOptions):
    model_class_name = 'Problem'
    serializers = ProblemSerializers
    field_validators = {
        'name_title': [NonNullValidator()],
        'name_code_system': [ExactValueValidator(SNOMED_URI)],
        'name_code_identifier': [NonNullValidator()],
        'name_code_title': [NonNullValidator()],
        'startDate': [NonNullValidator()],
        }
