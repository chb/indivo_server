import uuid

from lxml import etree

from django.conf import settings
from django.core import serializers
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import simplejson

from indivo.lib.query import DATE, STRING, NUMBER
from indivo.lib.utils import LazyProperty
from indivo.models import Record, Document
from indivo.models.base import BaseModel, DataModelBase
from indivo.serializers.json import IndivoJSONEncoder

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
        return "%s/records/%s/%s/%s"%(settings.SITE_URL_PREFIX, self.record.id, modelname, self.id) 
    
    #Meta = BaseMeta(True)
    
    def save(self, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())

        # Validate the Model
        try:
            self.full_clean()
        except ValidationError as e:

            # Just raise the first failure
            error_field, errors = e.message_dict.popitem()
            raise ValueError("%s object didn't validate: %s -- %s"%(self.__class__.__name__, error_field, errors[0]))
        super(Fact, self).save(**kwargs)

    @classmethod
    def to_json(cls, queryset, result_count, record=None, carenet=None):
        data = serializers.serialize("indivo_python", queryset)
        return simplejson.dumps(data, cls=IndivoJSONEncoder)
      
    @classmethod
    def to_xml(cls, queryset, result_count, record=None, carenet=None):
        root = serializers.serialize("indivo_xml", queryset)
        return etree.tostring(root)

    @LazyProperty
    def filter_fields(self):
        """Dictionary of field_name:(field_name, field_type) for query-able fields on this Fact"""
        if not hasattr(self, '_filter_fields'):
            self.attach_filter_fields()

        # _filter_fields attribute is set on the Class, so we return a copy here to avoid accidental alteration
        return self._filter_fields.copy()

    @classmethod
    def attach_filter_fields(cls):
        """Inspect the Class and attach a list of valid filter fields for querying"""
        # all data models have a default created_at
        filters = {'created_at': ('created_at', 'date')}

        # find all viable local fields and add them as valid filters
        for field in cls._meta.local_fields:
            if field.serialize and field.rel is None:
                # determine field type, defaulting to string
                field_type = 'string'
                if isinstance(field, models.DateField) or isinstance(field, models.TimeField):
                    field_type = 'date'
                elif isinstance(field, models.DecimalField) or isinstance(field, models.FloatField) or isinstance(field, models.IntegerField):
                    field_type = 'number'
                    # add to filters
                filters[field.name] = (field.name, field_type )
        cls._filter_fields = filters