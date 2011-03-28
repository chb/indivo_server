"""
Indivo Models for Immunizations
"""

from fact import Fact
from django.db import models
from django.conf import settings

class Immunization(Fact):
  date_administered = models.DateTimeField(null=True)
  administered_by   = models.CharField(max_length=40, null=True)
  vaccine_type      =  models.CharField(max_length=200, null=True)
  vaccine_type_type =  models.CharField(max_length=80, null=True)
  vaccine_type_value = models.CharField(max_length=40, null=True)
  vaccine_type_abbrev = models.CharField(max_length=20, null=True)
  vaccine_manufacturer = models.CharField(max_length=40, null=True)
  vaccine_lot = models.CharField(max_length=20, null=True)
  vaccine_expiration = models.DateField(null=True)
  sequence = models.IntegerField(null=True)
  anatomic_surface = models.CharField(max_length=40, null=True)
  anatomic_surface_type =  models.CharField(max_length=80, null=True)
  anatomic_surface_value =  models.CharField(max_length=20, null=True)
  anatomic_surface_abbrev =  models.CharField(max_length=20, null=True)
  adverse_event = models.CharField(max_length=100, null=True)

  def __unicode__(self):
    return 'Immunization %s' % self.id

