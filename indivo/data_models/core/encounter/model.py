from indivo.models import Fact
from indivo.fields import CodedValueField, OrganizationField, ProviderField
from django.db import models

class Encounter(Fact):
  startDate = models.DateTimeField(null=True)
  endDate = models.DateTimeField(null=True)
  facility = OrganizationField()
  provider = ProviderField()
  encounterType = CodedValueField()
