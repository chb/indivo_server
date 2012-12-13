from indivo.serializers import DataModelSerializers
from indivo.data_models.options import DataModelOptions
from indivo.lib.rdf import PatientGraph
from indivo.validators import ValueInSetValidator, ExactValueValidator, NonNullValidator

SNOMED_URI = 'http://purl.bioontology.org/ontology/SNOMEDCT/'

class ClinicalNoteSerializers(DataModelSerializers):

    def to_rdf(query, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        resultOrder = graph.addClinicalNoteList(query.results.iterator(), True if query.limit else False)
        graph.addResponseSummary(query, resultOrder)
        return graph.toRDF()        

class ClinicalNoteOptions(DataModelOptions):
    model_class_name = 'ClinicalNote'
    serializers = ClinicalNoteSerializers
    field_validators = {
        'format': [NonNullValidator()],
        }
