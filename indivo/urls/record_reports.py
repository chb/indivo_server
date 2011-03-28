from django.conf.urls.defaults import *

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',
  (r'^minimal/measurements/(?P<lab_code>[^/]+)/$', measurement_list),
  (r'^minimal/immunizations/$', immunization_list),
  (r'^minimal/allergies/$', allergy_list),
  (r'^minimal/labs/$', lab_list),
  (r'^minimal/medications/$', medication_list),
  (r'^minimal/procedures/$', procedure_list),
  (r'^minimal/problems/$', problem_list),
  (r'^minimal/equipment/$', equipment_list),
  (r'^minimal/simple-clinical-notes/$', simple_clinical_notes_list),
  (r'^minimal/vitals/$', vitals_list),
  (r'^minimal/vitals/(?P<category>[^/]+)/$', vitals_list),
  (r'^experimental/ccr$', report_ccr),
)
