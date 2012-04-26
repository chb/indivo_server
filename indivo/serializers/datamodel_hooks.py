ATTACHABLE_ATTRS = ['to_rdf', 'to_xml', 'to_json',]

class DataModelSerializers(object):
    """ Abstract base class for defining serializers that should be attached to a data model class.
    
    Serializers will override the default implementations. Subclasses should define any of three methods:

    * ``to_rdf(queryset)``: takes a queryset, and formats it as valid `RDF/XML <http://www.w3.org/TR/rdf-syntax-grammar/>`_ 
      string.

    * ``to_xml(queryset)``: takes a queryset, and formats it as a valid `XML <http://www.w3.org/TR/xml11/>`_ string.

    * ``to_json(queryset)``: takes a queryset, and formats it as a valid `JSON <http://www.json.org/>`_ string.

    Querysets passed into these methods will contain instances of the class specifed in the *data_model_cls* argument
    of the ``__init__()`` method.

    In order to be called, the methods must be attached to that data model class by calling the 
    ``attach_to_data_model()`` method.

    """

    def __init__(self, data_model_cls):
        self.model_cls = data_model_cls

    def attach_to_data_model(self):
        """ Add all of the defined methods as classmethods on ``self.model_cls``. """

        for attr_name in ATTACHABLE_ATTRS:
            attr_val = getattr(self, attr_name, None)
            if attr_val:
                # unbind the method from our class
                unbound_func = attr_val.__func__

                # Wrap it as a classmethod
                def internal_classmethod(cls, *args, **kwargs):
                    return unbound_func(*args, **kwargs)
                internal_classmethod.__name__ = attr_name
                internal_classmethod = classmethod(internal_classmethod)

                # And bind it to our data model
                setattr(self.model_cls, attr_name, internal_classmethod)
