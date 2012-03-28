"""
Indivo Model for Vitals
"""

from indivo.models import Fact
from django.db import models
from django.conf import settings

class Vitals(Fact):

  date_measured = models.DateTimeField(null=True)
  name = models.CharField(max_length=100)
  name_type = models.CharField(max_length=80, null=True)
  name_value = models.CharField(max_length=40, null=True)
  name_abbrev = models.CharField(max_length=20, null=True)
  value = models.FloatField()
  unit = models.CharField(max_length=100)
  unit_type = models.CharField(max_length=80, null=True)
  unit_value = models.CharField(max_length=40, null=True)
  unit_abbrev = models.CharField(max_length=20, null=True)
  site = models.CharField(max_length=40, null=True)
  position = models.CharField(max_length=40, null=True)
  comments = models.TextField(null=True)

  def __unicode__(self):
    return 'Vitals %s' % self.id

