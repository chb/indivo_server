"""
Indivo Model for Procedure
"""

from fact import Fact
from django.db import models
from django.conf import settings

class Procedure(Fact):
  date_performed = models.DateTimeField(null=True)
  name = models.CharField(max_length=100)
  name_type = models.CharField(max_length=80, null=True)
  name_value = models.CharField(max_length=40, null=True)
  name_abbrev = models.CharField(max_length=20, null=True)
  provider_name = models.CharField(max_length=200, null=True)
  provider_institution = models.CharField(max_length=200, null=True)
  location = models.CharField(max_length=100, null=True)
  comments = models.TextField(null=True)

  def __unicode__(self):
    return 'Procedure %s' % self.id

