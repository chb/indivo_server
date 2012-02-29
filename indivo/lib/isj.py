"""
Library functions for parsing and generating Indivo-Specific JSON (ISJ)

"""

try:
    from django.utils import simplejson
except ImportError:
    try:
        import simplejson
    except ImportError:
        raise ImportError("Couldn't find an installation of SimpleJSON")

from django.db import models
from indivo.models import Fact

test_isj_definition = '''
{
    "__modelname__": "Medication",
    "name": "String",
    "date_started": "Date",
    "date_stopped": "Date",
    "brand_name": "String", 
    "route": "String",
    "prescription": {
        "__modelname__": "Prescription",
        "prescribed_by_name": "String",
        "prescribed_by_institution": "String",
        "prescribed_on": "Date",
        "prescribed_stop_on": "Date"
        },
    "fills": [{
            "__modelname__": "Fill",
            "date_filled": "Date",
            "supply_days": "Number",
            "filled_at_name": "String"
            }]
}
'''
   
test_isj_document = '''
{
    "__modelname__": "Medication",
    "name": "ibuprofen",
    "date_started": "10-01-2010T00:00:00Z",
    "date_stopped": "10-31-2010T00:00:00Z",
    "brand_name": "Advil",
    "route": "Oral",
    "prescription": {
        "prescribed_by_name": "Kenneth D. Mandl",
        "prescribed_by_institution": "Children'sHospitalBoston",
        "prescribed_on": "09-30-2010T00: 00: 00Z",
        "prescribed_stop_on": "10-31-2010T00: 00: 00Z"
    },
    "fills": [
        {
            "date_filled": "10-01-2010T00: 00: 00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        },
        {
            "date_filled": "10-16-2010T00: 00: 00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        }
    ]
}
'''

ISJ_TYPES = {
    'Date': (models.DateTimeField, {'null':True}),
    'String': (models.CharField, {'max_length': 255, 'null':True}),
    'Number': (models.FloatField, {}),
}

MODEL_NAME_KEY = '__modelname__'

MODEL_SUPERCLASSES = (Fact,)

class ISJ(object):
    """ A base class for parsing ISJ. 

    Usage of subclasses looks like:
    >>> parser = ISJSubclass()
    >>> django_objs = parser.get_output()
    
    """
    
    def __init__(self, data_string, module_name):
        self.parsed_data = simplejson.loads(data_string)
        if not isinstance(self.parsed_data, list): # Allow lists of ISJ objects in one string
            self.parsed_data = [self.parsed_data]

        self.module_name = module_name
        self.output_objects = []

    def _parse(self):
        """ A generator to transform ISJ data into Django objects.

        Subclasses should parse the ISJ in self.parsed_data and yield Django objects.

        """
        raise NotImplementedError()

    def get_output(self):

        # only parse once
        if self.output_objects:
            for django_obj in self.output_objects:
                yield django_obj
        
        else:
            for django_obj in self._parse():
                self.output_objects.append(django_obj)
                yield django_obj

class ISJSchema(ISJ):
    """ A class for parsing ISJ definitions and building them as Django Model Subclasses. """

    def _parse(self):
        """ Parses the definition string into Django model definitions """

        # Add our toplevel ISJ definitions to the stack
        parse_stack = []
        for toplevel_model_def in self.parsed_data:
            parse_stack.append((toplevel_model_def, None))

        # Parse until the stack is empty
        while parse_stack:
            next = parse_stack.pop()
            subdefs_to_parse, model_class = self._parse_one(*next)
                
            # Add the submodels to our stack
            parse_stack.extend(subdefs_to_parse)

            # Yield the model_class we just created
            yield model_class

    def _parse_one(self, parsed_def, foreign_key=None):
        """ Build one Django model definition.
        
        foreign_keys is a list of django.db.models.ForeignKey objects that should be added
        to the new model.

        Returns a tuple of (subdefs_to_parse, model_def), where subdefs_to_parse is a list
        of subobjects that need parsing, and model_def is a django.db.models.Model subclass
        defined by the original parsed_def. list elements of subdefs_to_parse are tuples of
        (definition, foreign_key), appropriate for passing back into this function.
        
        """

        subdefs_to_parse = []
        fields = {}

        # Pull out our model's name first, so we can pass it into submodels as needed.
        model_name = parsed_def.get(MODEL_NAME_KEY, None)
        if not model_name:
            raise ISJSchemaException("All model definitions must specify a name, using the '%s' key"%MODEL_NAME_KEY)
        del parsed_def[MODEL_NAME_KEY]

        for attrname, attrval in parsed_def.iteritems():
            if isinstance(attrval, list):
                # OneToMany Relationship: we save the subobject for later parsing.
                # We don't create any fields on our model--we just tell the subobject
                # to add a foreign key to us.
                if len(attrval) != 1:
                    raise ISJSchemaException("OneToMany Relationships may only define one target relation model")
                
                # build the foreignkey that the submodel should add (pointing at our model)
                submodel_fk = models.ForeignKey(model_name, related_name=attrname)

                # Add the submodel definition and requested key to the list
                subdefs_to_parse.append((attrval[0], submodel_fk))

            elif isinstance(attrval, dict):
                # OnetoOne Relationship: we save the subobject for later parsing,
                # and create a OneToOne field from us to them

                # get the submodel's name
                try:
                    submodel_name = attrval[MODEL_NAME_KEY]
                except KeyError:
                    raise ISJSchemaException("All model definitions must specify a name, using the '%s' key"%MODEL_NAME_KEY)

                # create the OneToOne field
                # The related name is by default the lowercased name of our model.
                # Might want to re-examine this at some point.
                fields[attrname] = models.OneToOneField(submodel_name)
                
                # Save the submodel for later parsing
                subdefs_to_parse.append((attrval, None))

            else:
                # Simple type: we simply create the relevant field
                try:
                    field_class, args = ISJ_TYPES[attrval]
                except KeyError:
                    raise ISJSchemaException("Invalid ISJ type: %s" % str(attrval))

                fields[attrname] = field_class(**args)

        # Add the foreign_key, if we were asked to
        # We'll name the foreign_key after the lowercased name of the model we're pointing
        # at (for now).
        if foreign_key:
            fk_target = foreign_key.rel.to # this might be a string or the class itself
            if hasattr(fk_target, 'lower'):
                fk_name = fk_target.lower()
            else:
                fk_name = fk_target.__name__.lower()
            fields[fk_name] = foreign_key

        # Add special Django-specific model attrs
        fields['__module__'] = self.module_name

        # Now build the Django Model class
        klass = type(str(model_name), MODEL_SUPERCLASSES, fields)

        # And we're done!
        return (subdefs_to_parse, klass)        

class ISJData(ISJ):
    """ A class for parsing ISJ data, and building it into Django Model instances. """
    
    def _parse(self):
        # TODO
        pass

class ISJException(ValueError):
    prefix = "" # subclasses should define this

    def __init__(self, msg):
        super(ISJException, self).__init__(self.prefix + msg)
    
class ISJSchemaException(ISJException):
    prefix = "Invalid ISJ model definition: "

class ISJDataException(ISJException):
    prefix = "Invalid ISJ data: "
