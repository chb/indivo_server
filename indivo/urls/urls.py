from django.conf.urls.defaults import *

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',
    
    # OAuth
    (r'^oauth/', include('indivo.urls.oauth')),
    (r'^version$', get_version),

    # account-specific URLs
    (r'^accounts/$', account_create),
    (r'^accounts/search$', account_search),
    (r'^accounts/forgot-password$', account_forgot_password),
    (r'^accounts/(?P<account_email>[^/]+)$', account_info),
    (r'^accounts/(?P<account_email>[^/]+)/', include('indivo.urls.account')),

    (r'^carenets/(?P<carenet_id>[^/]+)', include('indivo.urls.carenet')),

    # create a new record
    (r'^records/$', MethodDispatcher({'POST': record_create})),
   
    # SZ: FIX ME! 
    # create a new record by external ID
    (r'^records/external/(?P<principal_email>[^/]+)/(?P<external_id>[^/]+)$', MethodDispatcher({
                'PUT'  : record_create_ext})),

    # Records
    (r'^records/(?P<record_id>[^/]+)', include('indivo.urls.record')),
    
    # Current identity
    (r'^id$', get_id),

    # PHAs
    # NOTE: the double-underscore extra parameter __app_specific triggers access-control mechanisms
    (r'^apps/$', all_phas),
    (r'^apps/(?P<pha_email>[^/]+)$', MethodDispatcher({'GET' : pha, 'DELETE': pha_delete})),
    (r'^apps/(?P<pha_email>[^/]+)', include('indivo.urls.application')),
    
    # static
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    
    )
