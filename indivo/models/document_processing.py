"""
Indivo Models
"""

from django.db import models
from django.conf import settings
from base import Object

class DocumentProcessing(Object):
  document = models.ForeignKey('Document', null=True, related_name='processed_doc')
