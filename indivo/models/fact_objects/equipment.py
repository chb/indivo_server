"""
Indivo Model for Equipment
"""

from fact import Fact
from django.db import models
from django.conf import settings

class Equipment(Fact):
  date_started = models.DateField(null=True)
  date_stopped = models.DateField(null=True)
  name = models.CharField(max_length=40)
  vendor = models.CharField(max_length=40, null=True)
  description = models.TextField(null=True)

  def __unicode__(self):
    return 'Equipment %s' % self.id

