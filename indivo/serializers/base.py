"""
Module for abstract serializer base classes.

Differentiated from the Django base serializer by allowing implementing
serializers to process nested objects.  Recursion is prevented by keeping
track of visited objects, and results in repeated objects being skipped after
their first appearance

"""

from StringIO import StringIO

from django.db import models
from django.core.serializers import base
from django.db.models.fields.related import OneToOneField, ManyToOneRel, OneToOneRel

class SerializationRecursionError(Exception):
    """Object encountered twice during serialization"""
    pass

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
        self.seen = options.get("seen", set([]))
        self.start_serialization()
        self.process_objects(queryset)
        self.end_serialization()
        return self.getvalue()

    def process_objects(self, objects):
        for obj in objects:
            try:
                self.process_object(obj)
            except SerializationRecursionError:
                # do not process objects we have already seen
                pass
            
    def process_object(self, obj):
        # avoid recursive serialization
        if obj.pk in self.seen:
            raise SerializationRecursionError()
        self.seen.add(obj.pk)
        
        self.start_object(obj)
        for field in obj._meta.local_fields:
            if field.serialize:
                if field.rel is None:
                    if self.selected_fields is None or field.attname in self.selected_fields:
                        self.handle_field(obj, field)
                else:
                    if (not isinstance(field.rel, ManyToOneRel) or isinstance(field.rel, OneToOneRel)) and (self.selected_fields is None or field.attname[:-3] in self.selected_fields):
                        self.handle_fk_field(obj, field)
        for relatedObject in obj._meta.get_all_related_objects():
            # don't follow back links for One to One relationships, they will
            # show up in local_fields and be handled there.
            if not isinstance(relatedObject.field, OneToOneField):
                self.handle_o2m_field(obj, relatedObject.get_accessor_name())
        for field in obj._meta.many_to_many:
            if field.serialize:
                if self.selected_fields is None or field.attname in self.selected_fields:
                    self.handle_m2m_field(obj, field)
        self.end_object(obj)    
            
    def handle_o2m_field(self, obj, current, field_name):
        """
        Called to handle a OneToMany field.
        """
        raise NotImplementedError
            
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
