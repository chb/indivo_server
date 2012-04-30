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

    Subclasses must also define one attribute:

    * ``model_class_name``: a string describing the name of the data model it should be attached to, i.e. ``Problem``.

    In order to be called, the methods must be attached to that data model class by calling the 
    ``attach_to_data_model()`` method.

    """

    model_class_name = ''

    @classmethod
    def attach_to_data_model(cls, data_model_cls):
        """ Add all of the defined methods as classmethods on ``data_model_cls``. """
        
        # Don't attach to anything other than our intended target model
        if data_model_cls.__name__ != cls.model_class_name: return

        for attr_name in ATTACHABLE_ATTRS:
            attr_val = getattr(cls, attr_name, None)
            if attr_val:
                # unbind the method from our class
                unbound_func = attr_val.__func__

                # Wrap it as a classmethod
                cm = classmethod(lambda cls, *args, **kwargs: unbound_func(*args, **kwargs))

                # And bind it to our data model
                setattr(data_model_cls, attr_name, cm)
