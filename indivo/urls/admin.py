from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',
    
    (r'^login/', MethodDispatcher({'GET': login, 'POST': login,}), {}, 'login-view'),
    (r'^$', MethodDispatcher({'GET': show_front_page})),
    (r'^logout/', MethodDispatcher({'GET': logout})),
    
    )
