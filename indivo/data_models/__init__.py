"""
Indivo DataModels
"""

import os, sys, inspect
from django.db.models import Model

MODULE_NAME = 'model'
MODULE_EXTENSIONS = ['.py', '.isj']
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
    def detect_model_dir(cls, dir_path):
        """ Detects whether a directory is a properly-formatted datamodel.
        
        This is true if:
        
        * It contains a model file of an appropriate type
          (for now, .py or .isj)
        
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
            valid_p, fileroot, ext = self.detect_model_dir(dirpath)
            if valid_p:
                dirnames = [] # we found a datamodel: don't look in subdirectories for others

                # Handle models based on their definition type
                if ext == '.py':
                    handler_func = self._discover_python_data_models
                elif ext == '.isj':
                    handler_func = self._discover_isj_data_models

                for name, cls in handler_func(dirpath, fileroot, ext):
                    yield (name, cls)
                
    def _discover_python_data_models(self, dirpath, fileroot, ext):
        """ Imports a python module and extracts all Django Model subclasses."""
        
        # add the model.py file to the path
        sys.path.insert(0, dirpath)
        
        # import the module
        try:
            module = __import__(fileroot)
        except ImportError:
            return # fail silently

        # now that we have the module, remove model.py from the path
        sys.path.pop(0)

        # discover and yield classes in the module
        for name, cls in inspect.getmembers(module):
            if inspect.isclass(cls) and issubclass(cls, Model) \
                    and inspect.getmodule(cls).__name__ in MODEL_MODULE_NAMES:
                yield (name, cls)

    def _discover_isj_data_models(self, dirpath, fileroot, ext):
        """ Reads in an ISJ model definition and generates Django Model subclasses."""

        # TODO
        pass
                        
# Core data models
from core import *

# Extra installed data models
from contrib import *
