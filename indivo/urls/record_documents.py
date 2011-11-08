from django.conf.urls.defaults import *

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',

    #sharing
    (r'^(?P<document_id>[^/]+)/nevershare', MethodDispatcher({
                'PUT' : document_set_nevershare,
                'DELETE': document_remove_nevershare})),
    (r'^(?P<document_id>[^/]+)/carenets/$', MethodDispatcher({
                'GET' : document_carenets
                })), 
    (r'^(?P<document_id>[^/]+)/carenets/(?P<carenet_id>[^/]+)$', MethodDispatcher({
                'PUT' : carenet_document_placement, 
                'DELETE' : carenet_document_delete
                })), 
    (r'^(?P<document_id>[^/]+)/carenets/(?P<carenet_id>[^/]+)/autoshare-revert$', MethodDispatcher({
                'POST' : autoshare_revert
                })), 

    (r'^$', MethodDispatcher({
                'GET'     : record_document_list,
                'POST'    : document_create,
                'DELETE'  : documents_delete})),

    # create by document external ID
    (r'^external/(?P<pha_email>[^/]+)/(?P<external_id>[^/]+)$', 
      MethodDispatcher({'PUT' : document_create_by_ext_id})),
    (r'^external/(?P<pha_email>[^/]+)/(?P<external_id>[^/]+)/meta$', 
      MethodDispatcher({'GET': record_document_meta_ext})),

    # single document
    (r'^(?P<document_id>[^/]+)$', MethodDispatcher({
                'GET': record_specific_document})),
    
    # document metadata
    (r'^(?P<document_id>[^/]+)/meta$', MethodDispatcher({ 'GET': record_document_meta,
                                                          'PUT' : update_document_meta })),

    # document replace
    (r'^(?P<document_id>[^/]+)/replace$', MethodDispatcher({'POST' : document_version})),
    (r'^(?P<document_id>[^/]+)/replace/external/(?P<pha_email>[^/]+)/(?P<external_id>[^/]+)$', MethodDispatcher({'PUT' : document_version_by_ext_id})),

    # document versions
    (r'^(?P<document_id>[^/]+)/versions/$', 
     MethodDispatcher({'GET':document_versions})),

    # document label
    (r'^(?P<document_id>[^/]+)/label$', 
     MethodDispatcher({'PUT':record_document_label})),

    # Document Status
    (r'^(?P<document_id>[^/]+)/set-status$', MethodDispatcher({'POST' : document_set_status})),
    (r'^(?P<document_id>[^/]+)/status-history$', MethodDispatcher({'GET' : document_status_history})),

    # document label by external id
    #(r'^/documents/external/(?P<external_id>[^/]+)/label$', document_label),
    (r'^external/(?P<pha_email>[^/]+)/(?P<external_id>[^/]+)/label$', 
     MethodDispatcher({'PUT':record_document_label_ext})),

    # document types
    # disabled 2010-08-15 we will only use the query parameter for this
    # (r'^types/(?P<type>[A-Za-z0-9._%-:#]+)/$', document_list),

    # document rels
    (r'^(?P<document_id_0>[^/]+)/rels/(?P<rel>[^/]+)/(?P<document_id_1>[^/]+)$', 
      MethodDispatcher({'PUT' : document_rels})),
    (r'^(?P<document_id>[^/]+)/rels/(?P<rel>[^/]+)/$', 
      MethodDispatcher({'POST': document_create_by_rel, 
                        'GET' : get_documents_by_rel})),
    (r'^(?P<document_id>[^/]+)/rels/(?P<rel>[^/]+)/external/(?P<pha_email>[^/]+)/(?P<external_id>[^/]+)$', 
      MethodDispatcher({'PUT' : document_create_by_rel_with_ext_id, 
                        'POST': document_create_by_rel_with_ext_id})),    

    # special documents
    (r'^special/(?P<special_document>[^/]+)$', MethodDispatcher(
            {'GET' : read_special_document,
             'PUT' : save_special_document,
             'POST': save_special_document}))

)
