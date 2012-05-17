from indivo.models import Fact
from django.db import models
from indivo.fields import CodedValueField, QuantitativeResultField, OrganizationField, NameField

class LabResult(Fact):
    abnormal_interpretation = CodedValueField()
    accession_number = models.CharField(max_length=255, null=True)
    test_name = CodedValueField()
    status = CodedValueField()
    narrative_result = models.CharField(max_length=255, null=True)
    notes = models.CharField(max_length=600, null=True)
    quantitative_result = QuantitativeResultField()
    collected_at = models.DateTimeField(null=True)
    collected_by_org = OrganizationField()
    collected_by_name = NameField()
    collected_by_role = models.CharField(max_length=255, null=True)
