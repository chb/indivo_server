"""
Contributed Indivo DataModels
"""

import sys, os

# Autoload datamodels defined in this package
from indivo.data_models import IndivoDataModelLoader
this_dir = os.path.abspath(os.path.dirname(__file__))
this_module = sys.modules[__name__]

loader = IndivoDataModelLoader(this_dir, module='contrib')
loader.import_data_models(this_module)
