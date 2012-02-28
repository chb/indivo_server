"""
Indivo Models for Measurements
"""

from fact import Fact
from django.db import models
from django.conf import settings

class Measurement(Fact):
  type = models.CharField(max_length=24)
  value = models.FloatField()
  unit = models.CharField(max_length=8)
  datetime = models.DateTimeField()

  def set_source_docs(self, docs):
    self.source_docs = docs

  def __unicode__(self):
    return 'Measurement %s' % self.id

