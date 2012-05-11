from django.conf.urls.defaults import *

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',

    (r'^$', record),

    (r'^/apps/',      include('indivo.urls.record_apps')),
    (r'^/audits/',    include('indivo.urls.record_audits')),
    (r'^/autoshare/', include('indivo.urls.record_autoshare')),
    (r'^/carenets/',  include('indivo.urls.record_carenets')),
    (r'^/documents/', include('indivo.urls.record_documents')),
    (r'^/reports/',   include('indivo.urls.record_reports')),

    # ownership
    (r'^/owner$', MethodDispatcher({
                'GET' : record_get_owner,
                'PUT' : record_set_owner,
                # for now, POST compatibility (Ben)
                'POST' : record_set_owner
                })),
    # shares
    (r'^/shares/$', MethodDispatcher({
        'GET'  : record_shares,
        'POST' : record_share_add})),

    # Deprecated as of 1.0: This isn't RESTful at all
    # Use the below call instead.                       
    (r'^/shares/(?P<other_account_id>[^/]+)/delete$', 
     MethodDispatcher({'POST':record_share_delete})),

    (r'^/shares/(?P<other_account_id>[^/]+)$', 
     MethodDispatcher({'DELETE':record_share_delete})),

    # Deprecated as of 1.0: This isn't RESTful.
    # Use the below call instead.
    (r'^/notify$', MethodDispatcher({'POST':record_notify})),
    (r'^/notifications/$', MethodDispatcher({'POST':record_notify})),

    # message record
    (r'^/inbox/(?P<message_id>[^/]+)$', MethodDispatcher({
                'POST': record_send_message})),
    (r'^/inbox/(?P<message_id>[^/]+)/attachments/(?P<attachment_num>[^/]+)$', MethodDispatcher({
                'POST' : record_message_attach})),

    # SMART API Aliases
    (r'^/allergies/$', MethodDispatcher({'GET': smart_allergies})), # requires a custom view due to AllergyExclusions
    (r'^/(?P<model_name>[^/]+)/$', MethodDispatcher({'GET': smart_generic})),

)
