"""
Indivo Python Serializer

"""

from django.core.serializers.python import Serializer as DjangoPythonSerializer
from django.db import models
from django.utils.encoding import smart_unicode, is_protected_type

class Serializer(DjangoPythonSerializer):
    """
    Serializes a QuerySet to basic Python objects.
    - Parses foreign key and many-to-many fields into nested objects
    - Output mirrors Indivo SDML format
    
    WARNING: currently does not detect cycles
    """

    internal_use_only = True

    def end_object(self, obj):
        self._current["__modelname__"] = smart_unicode(obj.__class__.__name__)
        self.objects.append(self._current)
        self._current = None

    def handle_fk_field(self, obj, field):
        related = getattr(obj, field.name)
        if related is not None:
            new_serializer = self.__class__()
            related = new_serializer.serialize([related], **self.options)[0]
        self._current[field.name] = related

    def handle_m2m_field(self, obj, field):
        if field.creates_table:
            related = getattr(obj, field.name)
            self._current[field.name] = new_serializer.serialize(related.iterator(), **self.options)

def Deserializer(object_list, **options):
    """
    Deserialization is not currently supported
    
    """
    raise NotImplementedError
