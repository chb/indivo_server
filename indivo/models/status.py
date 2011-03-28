"""
Indivo Models for Document Status
"""

from django.db import models
from django.conf import settings

from base import BaseModel, Object

class StatusName(BaseModel):
  name = models.CharField(max_length=24)

  def __unicode__(self):
    return 'StatusName %s' % self.id

class DocumentStatusHistory(Object):
  status = models.ForeignKey('StatusName', null=False)
  reason = models.TextField()
  document = models.CharField(max_length=64, null=True)
  record = models.CharField(max_length=64, null=True)
  proxied_by_principal = models.CharField(max_length=255, null=True)
  effective_principal = models.CharField(max_length=255, null=True)

  def __unicode__(self):
    return 'DocumentStatusHistory %s' % self.id
