"""
Options processing and loading for Indivo medical data models.
"""

from indivo.serializers import DataModelSerializers
from indivo.validators import NonNullValidator

class DataModelOptions(object):
    """ Defines optional extra functionality for Indivo datamodels.

    To add options to a datamodel, subclass this class and override 
    its attributes. 

    Currently available options are:

    * *model_class_name*: **Required**. The name of the datamodel class 
      to attach to.

    * *serializers*: Custom serializers for the data model. Should be 
      set to a subclass of :py:class:`indivo.serializers.DataModelSerializers`.

    * *field_validators*: Custom validators for fields on the data model. A
      dictionary, where keys are field names on the model, and values are lists of
      `Django Validators <https://docs.djangoproject.com/en/1.2/ref/validators/>`_ 
      to be run against the field.

    """

    model_class_name = ''    
    serializers = None
    field_validators = {}

    @classmethod
    def attach(cls, data_model_class):
        """ Apply these options to a data model class.

        Attaches custom serializers and field validators.

        """
        
        if not cls.attach_p(data_model_class): return

        cls.attach_serializers(data_model_class)
        cls.attach_validators(data_model_class)

    @classmethod
    def attach_p(cls, data_model_class):
        """ True if these options should be applied to data_model_class.

        Right now, does ``cls.model_class_name`` match ``data_model_class.__name__``?
        
        """
        
        return cls.model_class_name == data_model_class.__name__

    @classmethod
    def attach_serializers(cls, data_model_class):
        if not cls.serializers: return # No custom serializers

        if issubclass(cls.serializers, DataModelSerializers):
            cls.serializers.attach_to_data_model(data_model_class)
        else:
            raise ValueError("Serializers must be defined on a custom subclass of indivo.serializers.DataModelSerializers")

    @classmethod
    def attach_validators(cls, data_model_class):
        if not cls.field_validators: return # No custom validators

        for field_name, validators in cls.field_validators.iteritems():
            field = data_model_class._meta.get_field(field_name)
            for v in validators:
                
                # We don't actually run NonNullValidators, we simply set blank=False
                # on the field, and let Django do the work
                if isinstance(v, NonNullValidator):
                    field.blank = False
                else:
                    field.validators.append(v)
