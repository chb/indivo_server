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

    (r'^/shares/(?P<other_account_id>[^/]+)/delete$', record_share_delete),

    # reset password
    (r'^/password_reset$', record_password_reset),

    # notify record
    (r'^/notify$', record_notify),

    # message record
    (r'^/inbox/$', MethodDispatcher({
                'GET': record_inbox})),
    (r'^/inbox/(?P<message_id>[^/]+)$', MethodDispatcher({
                'POST': record_send_message})),
    (r'^/inbox/(?P<message_id>[^/]+)/attachments/(?P<attachment_num>[^/]+)$', MethodDispatcher({
                'POST' : record_message_attach}))
)
