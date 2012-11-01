from django.db import models

from indivo.fields import CodedValueField, ProviderField
from indivo.models import Fact

class Procedure(Fact):
    date = models.DateTimeField(null=True)
    notes = models.TextField(null=True)
    name = CodedValueField()
    status = CodedValueField(null=True)
    provider = ProviderField(null=True)
    