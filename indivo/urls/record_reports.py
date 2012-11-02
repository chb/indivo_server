from django.conf.urls.defaults import *

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',
  (r'^minimal/measurements/(?P<lab_code>[^/]+)/$', 
   MethodDispatcher({'GET':measurement_list})),
  (r'^minimal/equipment/$', 
   MethodDispatcher({'GET':equipment_list})),
  (r'^experimental/ccr$', 
   MethodDispatcher({'GET':report_ccr})),
  (r'^(?P<data_model>[^/]+)/$', 
   MethodDispatcher({'GET':generic_list})),
)
