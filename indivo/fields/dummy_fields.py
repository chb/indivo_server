from django.db import models

class DummyField(models.Field):
    """ A field that should be replaced by other fields.
    
    *replacements* should be a mapping from field_suffix to (fieldclass, field_kwargs).
    This instructs the datamodel loader to remove this field, and for each entry in the mapping,
    to add a new field with the original name concatenated with field_suffix, which is an instance
    of class fieldclass instantiated with field_kwargs.
    
    """
    replacements = {}

class CodedValueField(DummyField):
    """ A field for representing coded values.
    
    Eventually, when Django supports fields mapping to multiple database columns, we'll make this
    a real field, but for now it's just an empty DummyField.

    So creating a CodedValueField named 'value', for example, will (under the hood) create three fields:
    
    * value_identifier, a CharField with max_length 255
    * value_title, a CharField with max_length 255
    * value_system, a CharField with max_length 255

    """

    replacements = {
        '_identifier': (models.CharField, {'max_length':255}),
        '_title': (models.CharField, {'max_length':255}),
        '_system': (models.CharField, {'max_length':255}),
        }
    
