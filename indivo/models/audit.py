"""
Indivo Model for Audit
"""

from django.db import models
from django.conf import settings

from base import BaseModel
from indivo.models import Principal, Record, Document

# SZ: Do not put any foreign key constraints on this table. :)
class Audit(BaseModel):
  req_view_func               = models.CharField(max_length=255)
  req_url                     = models.URLField()
  req_datetime                = models.DateTimeField()
  req_ip_address              = models.IPAddressField()
  req_domain                  = models.URLField(null=True)
  req_headers                 = models.TextField()
  req_method                  = models.CharField(max_length=12)
  record                      = models.CharField(max_length=64, null=True)
  document                    = models.CharField(max_length=64, null=True)
  resp_code                   = models.IntegerField()
  resp_error_msg              = models.CharField(max_length=255)
  resp_server                 = models.CharField(max_length=255)
  resp_headers                = models.TextField()

  # 2010-01-19 Ben - we only record the effective and proxied by principal
  #                  because the actual principal might be a token, which
  #                  is short lived.
  #
  # req_principal_id            = models.CharField(max_length=64)
  # req_principal_email         = models.CharField(max_length=255)

  ## added by Ben for new types of tokens
  req_effective_principal_email = models.CharField(max_length=255, null=True)
  req_proxied_by_principal_email = models.CharField(max_length=255, null=True)

  #req_principal_creator_email = models.CharField(max_length=255)
  #req_principal_type          = models.CharField(max_length=24)

  def __unicode__(self):
    return 'Audit %s' % self.id
