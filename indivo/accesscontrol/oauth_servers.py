"""
OAuth servers for users and admins
"""

import oauth.oauth as oauth

from django.db import transaction

from indivo import models

import datetime, logging


class UserDataStore(oauth.OAuthStore):
  """
  Layer between Python OAuth and Django database
  for user applications (PHAs)
  """

  def __get_pha(self, consumer_key):
    try:
      return models.PHA.objects.get(consumer_key = consumer_key)
    except models.PHA.DoesNotExist:
      return None

  def __get_token(self, token_str, pha=None):
    kwargs = {'token': token_str}
    if pha: kwargs['share__with_pha'] = pha

    try:
      return models.AccessToken.objects.get(**kwargs)
    except models.AccessToken.DoesNotExist:
      return None
    
  def verify_request_token_verifier(self, request_token, verifier):
    """
    Verify whether a request token's verifier matches
    The verifier is stored right in the request token itself
    """
    return request_token.verifier == verifier

  def lookup_consumer(self, consumer_key):
    """
    looks up a consumer
    """
    return self.__get_pha(consumer_key)

  def create_request_token(self,  consumer, 
                           request_token_str, 
                           request_token_secret, 
                           verifier, 
                           oauth_callback, 
                           record_id=None,
                           carenet_id=None):
    """
    take a RequestToken and store it.

    anything after request_token_secret is extra kwargs custom to this server.
    """
    
    # look for the record that this might be mapped to
    # IMPORTANT: if the user who authorizes this token is not authorized to admin the record, it will be a no-go
    record = None
    if record_id:
      try:
        record = models.Record.objects.get(id = record_id)
      except models.Record.DoesNotExist:
        pass

    carenet = None
    if carenet_id:
      try:
        carenet = models.Carenet.objects.get(id = carenet_id)
      except models.Carenet.DoesNotExist:
        pass
      
    # (BA) added record to the req token now that it can store it
    # (BA 2010-05-06) added offline_capable
    return models.ReqToken.objects.create(pha             = consumer, 
                                          token           = request_token_str, 
                                          token_secret    = request_token_secret, 
                                          verifier        = verifier, 
                                          oauth_callback  = oauth_callback, 
                                          record          = record,
                                          carenet         = carenet)

  def lookup_request_token(self, consumer, request_token_str):
    """
    token is the token string
    returns a OAuthRequestToken

    consumer may be null.
    """
    try:
      # (BA) fix for consumer being null when we don't know yet who the consumer is
      if consumer:
        return models.ReqToken.objects.get(token = request_token_str, pha = consumer)
      else:
        return models.ReqToken.objects.get(token = request_token_str)
    except models.ReqToken.DoesNotExist:
      return None

  def authorize_request_token(self, request_token, record=None, carenet=None, account=None):
    """
    Mark a request token as authorized by the given user,
    with the given additional parameters.

    This means the sharing has beeen authorized, so the Share should be added now.
    This way, if the access token process fails, a re-auth will go through automatically.

    The account is whatever data structure was received by the OAuthServer.
    """

    if (record or carenet) == None:
      raise Exception("at least record or carenet must be set")

    request_token.authorized_at = datetime.datetime.utcnow()
    request_token.authorized_by = account

    # store the share in the request token
    # added use of defaults to reduce code size if creating an object
    if record:
      share, create_p = models.PHAShare.objects.get_or_create( record        = record, 
                                                               with_pha      = request_token.pha, 
                                                               defaults = {'authorized_at': request_token.authorized_at, 
                                                                           'authorized_by': request_token.authorized_by})
    else:
      # this is a carenet only situation, we NEVER create the share
      share = models.PHAShare.objects.get(record = carenet.record, with_pha = request_token.pha)
      
    request_token.share = share
    request_token.save()
    

  def mark_request_token_used(self, consumer, request_token):
    """
    Mark that this request token has been used.
    Should fail if it is already used
    """
    new_rt = models.ReqToken.objects.get(pha = consumer, token = request_token.token)

    # authorized?
    if not new_rt.authorized:
      raise oauth.OAuthError("Request Token not Authorized")

    new_rt.delete()

  def create_access_token(self, consumer, request_token, access_token_str, access_token_secret):
    """
    Store the newly created access token that is the exchanged version of this
    request token.
    
    IMPORTANT: does not need to check that the request token is still valid, 
    as the library will ensure that this method is never called twice on the same request token,
    as long as mark_request_token_used appropriately throws an error the second time it's called.
    """

    share = request_token.share

    # FIXME: for autonomous apps, it would be good if we didn't keep handing out
    # long-lived tokens here.

    # create an access token for this share
    return share.new_access_token(access_token_str, 
                                  access_token_secret, 
                                  account=request_token.authorized_by,
                                  carenet=request_token.carenet)

  def lookup_access_token(self, consumer, access_token_str):
    """
    token is the token string
    returns a OAuthAccessToken
    """
    return self.__get_token(token_str = access_token_str, pha = consumer)

  def check_and_store_nonce(self, nonce_str):
    """
    store the given nonce in some form to check for later duplicates
    
    IMPORTANT: raises an exception if the nonce has already been stored
    """
    nonce, created = models.Nonce.objects.get_or_create(nonce = nonce_str, 
                                                        oauth_type = self.__class__.__name__)
    if not created:
      raise oauth.OAuthError("Nonce already exists")


class MachineDataStore(oauth.OAuthStore):
  """
  Layer between Python OAuth and Django database.
  """

  def __init__(self, type = None):
    self.type = type

  def __get_machine_app(self, consumer_key):
    try:
      if self.type:
        return models.MachineApp.objects.get(app_type = self.type, consumer_key = consumer_key)
      else:
        # no type, we look at all machine apps
        return models.MachineApp.objects.get(consumer_key = consumer_key)
    except models.MachineApp.DoesNotExist:
      return None

  def lookup_consumer(self, consumer_key):
    """
    looks up a consumer
    """
    return self.__get_machine_app(consumer_key)

  def lookup_request_token(self, consumer, request_token_str):
    """
    token is the token string
    returns a OAuthRequestToken

    consumer may be null.
    """
    return None

  def lookup_access_token(self, consumer, access_token_str):
    """
    token is the token string
    no access tokens for machine apps
    """
    return None

  def check_and_store_nonce(self, nonce_str):
    """
    store the given nonce in some form to check for later duplicates
    
    IMPORTANT: raises an exception if the nonce has already been stored
    """
    nonce, created = models.Nonce.objects.get_or_create(nonce = nonce_str,
                                                        oauth_type = self.__class__.__name__)
    if not created:
      raise oauth.OAuthError("Nonce already exists")


class SessionDataStore(oauth.OAuthStore):
  """
  Layer between Python OAuth and Django database.

  An oauth-server for in-RAM chrome-app user-specific tokens
  """

  def __get_chrome_app(self, consumer_key):
    try:
      return models.MachineApp.objects.get(consumer_key = consumer_key, app_type='chrome')
    except models.MachineApp.DoesNotExist:
      return None

  def __get_request_token(self, token_str, type=None, pha=None):
    try:
      return models.SessionRequestToken.objects.get(token = token_str)
    except models.SessionRequestToken.DoesNotExist:
      return None

  def __get_token(self, token_str, type=None, pha=None):
    try:
      return models.SessionToken.objects.get(token = token_str)
    except models.SessionToken.DoesNotExist:
      return None

  def lookup_consumer(self, consumer_key):
    """
    looks up a consumer
    """
    return self.__get_chrome_app(consumer_key)

  def create_request_token(self, consumer, request_token_str, request_token_secret, verifier, oauth_callback):
    """
    take a RequestToken and store it.

    the only parameter is the user that this token is mapped to.
    """
    
    # we reuse sessiontoken for request and access
    token = models.SessionRequestToken.objects.create(token = request_token_str, secret = request_token_secret)
    return token

  def lookup_request_token(self, consumer, request_token_str):
    """
    token is the token string
    returns a OAuthRequestToken

    consumer may be null.
    """
    return self.__get_request_token(token_str = request_token_str)

  def authorize_request_token(self, request_token, user=None):
    """
    Mark a request token as authorized by the given user,
    with the given additional parameters.

    The user is whatever data structure was received by the OAuthServer.
    """
    request_token.user = user
    request_token.authorized_p = True
    request_token.save()

  def mark_request_token_used(self, consumer, request_token):
    """
    Mark that this request token has been used.
    Should fail if it is already used
    """
    if not request_token.authorized_p:
      raise oauth.OAuthError("request token not authorized")

    request_token.delete()

  def create_access_token(self, consumer, request_token, access_token_str, access_token_secret):
    """
    Store the newly created access token that is the exchanged version of this
    request token.
    
    IMPORTANT: does not need to check that the request token is still valid, 
    as the library will ensure that this method is never called twice on the same request token,
    as long as mark_request_token_used appropriately throws an error the second time it's called.
    """

    token = models.SessionToken.objects.create( token   = access_token_str, 
                                                secret  = access_token_secret, 
                                                user    = request_token.user)
    return token

  def lookup_access_token(self, consumer, access_token_str):
    """
    token is the token string
    returns a OAuthAccessToken
    """
    return self.__get_token(access_token_str)

  def check_and_store_nonce(self, nonce_str):
    """
    store the given nonce in some form to check for later duplicates
    
    IMPORTANT: raises an exception if the nonce has already been stored
    """
    nonce, created = models.Nonce.objects.get_or_create(nonce = nonce_str,
                                                        oauth_type = self.__class__.__name__)
    if not created:
      raise oauth.OAuthError("Nonce already exists")


ADMIN_OAUTH_SERVER = oauth.OAuthServer(store = MachineDataStore())
SESSION_OAUTH_SERVER = oauth.OAuthServer(store = SessionDataStore())

OAUTH_SERVER = oauth.OAuthServer(store = UserDataStore())
