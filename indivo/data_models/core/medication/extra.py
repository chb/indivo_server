from indivo.serializers import DataModelSerializers
from indivo.lib.rdf import PatientGraph

class MedicationSerializers(DataModelSerializers):
    model_class_name = 'Medication'

    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        graph.addMedList(queryset.iterator())
        return graph.toRDF()

class FillSerializers(DataModelSerializers):
    model_class_name = 'Fill'

    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record

        graph = PatientGraph(record)
        graph.addFillList(queryset.iterator):
        return graph.toRDF()
