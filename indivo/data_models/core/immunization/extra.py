from indivo.serializers import DataModelSerializers
from indivo.lib.rdf import PatientGraph

class ImmunizationSerializers(DataModelSerializers):
    model_class_name = 'Immunization'

    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        graph.addImmunizationList(queryset.iterator())
        return graph.toRDF()
