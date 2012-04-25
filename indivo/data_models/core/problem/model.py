from indivo.models import Fact
from indivo.fields import CodedValueField
from django.db import models

class Problem(Fact):
  startDate = models.DateTimeField(null=True)
  endDate = models.DateTimeField(null=True)
  name = CodedValueField()
  notes = models.TextField(null=True)
