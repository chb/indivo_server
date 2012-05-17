from indivo.serializers import DataModelSerializers
from indivo.lib.rdf import PatientGraph

class LabSerializers(DataModelSerializers):
    model_class_name = 'LabResult'

    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        graph.addLabList(queryset.iterator())
        return graph.toRDF()
