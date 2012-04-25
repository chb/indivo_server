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
from indivo.fields import DummyField

import copy

class DataModelBase(models.base.ModelBase):
    """ Subclass of the Django Model metaclass that handles Dummy Fields on Indivo Data Models. """

    def __new__(cls, name, bases, attrs):
        new_attrs = copy.copy(attrs)
        
        for field_name, field_val in attrs.iteritems():
            if isinstance(field_val, DummyField):
                for suffix, new_field_args in field_val.__class__.replacements.iteritems():
                    new_name = "%s%s"%(field_name, suffix)
                    new_field = new_field_args[0](**new_field_args[1])
                    new_attrs[new_name] = new_field
                del new_attrs[field_name]
        
        return super(DataModelBase, cls).__new__(cls, name, bases, new_attrs)

class Fact(BaseModel):
    __metaclass__ = DataModelBase

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

