"""
Library functions for parsing and generating Simple Data Model (SDM) definitions and data.

"""

try:
    from django.utils import simplejson
except ImportError:
    try:
        import simplejson
    except ImportError:
        raise ImportError("Couldn't find an installation of SimpleJSON")

from django.db import models
from django.db.models.fields import FieldDoesNotExist
from indivo.models import Fact
from lxml import etree
from indivo.lib import iso8601

SDM_TYPES = {
    'Date': (models.DateTimeField, {'null':True}),
    'String': (models.CharField, {'max_length': 255, 'null':True}),
    'Number': (models.FloatField, {'null':True}),
}

MODEL_NAME_KEY = '__modelname__'

MODEL_SUPERCLASSES = (Fact,)

class SDMJ(object):
    """ A base class for parsing SDMJ. 

    Usage of subclasses looks like:
    >>> parser = SDMJSubclass()
    >>> for django_obj in parser.get_output(): do_stuff()
    
    """
    
    def __init__(self, data_string):
        self.parsed_data = simplejson.loads(data_string)
        if not isinstance(self.parsed_data, list): # Allow lists of SMDJ objects in one string
            self.parsed_data = [self.parsed_data]

        self.output_objects = []

    def _parse(self):
        """ A generator to transform SDMJ data into Django objects.

        Subclasses should parse the SDMJ in self.parsed_data and yield Django objects.

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

test_sdmj_definition = '''
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

class SDMJSchema(SDMJ):
    """ A class for parsing SDMJ definitions and building them as Django Model Subclasses. """

    def _parse(self):
        """ Parses the definition string into Django model definitions """

        # Add our toplevel SDMJ definitions to the stack
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
            raise SDMJSchemaException("All model definitions must specify a name, using the '%s' key"%MODEL_NAME_KEY)
        del parsed_def[MODEL_NAME_KEY]
        model_name = str(model_name) # Eliminate any unicode weirdness

        for attrname, attrval in parsed_def.iteritems():
            attrname = str(attrname) # Eliminate unicode weirdness

            if isinstance(attrval, list):
                # OneToMany Relationship: we save the subobject for later parsing.
                # We don't create any fields on our model--we just tell the subobject
                # to add a foreign key to us.
                if len(attrval) != 1:
                    raise SDMJSchemaException("OneToMany Relationships may only define one target relation model")
                
                # build the foreignkey that the submodel should add (pointing at our model)
                submodel_fk = models.ForeignKey(model_name, related_name=attrname)

                # Add the submodel definition and requested key to the list
                subdefs_to_parse.append((attrval[0], submodel_fk))

            elif isinstance(attrval, dict):
                # OnetoOne Relationship: we save the subobject for later parsing,
                # and create a OneToOne field from us to them

                # get the submodel's name
                try:
                    submodel_name = str(attrval[MODEL_NAME_KEY])
                except KeyError:
                    raise SDMJSchemaException("All model definitions must specify a name, using the '%s' key"%MODEL_NAME_KEY)

                # create the OneToOne field
                # The related name is by default the lowercased name of our model.
                # Might want to re-examine this at some point.
                fields[attrname] = models.OneToOneField(submodel_name)
                
                # Save the submodel for later parsing
                subdefs_to_parse.append((attrval, None))

            else:
                # Simple type: we simply create the relevant field
                try:
                    field_class, args = SDM_TYPES[attrval]
                except KeyError:
                    raise SDMJSchemaException("Invalid SDM type: %s" % str(attrval))

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

        # Add special Django-specific model attrs: placeholder, will be overwritten when the model is imported
        fields['__module__'] = 'indivo.data_models.tmp'

        # Now build the Django Model class
        klass = type(str(model_name), MODEL_SUPERCLASSES, fields)

        # And we're done!
        return (subdefs_to_parse, klass)        

test_sdmj_document = '''
{
    "__modelname__": "Medication",
    "name": "ibuprofen",
    "date_started": "2010-10-01T00:00:00Z",
    "date_stopped": "2010-10-31T00:00:00Z",
    "brand_name": "Advil",
    "route": "Oral",
    "prescription": {
        "__modelname__": "Prescription"
        "prescribed_by_name": "Kenneth D. Mandl",
        "prescribed_by_institution": "Children's Hospital Boston",
        "prescribed_on": "2010-09-30T00:00:00Z",
        "prescribed_stop_on": "2010-10-31T00:00:00Z"
    },
    "fills": [
        {
            "__modelname__": "Fill"
            "date_filled": "2010-10-01T00:00:00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        },
        {
            "__modelname__": "Fill"
            "date_filled": "2010-10-16T00:00:00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        }
    ]
}
'''

class SDMJData(SDMJ):
    """ A class for parsing SDMJ data, and building it into Django Model instances. """

    def _parse(self):
        """ Parses the data string into Django model instances. """

        # Add our toplevel SDMJ documents to the stack
        parse_stack = []
        for toplevel_model_instance in self.parsed_data:
            parse_stack.append((toplevel_model_instance, None, None, None))

        # Parse until the stack is empty
        while parse_stack:
            next = parse_stack.pop()
            subdefs_to_parse, model_instance = self._parse_one(*next)
                
            # Add the submodels to our stack
            parse_stack.extend(subdefs_to_parse)

            # Yield the model instance we just created
            yield model_instance

    def _parse_one(self, instance_dict, rel_parent_obj=None, rel_fieldname=None, rel_to_parent=False):
        """ Build one Django model instance.
        
        rel_parent_obj, rel_fieldname, and rel_to_parent, if provided, are instructions to set up a 
        reference to the parent object. Rel_fieldname is the field on which to create the reference,
        and rel_on_parent indicates which direction the reference should go (child to parent for a
        manytomany relationship, parent to child for a onetoone relationship).

        Returns a tuple of (subdefs_to_parse, parsed_instance), where subdefs_to_parse is a list
        of subobjects that need parsing, and parsed_instance is an instance of the 
        django.db.models.Model subclass we have just parsed. List elements of subdefs_to_parse are 
        tuples of (instance_etree, rel_parent_obj, rel_fieldname, rel_to_parent), appropriate for passing 
        back into this function.
        
        """

        subobjs_found = []
        subdefs_to_parse = []
        fields = {}

        # Pull out our model's name first, so we can pass it into submodels as needed.
        model_name = instance_dict.get(MODEL_NAME_KEY, None)
        if not model_name:
            raise SDMDataException("All SDM data instances must specify the model they belong to.")
        del instance_dict[MODEL_NAME_KEY]
     
        try:
            model_class = getattr(__import__('indivo.models', fromlist=[str(model_name)]), model_name, None)
        except ImportError:
            model_class = None
        finally:
            if not model_class:
                raise SDMDataException("SDM model specified a non-existent data-model: %s"%model_name)

        for fieldname, raw_value in instance_dict.iteritems():
            if isinstance(raw_value, list):
                # OneToMany Field: we save the subobjects for later parsing.
                # We tell the subobject to add a reference to our instance on a field
                # named after the lowercase of our modelname.
                for subobject_dict in raw_value:                
                    subobjs_found.append((subobject_dict, model_name.lower(), True))

            elif isinstance(raw_value, dict):
                # OnetoOne Field: we save the subobject for later parsing.
                # We tell the subobject to add a reference from our instance to them
                subobjs_found.append((raw_value, fieldname, False))

            else:
                # Simple Field: we validate the datatype, then add the data to our model

                # get the field definition on the class
                try:
                    model_field = model_class._meta.get_field(fieldname)
                except FieldDoesNotExist:
                    model_field = None

                if not model_field:
                    raise SDMDataException("Non-existent data field: %s"%fieldname)
                
                if not raw_value:
                    fields[fieldname] = None
                
                else:

                    # since everything is coming in as a string, try converting to native Django types
                    if isinstance(model_field, models.DateField):
                        try:
                            value = iso8601.parse_utc_date(raw_value)
                        except Exception as e:
                            raise SDMDataException("SDM data for field %s should have been an iso8601 datetime: got %s instead"%(fieldname, raw_value))

                    elif isinstance(model_field, models.FloatField) and raw_value:
                        try:
                            value = float(raw_value)
                        except Exception as e:
                            raise SDMDataException("SDM data for field %s should have been numeric: got %s instead"%(fieldname, raw_value))
                    else:
                        value = raw_value
 
                    fields[fieldname] = value

        # Add a reference from us to them, if we were asked to.
        # We'll need to save the parent object first, so it has an ID
        if rel_parent_obj and rel_to_parent:
            if not rel_parent_obj.id:
                rel_parent_obj.save()
            fields[rel_fieldname] = rel_parent_obj

        # Now build the Django Model instance
        instance = model_class(**fields)

        # Add a reference from them to us, if we were asked to.
        # We'll need to save ourselves first, so we have an ID.
        if rel_parent_obj and not rel_to_parent:
            instance.save()
            setattr(rel_parent_obj, rel_fieldname, instance)

        # Add ourselves as the parent to all of our subinstances
        for subobj_dict, subobj_field, subobj_direction in subobjs_found:
            subdefs_to_parse.append((subobj_dict, instance, subobj_field, subobj_direction))

        # And we're done!
        return (subdefs_to_parse, instance)        

test_sdmx_document = '''
<Models>
  <Model name="TestMed">
    <Field name="date_started">2010-10-01T00:00:00Z</Field>
    <Field name="name">ibuprofen</Field>
    <Field name="brand_name">Advil</Field>
    <Field name="frequency">14</Field>
    <Field name="prescription">
      <Model name="TestPrescription">
        <Field name="prescribed_by_name">Kenneth D. Mandl</Field>
        <Field name="prescribed_on">2010-09-30T00:00:00Z</Field>
      </Model>
    </Field>
    <Field name="fills">
      <Models>
        <Model name="TestFill">
          <Field name="date_filled">2010-10-01T00:00:00Z</Field>
          <Field name="supply_days">15</Field>
        </Model>
        <Model name="TestFill">
          <Field name="date_filled">2010-10-16T00:00:00Z</Field>
          <Field name="supply_days">15</Field>
        </Model>
      </Models>
    </Field>
  </Model>
</Models>
'''

class SDMXData(object):
    """ A base class for parsing SDMX data, and building it into Django Model instances. """

    def __init__(self, data_etree):
        self.raw_etree = data_etree
        self.output_objects = []

    def get_output(self):

        # only parse once
        if self.output_objects:
            for django_obj in self.output_objects:
                yield django_obj
        
        else:
            for django_obj in self._parse():
                self.output_objects.append(django_obj)
                yield django_obj

    def _parse(self):
        """ Parses the data etree into Django model instances """

        # Add our toplevel SDMX documents to the stack
        parse_stack = []
        for toplevel_model_instance in self.raw_etree.getroot():
            parse_stack.append((toplevel_model_instance, None, None, None))

        # Parse until the stack is empty
        while parse_stack:
            next = parse_stack.pop()
            subdefs_to_parse, model_instance = self._parse_one(*next)
                
            # Add the submodels to our stack
            parse_stack.extend(subdefs_to_parse)

            # Yield the model instance we just created
            yield model_instance

    def _parse_one(self, instance_etree, rel_parent_obj=None, rel_fieldname=None, rel_to_parent=False):
        """ Build one Django model instance.
        
        rel_parent_obj, rel_fieldname, and rel_to_parent, if provided, are instructions to set up a 
        reference to the parent object. Rel_fieldname is the field on which to create the reference,
        and rel_on_parent indicates which direction the reference should go (child to parent for a
        manytomany relationship, parent to child for a onetoone relationship).

        Returns a tuple of (subdefs_to_parse, parsed_instance), where subdefs_to_parse is a list
        of subobjects that need parsing, and parsed_instance is an instance of the 
        django.db.models.Model subclass we have just parsed. List elements of subdefs_to_parse are 
        tuples of (instance_etree, rel_parent_obj, rel_fieldname, rel_to_parent), appropriate for passing 
        back into this function.
        
        """

        subobjs_found = []
        subdefs_to_parse = []
        fields = {}

        # Pull out our model's name first, so we can pass it into submodels as needed.
        model_name = instance_etree.get('name', None)
        if not model_name:
            raise SDMDataException("All SDM data instances must specify the model they belong to.")
     
        try:
            model_class = getattr(__import__('indivo.models', fromlist=[model_name]), model_name, None)
        except ImportError:
            model_class = None
        finally:
            if not model_class:
                raise SDMDataException("SDM model specified a non-existent data-model: %s"%model_name)

        for field_etree in instance_etree.findall('Field'):
            fieldname = field_etree.get('name', None)
            if not fieldname:
                raise SDMDataException("All SDM data fields must specify a fieldname.")

            if field_etree.find('Models') is not None:
                # OneToMany Field: we save the subobjects for later parsing.
                # We tell the subobject to add a reference to our instance on a field
                # named after the lowercase of our modelname.
                for subobject_etree in field_etree.find('Models').findall('Model'):                
                    subobjs_found.append((subobject_etree, model_name.lower(), True))

            elif field_etree.find('Model') is not None:
                # OnetoOne Field: we save the subobject for later parsing.
                # We tell the subobject to add a reference from our instance to them
                subobjs_found.append((field_etree.find('Model'), fieldname, False))

            else:
                # Simple Field: we validate the datatype, then add the data to our model

                # get the field definition on the class
                try:
                    model_field = model_class._meta.get_field(fieldname)
                except FieldDoesNotExist:
                    model_field = None

                if not model_field:
                    raise SDMDataException("Non-existent data field: %s"%fieldname)
                raw_value = field_etree.text
                
                if not raw_value:
                    fields[fieldname] = None
                
                else:

                    # since everything is coming in as a string, try converting to native Django types
                    if isinstance(model_field, models.DateField):
                        try:
                            value = iso8601.parse_utc_date(raw_value)
                        except Exception as e:
                            raise SDMDataException("SDM data for field %s should have been an iso8601 datetime: got %s instead"%(fieldname, raw_value))

                    elif isinstance(model_field, models.FloatField) and raw_value:
                        try:
                            value = float(raw_value)
                        except Exception as e:
                            raise SDMDataException("SDM data for field %s should have been numeric: got %s instead"%(fieldname, raw_value))
                    else:
                        value = raw_value
 
                    fields[fieldname] = value

        # Add a reference from us to them, if we were asked to.
        # We'll need to save the parent object first, so it has an ID
        if rel_parent_obj and rel_to_parent:
            if not rel_parent_obj.id:
                rel_parent_obj.save()
            fields[rel_fieldname] = rel_parent_obj

        # Now build the Django Model instance
        instance = model_class(**fields)

        # Add a reference from them to us, if we were asked to.
        # We'll need to save ourselves first, so we have an ID.
        if rel_parent_obj and not rel_to_parent:
            instance.save()
            setattr(rel_parent_obj, rel_fieldname, instance)

        # Add ourselves as the parent to all of our subinstances
        for subobj_etree, subobj_field, subobj_direction in subobjs_found:
            subdefs_to_parse.append((subobj_etree, instance, subobj_field, subobj_direction))

        # And we're done!
        return (subdefs_to_parse, instance)        

class SDMException(ValueError):
    prefix = "" # subclasses should define this

    def __init__(self, msg):
        super(SDMException, self).__init__(self.prefix + msg)
    
class SDMJSchemaException(SDMException):
    prefix = "Invalid SDM model definition: "

class SDMDataException(SDMException):
    prefix = "Invalid SDM data: "

