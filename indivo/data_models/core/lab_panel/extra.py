from indivo.serializers import DataModelSerializers
from indivo.data_models.options import DataModelOptions
from indivo.rdf.rdf import PatientGraph

LOINC_URI="http://purl.bioontology.org/ontology/LNC/"

class LabPanelSerializers(DataModelSerializers):
    def to_rdf(query, record=None, carenet=None):
        if not record:
            record = carenet.record
        graph = PatientGraph(record)
        resultOrder = graph.addLabPanelList(query.results.iterator(), True if query.limit else False)
        graph.addResponseSummary(query, resultOrder)
        return graph.toRDF()

class LabPanelOptions(DataModelOptions):
    model_class_name = 'LabPanel'
    serializers = LabPanelSerializers
