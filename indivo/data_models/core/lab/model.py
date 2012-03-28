"""
Indivo Model for Allergies
"""

from indivo.models import Fact
from django.db import models
from django.conf import settings

class Lab(Fact):
  date_measured         = models.DateTimeField()
  lab_name              = models.CharField(max_length=250, null=True)
  lab_address           = models.CharField(max_length=250, null=True)
  lab_type              = models.CharField(max_length=250, null=True)
  lab_comments          = models.TextField(null=True)

  first_panel_name      = models.CharField(max_length=250, null=True)
  first_lab_test_name   = models.CharField(max_length=250, null=True)
  first_lab_test_value  = models.CharField(max_length=250, null=True)

  normal_range_minimum  = models.CharField(max_length=250, null=True)
  normal_range_maximum  = models.CharField(max_length=250, null=True)
  non_critical_range_minimum  = models.CharField(max_length=250, null=True)
  non_critical_range_maximum  = models.CharField(max_length=250, null=True)

  def __unicode__(self):
    return 'Lab %s' % self.id

