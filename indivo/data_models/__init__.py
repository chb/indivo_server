"""
Indivo DataModels
"""

import os, sys, inspect
from indivo.models import Fact
from indivo.lib import simpledatamodel
from indivo.serializers import DataModelSerializers

MODULE_NAME = 'model'
EXTRAS_NAME = 'extra'
EXTRAS_EXT = '.py'
MODULE_EXTENSIONS = ['.py', '.sdml']
MODEL_MODULES = {
    'core':'indivo.data_models.core',
    'contrib':'indivo.data_models.contrib',
    }

# Utilities to discover and load data models
def load_data_models(from_dir, target_module):
    """ Load all datamodels under *directory* into *module*. """
    loader = IndivoDataModelLoader(from_dir)
    loader.import_data_models(target_module)
    
def attach_filter_fields(cls):
    filters = {'created_at': ('created_at', 'date')}
    for field in cls._meta.local_fields:
        if field.serialize and field.rel is None:
            filters[field.name] = (field.name, 'string' )
    setattr(cls, 'filter_fields', filters)
    
class IndivoDataModelLoader(object):
    
    def __init__(self, top):
        self.top = top

    def import_data_models(self, target_module):
        for model_name, model_class in self.discover_data_models():
            self.add_model_to_module(model_name, model_class, target_module)

    @classmethod
    def detect_model_dir(cls, dir_path):
        """ Detects whether a directory is a properly-formatted datamodel.
        
        This is true if:
        
        * It contains a model file of an appropriate type
          (for now, .py or .sdml)
        
        * More to come later (maybe)
        
        *dir_path* MUST be an absolute path for this to work. Returns a tuple of
        (valid_p, fileroot, ext), where valid_p is True if the format is valid,
        fileroot is the name of the file containing the model definition (without 
        the extention), and ext is the extension. If no such file exists, returns
        (False, None, None). Returns the first valid definition format.
        
        """

        if os.path.isdir(dir_path):
            for ext in MODULE_EXTENSIONS:
                filename = MODULE_NAME + ext
                path = os.path.join(dir_path, filename)
                if os.path.isfile(path):
                    return (True, MODULE_NAME, ext)

        return (False, None, None)

    @classmethod
    def add_model_to_module(cls, model_name, model_class, module):

        # Check for conflicts in the namespaces
        if hasattr(module, model_name):
            raise ValueError("The module %s.%s already exists: Please choose a different name for your data model"% (module.__name__, model_name))

        setattr(module, model_name, model_class)
        all_list = getattr(module, '__all__', None)
        if all_list:
            all_list.append(model_name)
        else:
            module.__all__ = [model_name]

        # Make sure that the special Django '__module__' and 'app_label' attributes are set on the class
        model_class.__module__ =  module.__name__
        model_class.Meta.app_label = 'indivo'


    def discover_data_models(self):
        """ A generator for iterating over all valid datamodels below *toplevel_dir*.

        At each step, returns a tuple of (class_name, class), where class is a subclass of 
        indivo.models.Fact corresponding to a datamodel.

        If a model.py file fails to produce such a class, this function will silently 
        skip it.

        """

        for (dirpath, dirnames, filenames) in os.walk(self.top):
            valid_p, fileroot, ext = self.detect_model_dir(dirpath)
            if valid_p:
                dirnames = [] # we found a datamodel: don't look in subdirectories for others

                # Handle models based on their definition type
                if ext == '.py':
                    handler_func = self._discover_python_data_models
                elif ext == '.sdml':
                    handler_func = self._discover_sdml_data_models

                for name, cls in handler_func(dirpath, fileroot, ext):
                    attach_filter_fields(cls)
                    self.process_data_model_extras(dirpath, cls)
                    yield (name, cls)
                
    def _discover_python_data_models(self, dirpath, fileroot, ext):
        """ Imports a python module and extracts all Indivo Fact subclasses."""
        
        # add the model.py file to the path
        sys.path.insert(0, dirpath)

        # import the module
        try:
            module = __import__(fileroot)
        except ImportError:
            return # fail silently

        # move the module, but still save it, so that we don't lose references to
        # other modules imported by this one.
        #
        # The current namespace is just 'extra', since we imported straight
        # from the parent directory. Rename it something more unique.
        module_name = 'indivo.data_models.%s.%s'%(os.path.basename(dirpath),fileroot)
        sys.modules[module_name] = module
        del sys.modules[fileroot]
        
        # remove the module from the path
        sys.path.pop(0)

        # discover and yield classes in the module
        for name, cls in inspect.getmembers(module):
            if inspect.isclass(cls) and issubclass(cls, Fact) \
                    and cls != Fact: # Necessary because issubclass(Fact, Fact) evaluates to True                
                yield (name, cls)

    def _discover_sdml_data_models(self, dirpath, fileroot, ext):
        """ Reads in an SDML model definition and generates Indivo Fact subclasses."""

        # read the SDML definition in
        with open(os.path.join(dirpath, fileroot+ext)) as f:
            raw_data = f.read()

        # parse them into django models
        parser = simpledatamodel.SDML(raw_data)
        for cls in parser.get_output():
            yield (cls.__name__, cls)
                        
    def process_data_model_extras(self, dirpath, model_class):
        """ Processes extra options included in an extra.py file for a data model.

        For now, this is just a set of serializer implementations.
        
        """

        if os.path.exists(os.path.join(dirpath, "%s%s"%(EXTRAS_NAME, EXTRAS_EXT))):

            # add the extra.py file to the path
            sys.path.insert(0, dirpath)

            # import the module, if it exists
            try:
                module = __import__(EXTRAS_NAME)
            except ImportError:
                return # fail silently
            
            # move the module, but still save it, so that we don't lose references to
            # other modules imported by this one.
            #
            # The current namespace is just 'extra', since we imported straight
            # from the parent directory. Rename it something more unique.
            module_name = 'indivo.data_models.%s.%s'%(model_class.__name__, EXTRAS_NAME)
            sys.modules[module_name] = module
            del sys.modules[EXTRAS_NAME]

            # remove the module from the path
            sys.path.pop(0)

            # discover and process classes in the module
            for name, cls in inspect.getmembers(module):

                # Is it a Serializers class? Attach it.
                if inspect.isclass(cls) and issubclass(cls, DataModelSerializers) \
                        and cls != DataModelSerializers: # Necessary because issubclass(X, X) == True
                    cls(model_class).attach_to_data_model()

# Core data models
from core import *

# Extra installed data models
from contrib import *
