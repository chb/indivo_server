from django.conf.urls.defaults import *

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',
  (r'^$', MethodDispatcher({'GET':record_phas})),
  (r'^(?P<pha_email>[^/]+)$', 
      MethodDispatcher({'GET' : record_pha, 
                        'PUT': record_pha_enable,
                        'DELETE': pha_record_delete})),
  
  # List of app-specific documents / create a doc
  (r'^(?P<pha_email>[^/]+)/documents/$', 
      MethodDispatcher({
              'GET'  : record_app_document_list,
              'POST' : record_app_document_create})),
  
  # create app-specific doc by document external ID
  (r'^(?P<pha_email>[^/]+)/documents/external/(?P<external_id>[^/]+)$', 
      MethodDispatcher({
              'GET' : record_app_document_ext, 
              'POST' : record_app_document_create_or_update_ext, 
              'PUT'  : record_app_document_create_or_update_ext})),

  # One app-specific document
  (r'^(?P<pha_email>[^/]+)/documents/(?P<document_id>[^/]+)$', MethodDispatcher({
                'GET': record_app_document,
                'DELETE': record_app_document_delete})),

  # One app-specific document's metadata
  (r'^(?P<pha_email>[^/]+)/documents/(?P<document_id>[^/]+)/meta$', 
      MethodDispatcher({'GET': record_app_document_meta})),

  # app-specific document metadata by external ID 
  (r'^(?P<pha_email>[^/]+)/documents/external/(?P<external_id>[^/]+)/meta$', 
      MethodDispatcher({'GET': record_app_document_meta_ext})),

  # app-specific set document label
  (r'^(?P<pha_email>[^/]+)/documents/(?P<document_id>[^/]+)/label$', 
   MethodDispatcher({'PUT':record_app_document_label})),

  # app-specific document types
  # (r'^(?P<pha_email>[^/]+)/documents/types/(?P<type>[A-Za-z0-9._%-:#]+)/$', record_app_document_list_by_type),
  # REMOVED 02/15/2011 for compatibility with record-specific doc access: type is now only passed as a GET param,
  # i.e. GET /{pha_email}/documents/?type={TYPE}

  # setup a PHA completely (pre-auth'ed)
  (r'^(?P<pha_email>[^/]+)/setup$', 
   MethodDispatcher({'POST':record_pha_setup})),
)
