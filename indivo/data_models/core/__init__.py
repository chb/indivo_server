"""
Core Indivo Data Models
"""

import sys, os

# Import our core medical datamodels 
# (the ones that haven't been implemented in the new style yet)
from allergy               import Allergy
from simple_clinical_note  import SimpleClinicalNote
from equipment             import Equipment
from measurement           import Measurement
from immunization          import Immunization
from lab                   import Lab
from medication            import Medication
from procedure             import Procedure
from vitals                import Vitals

__all__ = [
    'Allergy',
    'SimpleClinicalNote',
    'Equipment',
    'Measurement',
    'Immunization',
    'Lab',
    'Medication',
    'Procedure',
    'Vitals',
    ]

# Autoload datamodels defined below this point
from indivo.data_models import IndivoDataModelLoader
this_dir = os.path.abspath(os.path.dirname(__file__))
this_module = sys.modules[__name__]

loader = IndivoDataModelLoader(this_dir)
loader.import_data_models(this_module)
