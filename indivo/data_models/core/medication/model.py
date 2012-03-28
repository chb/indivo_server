"""
Indivo Model for Medication
"""

from indivo.models import Fact
from django.db import models
from django.conf import settings

class Medication(Fact):
  date_started = models.DateField(null=True)
  date_stopped = models.DateField(null=True)
  name = models.CharField(max_length=200)
  name_type = models.CharField(max_length=200, null=True)
  name_value = models.CharField(max_length=200, null=True)
  name_abbrev = models.CharField(max_length=20, null=True)
  brand_name = models.CharField(null=True, max_length=200)
  brand_name_type = models.CharField(null=True, max_length=200)
  brand_name_value = models.CharField(null=True, max_length=200)
  brand_name_abbrev = models.CharField(null=True, max_length=20)
  dose_textvalue = models.CharField(null=True, max_length=100)
  dose_value = models.CharField(null=True, max_length=20)
  dose_unit = models.CharField(null=True, max_length=40)
  dose_unit_type = models.CharField(null=True, max_length=200)
  dose_unit_value = models.CharField(null=True, max_length=20)
  dose_unit_abbrev = models.CharField(null=True, max_length=20)
  route = models.CharField(null=True, max_length=200)
  route_type = models.CharField(null=True, max_length=200)
  route_value = models.CharField(null=True, max_length=200)
  route_abbrev = models.CharField(null=True, max_length=20)
  strength_textvalue= models.CharField(null=True, max_length=100)
  strength_value = models.CharField(null=True, max_length=20)
  strength_unit = models.CharField(null=True, max_length=40)
  strength_unit_type = models.CharField(null=True, max_length=200)
  strength_unit_value = models.CharField(null=True, max_length=100)
  strength_unit_abbrev = models.CharField(null=True, max_length=20)
  frequency = models.CharField(null=True, max_length=100)
  frequency_type = models.CharField(null=True, max_length=200)
  frequency_value = models.CharField(null=True, max_length=20)
  frequency_abbrev = models.CharField(null=True, max_length=20)

  prescribed_by_name = models.CharField(max_length=200, null=True)
  prescribed_by_institution = models.CharField(max_length=200, null=True)
  prescribed_on = models.DateField(null=True)
  prescribed_stop_on = models.DateField(null=True)

  dispense_as_written = models.NullBooleanField(null=True)

  # written as days
  prescription_duration = models.CharField(null=True, max_length=100)
  prescription_refill_info = models.TextField(null=True)
  prescription_instructions = models.TextField(null=True)

  def __unicode__(self):
    return 'Medication %s' % self.id

