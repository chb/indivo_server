from django.conf.urls.defaults import *

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',
    (r'^$', MethodDispatcher({
                'DELETE' : carenet_delete})),
    (r'^/rename$', MethodDispatcher({
                'POST' : carenet_rename})),
    (r'^/record$', MethodDispatcher({'GET':carenet_record})),

    # Manage documents                      
    (r'^/documents/', include('indivo.urls.carenet_documents')),

    # Manage accounts
    (r'^/accounts/$',
                MethodDispatcher({
                  'GET'  : carenet_account_list, 
                  'POST' : carenet_account_create
                })),     
    (r'^/accounts/(?P<account_id>[^/]+)$', 
      MethodDispatcher({ 'DELETE' : carenet_account_delete })), 

    # Manage apps
    (r'^/apps/$', 
      MethodDispatcher({ 'GET' : carenet_apps_list})),
    (r'^/apps/(?P<pha_email>[^/]+)$', 
      MethodDispatcher({  'PUT' : carenet_apps_create,
                          'DELETE': carenet_apps_delete})),

    # Permissions Calls
    (r'^/accounts/(?P<account_id>[^/]+)/permissions$', 
      MethodDispatcher({ 'GET' : carenet_account_permissions })),
    (r'^/apps/(?P<pha_email>[^/]+)/permissions$', 
      MethodDispatcher({ 'GET' : carenet_app_permissions })),

    # Reporting Calls                      
    (r'^/reports/minimal/immunizations/$', 
     MethodDispatcher({'GET':carenet_immunization_list})), 
    (r'^/reports/minimal/allergies/$',
     MethodDispatcher({'GET':carenet_allergy_list})), 
    (r'^/reports/minimal/procedures/$',
     MethodDispatcher({'GET':carenet_procedure_list})), 
    (r'^/reports/minimal/labs/$',
     MethodDispatcher({'GET':carenet_lab_list})), 
    (r'^/reports/minimal/simple-clinical-notes/$',
     MethodDispatcher({'GET':carenet_simple_clinical_notes_list})), 
    (r'^/reports/minimal/problems/$',
     MethodDispatcher({'GET':carenet_problem_list})), 
    (r'^/reports/minimal/medications/$',
     MethodDispatcher({'GET':carenet_medication_list})), 
    (r'^/reports/minimal/equipment/$',
     MethodDispatcher({'GET':carenet_equipment_list})), 
    (r'^/reports/minimal/vitals/$', 
     MethodDispatcher({'GET':carenet_vitals_list})), 
    (r'^/reports/minimal/vitals/(?P<category>[^/]+)$',
     MethodDispatcher({'GET':carenet_vitals_list})), 
    (r'^/reports/minimal/measurements/(?P<lab_code>[^/]+)/$',
     MethodDispatcher({'GET':carenet_measurement_list})),
)
