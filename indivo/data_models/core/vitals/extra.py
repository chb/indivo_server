from indivo.serializers import DataModelSerializers
from indivo.lib.rdf import PatientGraph

class EventSerializers(DataModelSerializers):
    model_class_name = 'Encounter'

    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        graph.addEncounterList(queryset.iterator())
        return graph.toRDF()

class VitalsSerializers(DataModelSerializers):
    model_class_name = 'VitalSigns'

    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record

        graph = PatientGraph(record)
        graph.addVitalsList(queryset.iterator())
        return graph.toRDF()
