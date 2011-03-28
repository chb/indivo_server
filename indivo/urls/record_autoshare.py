from django.conf.urls.defaults import *

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',
  (r'^bytype/$', MethodDispatcher({ 'GET'  : autoshare_list })),
  (r'^bytype/all$', MethodDispatcher({ 'GET'  : autoshare_list_bytype_all })),
  (r'^carenets/(?P<carenet_id>[^/]+)/bytype/set$', MethodDispatcher({ 'POST' : autoshare_create })),
  (r'^carenets/(?P<carenet_id>[^/]+)/bytype/unset$', MethodDispatcher({ 'POST' : autoshare_delete }))
)
