from indivo.models import Fact
from indivo.fields import ProviderField
from django.db import models

class ClinicalNote(Fact):
    date = models.DateTimeField()
    title = models.CharField(max_length=255, null=True)
    format = models.CharField(max_length=255, null=True)
    value = models.CharField(max_length=255, null=True)
    provider = ProviderField()
