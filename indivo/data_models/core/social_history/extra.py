from indivo.serializers import DataModelSerializers
from indivo.data_models.options import DataModelOptions
from indivo.lib.rdf import PatientGraph
from indivo.validators import ValueInSetValidator, ExactValueValidator, NonNullValidator

SNOMED_URI = 'http://purl.bioontology.org/ontology/SNOMEDCT/'

SMOKING_STATUS_IDS = [
    '449868002',
    '230059006',
    '8517006',
    '266919005',
    '266927001',
    '405746006',
]

class SocialHistorySerializers(DataModelSerializers):

    def to_rdf(query, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        resultOrder = graph.addSocialHistoryList(query.results.iterator(), True if query.limit else False)
        graph.addResponseSummary(query, resultOrder)
        return graph.toRDF()        

class SocialHistoryOptions(DataModelOptions):
    model_class_name = 'SocialHistory'
    serializers = SocialHistorySerializers
    field_validators = {
        'smoking_status_code_system': [ExactValueValidator(SNOMED_URI, nullable=True)],
        'smoking_status_code_identifier': [ValueInSetValidator(SMOKING_STATUS_IDS, nullable=True)],
        }
