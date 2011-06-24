from django.conf.urls.defaults import *

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',
    ##
    ## Application-Specific Data Storage
    ##

    # List of app-specific documents / create a doc
    (r'^/documents/$', 
      MethodDispatcher({ 'GET': app_document_list, 'POST': app_document_create})),

    # create app-specific doc by document external ID
    (r'^/documents/external/(?P<external_id>[^/]+)$', 
      MethodDispatcher({'PUT': app_document_create_or_update_ext})),

    # One app-specific document
    # app-specific document replace
    (r'^/documents/(?P<document_id>[^/]+)$', 
      MethodDispatcher({'GET': app_specific_document, 
                        'PUT': app_document_create_or_update, 
                        'DELETE': app_document_delete})),

    # update
    (r'^/documents/(?P<document_id>[^/]+)/update$', app_document_update),

    # One app-specific document's metadata
    # and app-specific document metadata by external ID
    (r'^/documents/(?P<document_id>[^/]+)/meta$', 
      MethodDispatcher({'GET': app_document_meta})),
    (r'^/documents/external/(?P<external_id>[^/]+)/meta$', 
      MethodDispatcher({'GET': app_document_meta_ext})),

    # app-specific document label
    # FIXME: not sure this view works
    (r'^/documents/(?P<document_id>[^/]+)/label$', app_document_label),

    # app-specific document types
    # (r'^/documents/types/(?P<type>[A-Za-z0-9._%-:#]+)/$', app_document_list_by_type)
    # REMOVED 02/15/2011 for compatibility with record-specific document type calls
    # Type must be passed as a get parameter, i.e. GET /documents/?type={TYPE}
)
