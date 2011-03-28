"""
Indivo Model for Allergies
"""

from fact import Fact
from django.db import models
from django.conf import settings

class Allergy(Fact):
  date_diagnosed = models.DateField(null=True)
  diagnosed_by = models.CharField(max_length=32, null=True)

  allergen_type = models.CharField(max_length=200, null=True)
  allergen_type_type = models.CharField(max_length=200, null=True)
  allergen_type_value = models.CharField(max_length=200, null=True)
  allergen_type_abbrev = models.CharField(max_length=200, null=True)

  allergen_name = models.CharField(max_length=200)
  allergen_name_type = models.CharField(max_length=200, null=True)
  allergen_name_value = models.CharField(max_length=200, null=True)
  allergen_name_abbrev = models.CharField(max_length=200, null=True)

  reaction = models.CharField(max_length=128, null=True)
  specifics = models.TextField(null=True)

  def __unicode__(self):
    return 'Allergy %s' % self.id

