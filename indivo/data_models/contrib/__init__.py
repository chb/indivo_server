"""
Contributed Indivo DataModels
"""

from django.conf import settings
import sys

# Autoload contributed datamodels
from indivo.data_models import load_data_models
this_module = sys.modules[__name__]

for data_model_dir in settings.CONTRIB_DATAMODEL_DIRS:
    load_data_models(data_model_dir, this_module)
