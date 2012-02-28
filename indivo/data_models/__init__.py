"""
Indivo DataModels
"""

import os, sys, inspect
from django.db.models import Model

MODULE_NAME = 'model'
MODULE_FILE = 'model.py'
MODEL_MODULE_NAMES = [
    'indivo.data_models.core',
    'indivo.data_models.contrib',
    ]

# Utilities to discover data models
class IndivoDataModelLoader(object):
    
    def __init__(self, top, core=True):
        self.core = core
        self.top = top

    def import_data_models(self, target_module):
        for model_name, model_class in self.discover_data_models():
            self.add_model_to_module(model_name, model_class, target_module)

    @classmethod
    def is_valid_data_model(cls, dir_path):
        """ Detects whether a directory is a properly-formatted datamodel.
        
        This is true if:
        
        * It contains a model.py file (maybe more to come later)
        
        *dir_path* MUST be an absolute path for this to work
        
        """

        module_path = os.path.join(dir_path, MODULE_FILE)
        return os.path.isdir(dir_path) and os.path.isfile(module_path)

    @classmethod
    def add_model_to_module(cls, model_name, model_class, module):
        setattr(module, model_name, model_class)
        all_list = getattr(module, '__all__', None)
        if all_list:
            all_list.append(model_name)
        else:
            module.__all__ = [model_name]


    def discover_data_models(self):
        """ A generator for iterating over all valid datamodels below *toplevel_dir*.

        At each step, returns a tuple of (class_name, class), where class is a subclass of 
        django.db.models.Model corresponding to a datamodel.

        If a model.py file fails to produce such a class, this function will silently 
        skip it.

        """
    
        for (dirpath, dirnames, filenames) in os.walk(self.top):
            if self.is_valid_data_model(dirpath):
                dirnames = [] # we found a datamodel: don't look in subdirectories for others
            
                # add the model.py file to the path
                sys.path.insert(0, dirpath)

                # import the module
                try:
                    module = __import__(MODULE_NAME)
                except ImportError:
                    continue # fail silently

                # now that we have the module, remove model.py from the path
                sys.path.pop(0)

                # discover and yield classes in the module
                for name, cls in inspect.getmembers(module):
                    if inspect.isclass(cls) and issubclass(cls, Model) \
                            and inspect.getmodule(cls).__name__ in MODEL_MODULE_NAMES:
                        yield (name, cls)
                        
# Core data models
from core import *

# Extra installed data models
from contrib import *
