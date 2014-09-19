ATTACHABLE_ATTRS = ['to_rdf', 'to_xml', 'to_json', 'to_sdmx',]

class DataModelSerializers(object):
    """ Abstract base class for defining serializers that should be attached to a data model class.
    
    Serializers will override the default implementations. Subclasses should define any of three methods:

    * ``to_rdf(queryset, result_count, record=None, carenet=None)``: takes a queryset, and formats it as valid 
      `RDF/XML <http://www.w3.org/TR/rdf-syntax-grammar/>`_ string.

    * ``to_xml(queryset, result_count, record=None, carenet=None)``: takes a queryset, and formats it as a valid 
      `XML <http://www.w3.org/TR/xml11/>`_ string.

    * ``to_json(queryset, result_count, record=None, carenet=None)``: takes a queryset, and formats it as a valid 
      `JSON <http://www.json.org/>`_ string.

    * ``to_sdmx(doc_etree)``: takes an etree, and returns another etree as a valid Simple Data Model XML.
      Actually, this method is not a serializer, but a preprocessor for the :ref:`SDMX <sdmx>` transform.

    In order to be called, the methods must be attached to that data model class by calling the
    ``attach_to_data_model()`` method.

    """

    @classmethod
    def attach_to_data_model(cls, data_model_cls):
        """ Add all of the defined methods as classmethods on ``data_model_cls``. """
        
        for attr_name in ATTACHABLE_ATTRS:
            attr_val = getattr(cls, attr_name, None)
            if attr_val:
                # unbind the method from our class
                def unbound_func_factory(unbound_func):
                    return lambda cls, *args, **kwargs: unbound_func(*args, **kwargs)

                # Wrap it as a classmethod
                cm = classmethod(unbound_func_factory(attr_val.__func__))

                # And bind it to our data model
                setattr(data_model_cls, attr_name, cm)
