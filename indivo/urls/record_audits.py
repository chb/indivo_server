from django.conf.urls.defaults import *

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',
  #get audit
  (r'^$', audit_record_view), 
  (r'^documents/(?P<document_id>[^/]+)/$', audit_document_view), 
  (r'^documents/(?P<document_id>[^/]+)/functions/(?P<function_name>[^/]+)/$', audit_function_view)
)
