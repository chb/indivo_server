from django.conf.urls import patterns

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',
    ##
    ## Application-Specific Data Storage
    ##

    # Manifest for the app, SMART style
    (r'^/manifest$', MethodDispatcher({'GET':app_manifest})),

    # List of app-specific documents / create a doc
    (r'^/documents/$', 
      MethodDispatcher({ 'GET': app_document_list, 'POST': app_document_create})),

    # create app-specific doc by document external ID
    (r'^/documents/external/(?P<external_id>[^/]+)$', 
      MethodDispatcher({'PUT': app_document_create_or_update_ext,
                        'GET': app_document_ext})),

    # One app-specific document
    # app-specific document replace
    (r'^/documents/(?P<document_id>[^/]+)$', 
      MethodDispatcher({'GET': app_document, 
                        'PUT': app_document_create_or_update, 
                        'DELETE': app_document_delete})),

    # One app-specific document's metadata
    # and app-specific document metadata by external ID
    (r'^/documents/(?P<document_id>[^/]+)/meta$', 
      MethodDispatcher({'GET': app_document_meta})),
    (r'^/documents/external/(?P<external_id>[^/]+)/meta$', 
      MethodDispatcher({'GET': app_document_meta_ext})),

    # app-specific document label
    # FIXME: not sure this view works
    (r'^/documents/(?P<document_id>[^/]+)/label$', 
     MethodDispatcher({'PUT':app_document_label})),

    # List available records
    # (autonomous apps only)
    (r'^/records/$', MethodDispatcher({'GET':app_record_list})),

    # Get an access token for an enabled record
    # (autonomous apps only!!!!!)
    # POST, for compatibility with other oAuth calls
    (r'^/records/(?P<record_id>[^/]+)/access_token$', MethodDispatcher({'POST': autonomous_access_token})),

    # app-specific document types
    # (r'^/documents/types/(?P<type>[A-Za-z0-9._%-:#]+)/$', app_document_list_by_type)
    # REMOVED 02/15/2011 for compatibility with record-specific document type calls
    # Type must be passed as a get parameter, i.e. GET /documents/?type={TYPE}
)
