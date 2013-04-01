from django.conf.urls import patterns

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',

  # Old style audit views, supported for backwards compatibility
  (r'^$', MethodDispatcher({'GET':audit_record_view})), 
  (r'^documents/(?P<document_id>[^/]+)/$', 
   MethodDispatcher({'GET':audit_document_view})), 
  (r'^documents/(?P<document_id>[^/]+)/functions/(?P<function_name>[^/]+)/$', 
   MethodDispatcher({'GET':audit_function_view})),

  # Audit Using the Query API Interface
  (r'^query/$', MethodDispatcher({'GET':audit_query}))
)