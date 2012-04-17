"""
Indivo custom XML serializer
"""
import datetime
from xml.dom import pulldom

from django.conf import settings
from django.db import models
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.encoding import smart_unicode

from indivo.lib.iso8601 import format_utc_date
from indivo.serializers import base

class Serializer(base.Serializer):
    """
    Serializes a QuerySet to XML.  Foreign Key and Many-to-Many fields are 
    processed as sub-objects. 
    
    WARNING: currently does not detect cycles
    """

    def indent(self, level):
        if self.options.get('indent', None) is not None:
            self.xml.ignorableWhitespace('\n' + ' ' * self.options.get('indent', None) * level)

    def start_serialization(self):
        """
        Start serialization -- open the XML document and the root element.
        """
        self.xml = SimplerXMLGenerator(self.stream, self.options.get("encoding", settings.DEFAULT_CHARSET))
        self.xml.startDocument()
        self.xml.startElement("Models", {})

    def end_serialization(self):
        """
        End serialization -- end the document.
        """
        self.indent(0)
        self.xml.endElement("Models")
        self.xml.endDocument()

    def start_object(self, obj):
        """
        Called as each object is handled.
        """
        if not hasattr(obj, "_meta"):
            raise base.SerializationError("Non-model object (%s) encountered during serialization" % type(obj))

        self.indent(1)
        self.xml.startElement("Model", {
            "name" : smart_unicode(obj.__class__.__name__)
        })

    def end_object(self, obj):
        """
        Called after handling all fields for an object.
        """
        self.indent(1)
        self.xml.endElement("Model")

    def handle_field(self, obj, field):
        """
        Called to handle each field on an object (except for ForeignKeys and
        ManyToManyFields)
        """
        self.indent(2)
        self.xml.startElement("Field", {
            "name" : field.name
        })
        # Get a "string version" of the object's data.
        if getattr(obj, field.name) is not None:
            value = field._get_val_from_obj(obj)
            if isinstance(value, datetime.datetime) or isinstance(value, datetime.time):
                value = format_utc_date(value)
            elif isinstance(value, datetime.date):
                value = format_utc_date(value, date_only=True)
            else:
                 value = field.value_to_string(obj)
            self.xml.characters(value)
        else:
            self.xml.addQuickElement("None")

        self.xml.endElement("Field")

    def handle_fk_field(self, obj, field):
        """
        Called to handle a ForeignKey (we need to treat them slightly
        differently from regular fields).
        """
        self._start_relational_field(field)
        related = getattr(obj, field.name)
        if related is not None:
            self.process_objects([related])
        else:
            self.xml.addQuickElement("None")
        self.xml.endElement("Field")

    def handle_m2m_field(self, obj, field):
        """
        Called to handle a ManyToManyField. Related objects are only
        serialized as references to the object's PK (i.e. the related *data*
        is not dumped, just the relation).
        """
        if field.creates_table:
            self._start_relational_field(field)
            self.xml.startElement("Models")
            self.process_objects(getattr(obj, field.name))
            self.xml.endElement("Models")
            self.xml.endElement("Field")

    def _start_relational_field(self, field):
        """
        Helper to output the <field> element for relational fields
        """
        self.indent(2)
        self.xml.startElement("Field", {
            "name" : field.name
        })

class Deserializer(base.Deserializer):
    """
    Deserialization is not currently supported
    """

    def __init__(self, stream_or_string, **options):
        raise NotImplementedError