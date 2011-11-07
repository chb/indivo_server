"""
Indivo Models for Applications that extend Indivo
"""

from django.db import models
from django.conf import settings

from records_and_documents import Record, DocumentSchema
from base import Object, Principal, BaseModel, BaseMeta

import urllib, datetime
import indivo

##
## OAuth Stuff
##
class Nonce(BaseModel):
  """
  Nonces for oauth
  FIXME: clear out the old nonces regularly
  """
  nonce = models.CharField(max_length=100, null=False)
  oauth_type = models.CharField(max_length=50, null=True)
  created_at = models.DateTimeField(auto_now_add = True)

  Meta = BaseMeta()
  Meta.unique_together = ("nonce", "oauth_type")

##
## problem with hierarchy of abstracts
##
class OAuthApp(Principal):
  """
  An intermediate abstract class for all OAuth applications
  """

  Meta = BaseMeta(True)

  consumer_key = models.CharField(max_length=200)
  secret = models.CharField(max_length=60)
  name = models.CharField(max_length = 200)

## HACK because of problem
#OAuthApp = Principal

##
## PHAs
##

class PHA(OAuthApp):
  """
  User applications
  """

  Meta = BaseMeta()

  # URL templates look like http://host/url/{param1}?foo={param2}

  # start_url_template should contain a {record_id} parameter
  # start_url_template may contain a {document_id} parameter
  # start_url_template may contain a {next_url} parameter
  start_url_template = models.CharField(max_length=500)

  # callback_url
  callback_url = models.CharField(max_length=500)

  # does this app request a long-lived token?
  is_autonomous = models.BooleanField(default=False)
  autonomous_reason = models.TextField(null=True)

  # does the application have a user interface at all? (some are just background)
  # this really should only be falsifiable for autonomous apps.
  # non-autonomous apps must have a UI
  has_ui = models.BooleanField(default=True)

  # does the application fit in an iframe?
  # this should be true for now. Eventually
  # we'll have some apps that are not frameable
  frameable = models.BooleanField(default=True)

  # does the application have a document schema that it knows how to display well?
  schema = models.ForeignKey('DocumentSchema', null = True)

  # short description of the app
  description = models.CharField(max_length=2000, null=True)

  # privacy terms of use (XML)
  # FIXME: probably change this field type to XMLField()
  privacy_tou = models.TextField(null=True)

  # Accesscontrol:
  # roles that PHAs could implement.
  def isInCarenet(self, carenet):
    """
    True if the PHA is in the specified carenet
    """
    try:
      return indivo.models.CarenetPHA.objects.filter(carenet=carenet, pha=self)
    except:
      return False

##
## App Tokens are implemented separately, since they require access to record and docs
## (yes, this is confusing, but otherwise it's circular import hell)
##

##
## Applications which communicate directly with Indivo, not user-mediated
## There are two types:
## - admin: can use the admin API
## - chrome: can use any API and sudo as another user (though not as an admin app)
## 

# inherit first from Principal, second from OAuth Consumer
class MachineApp(OAuthApp):
  APP_TYPES = (
    ('admin', 'Admin'),
    ('chrome', 'Chrome')
    )

  # admin or chrome?
  # all chrome apps are also admin apps, but we use a type field
  # in case we add new types in the future
  app_type = models.CharField(max_length = 100, choices = APP_TYPES, null = False)

  # token and secret
  # an admin app is an oauth consumer with one token and one secret
  # which are repeated, as if it were an access token.
  #token = models.CharField(max_length=16)
  #secret = models.CharField(max_length=16)

  # Accesscontrol:
  # roles that a MachineApp could have
  def isType(self, type_str):
    """
    We override isType to handle admin vs. chrome apps.
    If type is 'MachineApp', always returns True. Otherwise,
    returns True if type_str is the app_type of the Machine App.
    """
    return super(MachineApp, self).isType(type_str) or \
        type_str == self.app_type

  def createdAccount(self, account):
    """
    The MachineApp created the account
    """
    try:
      return account.creator == self
    except:
      return False

  def createdRecord(self, record):
    """
    The MachineApps can created the record
    """
    try:
      return record.creator == self
    except:
      return False

##
## session tokens
##

class SessionRequestToken(Object):
  token = models.CharField(max_length=40)
  secret = models.CharField(max_length=60)

  user = models.ForeignKey('Account', null = True)
  approved_p = models.BooleanField(default=False)

class SessionToken(Object):
  token = models.CharField(max_length=40)
  secret = models.CharField(max_length=60)

  user = models.ForeignKey('Account', null = True)

  expires_at = models.DateTimeField(null = False)

  @property
  def approved_p(self):
    return True
  
  def save(self, *args, **kwargs):
    if self.expires_at == None:
      self.expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)
    super(SessionToken, self).save(*args, **kwargs)

  def __str__(self):
    vars = {'oauth_token' : self.token, 'oauth_token_secret' : self.secret, 'account_id': self.user.email}
    return urllib.urlencode(vars)
