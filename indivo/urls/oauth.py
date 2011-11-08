from django.conf.urls.defaults import *

#from oauth.djangoutils import request_token, exchange_token, PARAMS
#PARAMS['OAUTH_SERVER'] = OAUTH_SERVER

from indivo.views import *
from indivo.lib.utils import MethodDispatcher

urlpatterns = patterns('',
  url(r'^request_token$',    
      MethodDispatcher({'POST':request_token}),
      name='oauth_request_token'),

  url(r'^access_token$',
      MethodDispatcher({'POST':exchange_token}),     
      name='oauth_access_token'),

  url(r'^internal/request_tokens/(?P<reqtoken_id>[^/]+)/info$', 
      MethodDispatcher({'GET':request_token_info}), 
      name='oauth_internal_request_token_info'),

  # Request Token User Authorization is now handled by the UI, using internal
  # oauth calls (internal/request_tokens/approve), so oauth/authorize is no longer
  # part of the userapp-facing API.
                       
  ## INTERNAL oAuth operations that are not part of the standard public API
  # session
  url(r'^internal/session_create$', 
      MethodDispatcher({'POST':session_create}), 
      name='oauth_session_create'),

  url(r'^internal/request_tokens/(?P<reqtoken_id>[^/]+)/claim$', 
      MethodDispatcher({'POST':request_token_claim}), 
      name='oauth_internal_request_token_claim'),
    
  url(r'^internal/request_tokens/(?P<reqtoken_id>[^/]+)/approve$', 
      MethodDispatcher({'POST':request_token_approve}), 
      name='oauth_internal_request_token_approve'),
  
  ## signing URLS (SURL)
  url(r'^internal/surl-verify$', 
      MethodDispatcher({'GET':surl_verify})),
)

