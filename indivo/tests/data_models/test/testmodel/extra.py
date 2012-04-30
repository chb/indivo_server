from indivo.serializers import DataModelSerializers

class TestFillSerializers(DataModelSerializers):
    model_class_name = 'TestFill'

    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        return '''TestFill RDF SHOULD GO HERE. But we don't need to test that here.'''

class TestMedSerializers(DataModelSerializers):
    model_class_name = 'TestMed'

    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        return '''TestMed RDF SHOULD GO HERE. But we don't need to test that here.'''

class TestPrescriptionSerializers(DataModelSerializers):
    model_class_name = 'TestPrescription'

    def to_rdf(queryset, result_count, record=None, carenet=None):
        if not record:
            record = carenet.record
        
        return '''TestPrescription RDF SHOULD GO HERE. But we don't need to test that here.'''
