from indivo.models import Fact
from django.db import models
from indivo.fields import CodedValueField, ValueAndUnitField, PharmacyField, ProviderField

class Medication(Fact):
    name = CodedValueField()
    endDate = models.DateField(null=True)
    frequency = ValueAndUnitField()
    instructions = models.CharField(max_length=255, null=True)
    provenance = CodedValueField()
    quantity = ValueAndUnitField()
    startDate = models.DateField(null=True)

class Fill(Fact):
    date = models.DateTimeField(null=True)
    dispenseDaysSupply = models.FloatField(null=True)
    pbm = models.CharField(max_length=255, null=True)
    pharmacy = PharmacyField()
    provider = ProviderField()
    quantityDispensed = ValueAndUnitField()
    medication = models.ForeignKey(Medication, null=True, related_name='fulfillments')
  
