"""
Indivo Models for Document Relationships
"""

from django.db import models
from django.conf import settings

from base import BaseModel
from indivo.models import Document, DocumentSchema

class DocumentRels(BaseModel):
  document_0 = models.ForeignKey(Document, related_name='rels_as_doc_0')
  document_1 = models.ForeignKey(Document, related_name='rels_as_doc_1')
  relationship = models.ForeignKey(DocumentSchema)

  def __unicode__(self):
    return 'DocumentRel %s' % self.id

