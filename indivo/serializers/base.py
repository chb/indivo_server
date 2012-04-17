"""
Module for abstract serializer/unserializer base classes.

Differentiated from the Django base serializer by breaking out
object processing into a separate method; allowing implementing
serializers to process nested objects.  
"""

from StringIO import StringIO

from django.db import models
from django.core.serializers import base

class Serializer(base.Serializer):
    """
    Abstract serializer base class.
    """

    # Indicates if the implemented serializer is only available for
    # internal Django use.
    internal_use_only = False

    def serialize(self, queryset, **options):
        """
        Serialize a queryset.
        """
        self.options = options

        self.stream = options.get("stream", StringIO())
        self.selected_fields = options.get("fields")
        self.start_serialization()
        self.process_objects(queryset)
        self.end_serialization()
        return self.getvalue()

    def process_objects(self, objects):
        for obj in objects:
            self.start_object(obj)
            for field in obj._meta.local_fields:
                if field.serialize:
                    if field.rel is None:
                        if self.selected_fields is None or field.attname in self.selected_fields:
                            self.handle_field(obj, field)
                    else:
                        if self.selected_fields is None or field.attname[:-3] in self.selected_fields:
                            self.handle_fk_field(obj, field)
            for field in obj._meta.many_to_many:
                if field.serialize:
                    if self.selected_fields is None or field.attname in self.selected_fields:
                        self.handle_m2m_field(obj, field)
            self.end_object(obj)    
            
class Deserializer(object):
    """
    Deserialization is not supported
    """

    def __init__(self, stream_or_string, **options):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError


class DeserializedObject(object):
    """
    Deserialization is not currently supported
    """

    def __init__(self, obj, m2m_data=None):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def save(self, save_m2m=True):
        raise NotImplementedError
