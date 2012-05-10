from indivo.serializers import DataModelSerializers
from indivo.lib.rdf import PatientGraph

class ProblemSerializers(DataModelSerializers):
    model_class_name = 'Problem'

    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        graph = PatientGraph(record)
        graph.addProblemList(queryset.iterator())
        return graph.toRDF()


