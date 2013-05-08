from django.conf.urls import patterns

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',
    (r'^$', MethodDispatcher({
                  'GET' : carenet_list,
                  # SZ: Should be PUT but using POST for compatibility
                  'POST' : carenet_create
                }))
)
