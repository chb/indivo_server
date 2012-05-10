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

        def replace_field(fields_dict, field_name, field):
            new_fields_dict = copy.copy(fields_dict)
            
            # build the new fields to replace the old field with
            for suffix, new_field_params in field.__class__.replacements.iteritems():
                new_name = "%s%s"%(field_name, suffix)
                new_field_class, new_field_kwargs = new_field_params
                new_field = new_field_class(**new_field_kwargs)
                new_fields_dict[new_name] = new_field

                # recurse if the new field is actually a replaceable DummyField
                if issubclass(new_field_class, DummyField):
                    new_fields_dict = replace_field(new_fields_dict, new_name, new_field)

            del new_fields_dict[field_name]
            return new_fields_dict

        # Iterate over the fields in the model, and replace all of the dummy fields
        new_attrs = copy.copy(attrs)
        for field_name, field_val in attrs.iteritems():
            if isinstance(field_val, DummyField):
                new_attrs = replace_field(new_attrs, field_name, field_val)
        
        return super(DataModelBase, cls).__new__(cls, name, bases, new_attrs)

class Fact(BaseModel):
    __metaclass__ = DataModelBase

    id = models.CharField(max_length = 50, primary_key = True)
    created_at = models.DateTimeField(auto_now_add = True)
    # should we add a created_by denormalized field here to make it easier to sort facts?
    document = models.ForeignKey(Document, null=True)
    record = models.ForeignKey(Record, null=True)
    
    def __unicode__(self):
      return "%s %s" % (self.__class__.__name__, self.id)

    def uri(self, modelname=None):
        if not modelname:
            modelname = self.__class__.__name__.lower() + 's'
        return "http://indivo.org/records/%s/%s/%s"%(self.record.id, modelname, self.id)
    
    #Meta = BaseMeta(True)
    
    def save(self, **kwargs):
      if not self.id:
        self.id = str(uuid.uuid4())
      super(Fact, self).save(**kwargs)

    @classmethod
    def to_json(cls, queryset, result_count, record=None, carenet=None):
        data = serializers.serialize("indivo_python", queryset)
        return simplejson.dumps(data, cls=IndivoJSONEncoder)
      
    @classmethod
    def to_xml(cls, queryset, result_count, record=None, carenet=None):
        root = serializers.serialize("indivo_xml", queryset)
        return etree.tostring(root)

