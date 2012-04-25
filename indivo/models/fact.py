import uuid

from lxml import etree

from django.core import serializers
from django.db import models
from django.utils import simplejson

from indivo.lib.query import DATE, STRING, NUMBER
from indivo.lib.utils import LazyProperty
from indivo.models import Record, Document
from indivo.models.base import BaseModel
from indivo.serializers.json import IndivoJSONEncoder

class Fact(BaseModel):

    id = models.CharField(max_length = 50, primary_key = True)
    created_at = models.DateTimeField(auto_now_add = True)
    # should we add a created_by denormalized field here to make it easier to sort facts?
    document = models.ForeignKey(Document, related_name='allergy', null=True)
    record = models.ForeignKey(Record, related_name='allergy', null=True)
    
    def __unicode__(self):
      return "%s %s" % (self.__class__.__name__, self.id)
    
    #Meta = BaseMeta(True)
    
    def save(self, **kwargs):
      if not self.id:
        self.id = str(uuid.uuid4())
      super(Fact, self).save(**kwargs)

    @classmethod
    def to_json(cls, data):
        data = serializers.serialize("indivo_python", data)
        return simplejson.dumps(data, cls=IndivoJSONEncoder)
      
    @classmethod
    def to_xml(cls, data):
        root = serializers.serialize("indivo_xml", data)
        return etree.tostring(root)