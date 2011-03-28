import uuid
from django.db import models
from indivo.models.base import BaseModel
from indivo.models import Record, Document

class Fact(BaseModel):

  id = models.CharField(max_length = 50, primary_key = True)
  created_at = models.DateTimeField(auto_now_add = True)
  # should we add a created_by denormalized field here to make it easier to sort facts?
  document = models.ForeignKey(Document, related_name='allergy', null=True)
  record = models.ForeignKey(Record, related_name='allergy', null=True)

  def __unicode__(self):
    return "Fact %s" % self.id
  
  #Meta = BaseMeta(True)

  def save(self, **kwargs):
    if not self.id:
      self.id = str(uuid.uuid4())
    super(Fact, self).save(**kwargs)

