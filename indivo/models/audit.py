"""
Indivo Model for Audit
"""

from django.db import models
from django.conf import settings

from base import BaseModel
from indivo.models import Principal, Record, Document

# SZ: Do not put any foreign key constraints on this table. :)
class Audit(BaseModel):
  # Basic Info
  datetime = models.DateTimeField()
  view_func = models.CharField(max_length=255, null=True)
  request_successful = models.BooleanField()
  
  # Principal Info
  effective_principal_email = models.CharField(max_length=255, null=True)
  proxied_by_email = models.CharField(max_length=255, null=True)
  
  # Resources
  carenet_id = models.CharField(max_length=64, null=True)
  record_id = models.CharField(max_length=64, null=True)
  pha_id = models.CharField(max_length=64, null=True)
  document_id = models.CharField(max_length=64, null=True)
  external_id = models.CharField(max_length=250, null=True)
  message_id = models.CharField(max_length=250, null=True)
  
  # Request Info
  req_url = models.URLField(null=True)
  req_ip_address = models.IPAddressField(null=True)
  req_domain = models.URLField(null=True)
  req_headers = models.TextField(null=True)
  req_method = models.CharField(max_length=12, null=True)
  
  # Response Info
  resp_code = models.IntegerField(null=True)
  resp_headers = models.TextField(null=True)
  

  def __unicode__(self):
    return 'Audit %s' % self.id
