"""
Indivo custom XML serializer
"""
import datetime
from lxml import etree

from django.conf import settings
from django.db import models
from django.utils.encoding import smart_unicode

from indivo.lib.iso8601 import format_utc_date
from indivo.serializers import base

class Serializer(base.Serializer):
    """
    Serializes a QuerySet to XML.  Foreign Key and Many-to-Many fields are 
    processed as sub-objects. 
    
    """

    def start_serialization(self):
        """
        Start serialization
        """
        self.root = etree.Element("Models")
        self._current = None

    def end_serialization(self):
        """
        End serialization -- end the document.
        """
        pass

    def start_object(self, obj):
        """
        Called as each object is handled.
        """
        if not hasattr(obj, "_meta"):
            raise base.SerializationError("Non-model object (%s) encountered during serialization" % type(obj))

        self.current = etree.Element("Model", 
                                     name = smart_unicode(obj.__class__.__name__),
                                     documentId = getattr(obj, 'document_id'))
        self.root.append(self.current)
        

    def end_object(self, obj):
        """
        Called after handling all fields for an object.
        """
        pass

    def handle_field(self, obj, field):
        """
        Called to handle each field on an object (except for ForeignKeys and
        ManyToManyFields)
        """
        field_element = etree.Element("Field", name=field.name)

        # Get a "string version" of the object's data.
        if getattr(obj, field.name) is not None:
            value = field._get_val_from_obj(obj)
            if isinstance(value, datetime.datetime) or isinstance(value, datetime.time):
                value = format_utc_date(value)
            elif isinstance(value, datetime.date):
                value = format_utc_date(value, date_only=True)
            else:
                 value = field.value_to_string(obj)
            field_element.text = value
        
        self.current.append(field_element)

    def handle_fk_field(self, obj, field):
        """
        Called to handle a ForeignKey (we need to treat them slightly
        differently from regular fields).
        """
        field_element = etree.Element("Field", name=field.name)
        related = getattr(obj, field.name)
        if related is not None:
            new_serializer = Serializer()
            self.options.update({'seen': self.seen})
            parsed_results = new_serializer.serialize([related], **self.options)
        else:
            return

        if len(parsed_results) > 0:
            # attach the first Model of the results
            field_element.append(parsed_results[0])
        
        self.current.append(field_element)

    def handle_m2m_field(self, obj, field):
        """
        Called to handle a ManyToManyField. 
        """
        field_element = etree.Element("Field", name=field.name)
        
        if field.creates_table:
            new_serializer = Serializer()
            self.options.update({'seen': self.seen})
            parsed_results = new_serializer.serialize(related, **self.options)
        
        if len(parsed_results) > 0:
            # attach the returned Models
            field_element.append(parsed_results)
            
        self.current.append(field_element)

    def handle_o2m_field(self, obj, field_name):
        field_element = etree.Element("Field", name=field_name)
        
        related_manager = getattr(obj, field_name)
        related = related_manager.all()
        new_serializer = Serializer()
        self.options.update({'seen': self.seen})
        parsed_results = new_serializer.serialize(related.iterator(), **self.options)
        
        if len(parsed_results) > 0:
            # attach the returned Models
            field_element.append(parsed_results)
            
        self.current.append(field_element) 

    def getvalue(self):
        return self.root

class Deserializer(base.Deserializer):
    """
    Deserialization is not currently supported
    """

    def __init__(self, stream_or_string, **options):
        raise NotImplementedError
