"""
Indivo Python Serializer

"""

from django.db import models
from django.utils.encoding import smart_unicode, is_protected_type

from indivo.serializers import base

class Serializer(base.Serializer):
    """
    Serializes a QuerySet to basic Python objects.
    - Parses foreign key and many-to-many fields into nested objects
    - Output mirrors Indivo SDML format
    
    """

    internal_use_only = True

    def start_serialization(self):
        self._current = None
        self.objects = []

    def end_serialization(self):
        pass

    def start_object(self, obj):
        self._current = {}

    def end_object(self, obj):
        self._current["__modelname__"] = smart_unicode(obj.__class__.__name__)
        self._current["__documentid__"] = getattr(obj, 'document_id')
        self.objects.append(self._current)
        self._current = None

    def handle_field(self, obj, field):
        value = field._get_val_from_obj(obj)
        # Protected types (i.e., primitives like None, numbers, dates,
        # and Decimals) are passed through as is. All other values are
        # converted to string first.
        if is_protected_type(value):
            self._current[field.name] = value
        else:
            self._current[field.name] = field.value_to_string(obj)

    def handle_fk_field(self, obj, field):
        related = getattr(obj, field.name)
        if related is not None:
            new_serializer = Serializer()
            self.options.update({'seen': self.seen})
            related = new_serializer.serialize([related], **self.options)
            self._current[field.name] = (related[0] if related else None)

    # TODO: m2m excluded by SDML?
    def handle_m2m_field(self, obj, field):
        if field.creates_table:
            related = getattr(obj, field.name)
            new_serializer = Serializer()
            self.options.update({'seen': self.seen})
            self._current[field.name] = new_serializer.serialize(related.iterator(), **self.options)

    def handle_o2m_field(self, obj, field_name):
        related_manager = getattr(obj, field_name)
        related = related_manager.all()
        new_serializer = Serializer()
        self.options.update({'seen': self.seen})
        parsed_results = new_serializer.serialize(related.iterator(), **self.options)
        self._current[field_name] = parsed_results 

    def getvalue(self):
        return self.objects

def Deserializer(object_list, **options):
    """
    Deserialization is not currently supported
    
    """
    raise NotImplementedError
