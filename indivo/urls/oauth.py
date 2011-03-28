from django.conf.urls.defaults import *

#from oauth.djangoutils import request_token, exchange_token, PARAMS
#PARAMS['OAUTH_SERVER'] = OAUTH_SERVER

from indivo.views import user_authorization, request_token, exchange_token, session_create, request_token_claim, request_token_info, request_token_approve, get_long_lived_token, surl_verify

urlpatterns = patterns('',
  url(r'^request_token$',    request_token,      name='oauth_request_token'),
  url(r'^authorize$',        user_authorization, name='oauth_user_authorization'),
  url(r'^access_token$',     exchange_token,     name='oauth_access_token'),
                       
  ## INTERNAL oAuth operations that are not part of the standard public API
  # session
  url(r'^internal/session_create$', session_create, name='oauth_session_create'),

  url(r'^internal/request_tokens/(?P<reqtoken_id>[^/]+)/claim$', 
          request_token_claim, name='oauth_internal_request_token_claim'),
  url(r'^internal/request_tokens/(?P<reqtoken_id>[^/]+)/info$', 
          request_token_info, name='oauth_internal_request_token_info'),
  url(r'^internal/request_tokens/(?P<reqtoken_id>[^/]+)/approve$', 
          request_token_approve, name='oauth_internal_request_token_approve'),
  url(r'^internal/long-lived-token$', 
          get_long_lived_token, name='oauth_internal_get_long_lived_token'),
           
  ## signing URLS (SURL)
  url(r'^internal/surl-verify$', surl_verify),
)

