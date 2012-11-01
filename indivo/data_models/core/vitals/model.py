from indivo.models import Fact
from django.db import models
from indivo.fields import BloodPressureField, VitalSignField, CodedValueField, OrganizationField, ProviderField

class VitalSigns(Fact):
    date = models.DateTimeField(null=True)
    encounter = models.ForeignKey('Encounter', null=True)
    bp = BloodPressureField()
    bmi = VitalSignField()
    heart_rate = VitalSignField()
    height = VitalSignField()
    oxygen_saturation = VitalSignField()
    respiratory_rate = VitalSignField()
    temperature = VitalSignField()
    weight = VitalSignField()
    head_circ = VitalSignField()

class Encounter(Fact):
    startDate = models.DateTimeField(null=True)
    endDate = models.DateTimeField(null=True)
    facility = OrganizationField()
    provider = ProviderField()
    type = CodedValueField()

    
    
    
