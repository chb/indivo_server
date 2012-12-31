from indivo.models import Fact
from django.db import models
from indivo.fields import CodedValueField, OrganizationField, ProviderField

class Encounter(Fact):
    startDate = models.DateTimeField(null=True)
    endDate = models.DateTimeField(null=True)
    facility = OrganizationField()
    provider = ProviderField()
    type = CodedValueField()