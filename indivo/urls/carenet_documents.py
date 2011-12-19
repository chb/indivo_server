from django.conf.urls.defaults import *

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns(
    '',
    (r'^$',                             
     MethodDispatcher({'GET' : carenet_document_list })), 
    (r'^(?P<document_id>[^/]+)/meta$',  
     MethodDispatcher({'GET' : carenet_document_meta})),
    (r'^(?P<document_id>[^/]+)$',       
     MethodDispatcher({'GET' : carenet_document })), 

    # special documents
    (r'^special/(?P<special_document>[^/]+)$', MethodDispatcher(
            {'GET' : read_special_document_carenet})),
)

"""
    (r'^(?P<document_id>[^/]+)/carenets/$', MethodDispatcher({
                'GET' : document_carenets
                })), 
    (r'^(?P<document_id>[^/]+)/carenets/(?P<carenet_id>[^/]+)$', MethodDispatcher({
                'PUT' : carenet_document_placement, 
                'DELETE' : carenet_document_delete
                })), 
    (r'^(?P<document_id>[^/]+)/carenets/(?P<carenet_id>[^/]+/autoshare-revert)$', MethodDispatcher({
                'POST' : autoshare_revert
                })), 


    # document list
    (r'^$', MethodDispatcher({
                'GET': document_list,
                'POST': document_create,
                'DELETE' : documents_delete})),

    # create by document external ID
    #(r'^/documents/external/(?P<external_id>[^/]+)$', MethodDispatcher({'POST' : document_create})),
    (r'^external/(?P<pha_email>[^/]+)/(?P<external_id>[^/]+)$', 
      MethodDispatcher({'PUT' : document_create})),
    
    # single document
    (r'^(?P<document_id>[^/]+)$', MethodDispatcher({'GET': document, 'DELETE': document_delete})),
    
    # document metadata
    (r'^(?P<document_id>[^/]+)/meta$', MethodDispatcher({'GET': document_meta})),

    # document metadata by external ID
    #(r'^/documents/external/(?P<external_id>[^/]+)/meta$', MethodDispatcher({'GET': document_meta})),
    (r'^external/(?P<pha_email>[^/]+)/(?P<external_id>[^/]+)/meta$', 
      MethodDispatcher({'GET': document_meta})),
    
    # document replace
    (r'^(?P<document_id>[^/]+)/replace$', MethodDispatcher({'POST' : document_version})),

    # document versions
    (r'^(?P<document_id>[^/]+)/versions/$', document_versions),

    # document label
    (r'^(?P<document_id>[^/]+)/label$', document_label),

    # Document Status
    (r'^(?P<document_id>[^/]+)/set-status$', MethodDispatcher({'POST' : document_set_status})),
    (r'^(?P<document_id>[^/]+)/status-history$', MethodDispatcher({'GET' : document_status_history})),

    # document label by external id
    #(r'^/documents/external/(?P<external_id>[^/]+)/label$', document_label),
    (r'^external/(?P<pha_email>[^/]+)/(?P<external_id>[^/]+)/label$', document_label),

    # document types
    (r'^types/(?P<type>[A-Za-z0-9._%-:#]+)/$', document_list),

    # document rels
    (r'^(?P<document_id_0>[^/]+)/rels/(?P<rel>[^/]+)/(?P<document_id_1>[^/]+)$', 
      MethodDispatcher({'PUT' : document_rels})),
    (r'^(?P<document_id>[^/]+)/rels/(?P<rel>[^/]+)/external/(?P<pha_email>[^/]+)/(?P<external_id>[^/]+)$', 
      MethodDispatcher({'PUT' : document_create_by_rel, 
                        'POST': document_create_by_rel})),    
    (r'^(?P<document_id_0>[^/]+)/rels/(?P<rel>[^/]+)/', 
      MethodDispatcher({'POST' : document_rels, 
                        'GET' : get_documents_by_rel}))
"""
