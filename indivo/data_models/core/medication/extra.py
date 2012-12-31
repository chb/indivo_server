from indivo.serializers import DataModelSerializers
from indivo.validators import ValueInSetValidator, ExactValueValidator, NonNullValidator
from indivo.data_models.options import DataModelOptions
from indivo.lib.rdf import PatientGraph

RXN_URI="http://purl.bioontology.org/ontology/RXNORM/"

class MedicationSerializers(DataModelSerializers):
    def to_rdf(query, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        resultOrder = graph.addMedList(query.results.iterator(), True if query.limit else False)
        graph.addResponseSummary(query, resultOrder)
        return graph.toRDF()

class MedicationOptions(DataModelOptions):
    model_class_name = 'Medication'
    serializers = MedicationSerializers
    field_validators = {
        'name_title': [NonNullValidator()],
        'name_code_system': [ExactValueValidator(RXN_URI)],
        'name_code_identifier': [NonNullValidator()],
        'name_code_title': [NonNullValidator()],
        'startDate': [NonNullValidator()],
        }


class FillSerializers(DataModelSerializers):
    def to_rdf(query, record=None, carenet=None):
        if not record:
            record = carenet.record

        graph = PatientGraph(record)
        resultOrder = graph.addFillList(query.results.iterator(), True if query.limit else False)
        graph.addResponseSummary(query, resultOrder)
        return graph.toRDF()

class FillOptions(DataModelOptions):
    model_class_name = 'Fill'
    serializers = FillSerializers
    field_validators = {
        'date': [NonNullValidator()],
        'dispenseDaysSupply': [NonNullValidator()],
        }
