"""
Indivo Model for Problems
"""

from fact import Fact
from django.db import models
from django.conf import settings

class Problem(Fact):
  date_onset = models.DateTimeField(null=True)
  date_resolution = models.DateTimeField(null=True)
  name = models.CharField(max_length=128)
  name_type = models.CharField(max_length=255, null=True)
  name_value = models.CharField(max_length=128, null=True)
  name_abbrev = models.CharField(max_length=24, null=True)
  comments = models.TextField(null=True)
  diagnosed_by = models.CharField(max_length=128, null=True)

  def __unicode__(self):
    return 'Problem %s' % self.id

