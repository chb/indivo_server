from django.conf.urls.defaults import *

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',
  (r'^minimal/measurements/(?P<lab_code>[^/]+)/$', 
   MethodDispatcher({'GET':measurement_list})),
  (r'^minimal/immunizations/$', 
   MethodDispatcher({'GET':immunization_list})),
  (r'^minimal/allergies/$', 
   MethodDispatcher({'GET':allergy_list})),
  (r'^minimal/labs/$', 
   MethodDispatcher({'GET':lab_list})),
  (r'^minimal/medications/$', 
   MethodDispatcher({'GET':medication_list})),
  (r'^minimal/procedures/$', 
   MethodDispatcher({'GET':procedure_list})),
  (r'^minimal/problems/$', 
   MethodDispatcher({'GET':problem_list})),
  (r'^minimal/equipment/$', 
   MethodDispatcher({'GET':equipment_list})),
  (r'^minimal/simple-clinical-notes/$', 
   MethodDispatcher({'GET':simple_clinical_notes_list})),
  (r'^minimal/vitals/$', 
   MethodDispatcher({'GET':vitals_list})),
  (r'^minimal/vitals/(?P<category>[^/]+)/$', 
   MethodDispatcher({'GET':vitals_list})),
  (r'^experimental/ccr$', 
   MethodDispatcher({'GET':report_ccr})),
  (r'^(?P<model_name>[^/]+)/$', 
   MethodDispatcher({'GET':simple_data_model_list})),
)
