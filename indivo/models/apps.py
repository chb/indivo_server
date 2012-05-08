"""
Indivo Models for Applications that extend Indivo
"""

from django.db import models
from django.conf import settings

from records_and_documents import Record, DocumentSchema
from base import Object, Principal, BaseModel, BaseMeta

import urllib, datetime
import indivo
from indivo.lib.utils import render_template_raw

try:
    from django.utils import simplejson
except ImportError:
    try:
        import simplejson
    except ImportError:
        raise ImportError("Couldn't find an installation of SimpleJSON")

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

  # short description of the app
  description = models.CharField(max_length=2000, null=True)

  # author of the app
  author = models.CharField(max_length=200, null=True)
  
  # version of the app
  version = models.CharField(max_length=40, null=True)

  # required Indivo version
  indivo_version = models.CharField(max_length=40, null=True)

  @classmethod
  def queryset_as_manifests(cls, queryset, as_string=False, **manifest_args):
      """ Return manifests for each app in the queryset, as a list or as a JSON string (if *as_string* is ``True``). """
      manifest_args.update(as_string=False)
      manifests = [obj.to_manifest(**manifest_args) for obj in queryset.iterator()]
      if as_string:
          return simplejson.dumps(manifests)
      return manifests
          

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

  # location of the app's icon
  icon_url = models.CharField(max_length=500, null=True)

  # other requirements: datatypes, REST methods, codes, etc.
  # represented as a JSON string suitable for dropping into
  # a SMART manifest
  requirements = models.TextField(null=True)

  @classmethod
  def from_manifest(cls, manifest, credentials, save=True):
    """ Produce a PHA object from an app manifest.

    Manifests should correspond to SMART manifest format 
    (http://wiki.chip.org/smart-project/index.php/Developers_Documentation:_Packaging_Applications_via_SMART_Manifest),
    with some optional Indivo specific extensions, namely:

    * *oauth_callback_url*: A callback URL for Indivo-style oAuth access
    * *autonomous_reason*: An explanation for why the app requires offline access to patient records
    * *has_ui*: ``true`` or ``false``, whether the app can be displayed in a browser.
    * *frameable*: ``true`` or ``false``, whether the app should be loaded in an iframe in the Indivo UI.
    * *indivo_version*: Required version of Indivo for compatibility
    
    Credentials should be JSON objects with two keys:

    * *consumer_key*: The oAuth consumer key to use for the app
    * *consumer_secret*: The oAuth consumer secret to use for the app

    See :doc:`app-registration` for more details.

    """

    from indivo.views import _get_indivo_version
    parsed_manifest = simplejson.loads(manifest)
    parsed_credentials = simplejson.loads(credentials)
    kwargs = {
      'consumer_key': parsed_credentials['consumer_key'],
      'secret': parsed_credentials['consumer_secret'],
      'name': parsed_manifest['name'],
      'email': parsed_manifest['id'],
      'start_url_template': parsed_manifest.get('index', ''),
      'callback_url': parsed_manifest.get('oauth_callback_url', ''),  # not used by SMART apps
      'is_autonomous': parsed_manifest.get('mode', '') == 'background',
      'autonomous_reason': parsed_manifest.get('autonomous_reason', ''),
      'has_ui': parsed_manifest['has_ui'] if parsed_manifest.has_key('has_ui') \
        else parsed_manifest.has_key('index'), # This may not be perfect
      'frameable': parsed_manifest['frameable'] if parsed_manifest.has_key('frameable') \
        else parsed_manifest.has_key('index'),
      'description': parsed_manifest.get('description', ''),
      'author': parsed_manifest.get('author', ''),
      'version': parsed_manifest.get('version', ''),
      'icon_url': parsed_manifest.get('icon', ''),
      'indivo_version':parsed_manifest['indivo_version'] if parsed_manifest.has_key('indivo_version') \
        else _get_indivo_version(parsed_manifest.get('smart_version', '')),
      'requirements': simplejson.dumps(parsed_manifest.get('requires', {})),
      }
    app = cls(**kwargs)
    if save:
      app.save()
    return app

  def to_manifest(self, smart_only=False, as_string=True):
      """ Produce a SMART-style manifest for the app.
      
      see :doc:`app-registration` for details on the manifest format.

      If *smart_only* is True, only SMART-manifest compatible fields will be included in the output.

      """
      from indivo.views import _get_smart_version
      smart_version = _get_smart_version(self.indivo_version)

      output = {
          "name": self.name,
          "description": self.description,
          "author": self.author,
          "id": self.email,
          "version": self.version,
          "smart_version": smart_version,
          "mode": "background" if self.is_autonomous else "ui",
          "scope": "record",
          "icon": self.icon_url,
          "index": self.start_url_template,          
          "requires": simplejson.loads(self.requirements),
          }
      if not smart_only:
          output.update({
                  "has_ui": self.has_ui,
                  "frameable": self.frameable,
                  "oauth_callback_url": self.callback_url,
                  "indivo_version": self.indivo_version,
                  })
          if self.is_autonomous:
              output['autonomous_reason'] = self.autonomous_reason
      if as_string:
          return simplejson.dumps(output)
      else:
          return output

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

  def scopedToRecord(self, record):
    """
    True if the PHA is enabled on the record
    """
    return self.pha_shares_to.filter(record=record).exists()

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

  @classmethod
  def from_manifest(cls, manifest, credentials, save=True):
    """ Produce a MachineApp object from an app manifest.

    Manifests should correspond to SMART manifest format 
    (http://wiki.chip.org/smart-project/index.php/Developers_Documentation:_Packaging_Applications_via_SMART_Manifest),
    with one required Indivo specific extensions, namely:
    
    * *ui_app*: ``true`` or ``false``. Whether the machineapp is a UIApp ('chrome app').
    * *indivo_version*: Required version of Indivo for compatibility
    
    Credentials should be JSON objects with two keys:

    * *consumer_key*: The oAuth consumer key to use for the app
    * *consumer_secret*: The oAuth consumer secret to use for the app

    See :doc:`app-registration` for more details.

    """

    from indivo.views import _get_indivo_version
    parsed_manifest = simplejson.loads(manifest)
    parsed_credentials = simplejson.loads(credentials)
    kwargs = {
      'consumer_key': parsed_credentials['consumer_key'],
      'secret': parsed_credentials['consumer_secret'],
      'name': parsed_manifest['name'],
      'email': parsed_manifest['id'],
      'app_type': 'chrome' if parsed_manifest['ui_app'] else 'admin',
      'description': parsed_manifest.get('description', ''),
      'author': parsed_manifest.get('author', ''),
      'version': parsed_manifest.get('version', ''),
      'indivo_version':parsed_manifest['indivo_version'] if parsed_manifest.has_key('indivo_version') \
        else _get_indivo_version(parsed_manifest.get('smart_version', '')),
      }
    app = cls(**kwargs)
    if save:
      app.save()
    return app

  def to_manifest(self, smart_only=False, as_string=True):
      """ Produce a SMART-style manifest for the app.
      
      see :doc:`app-registration` for details on the manifest format.
      
      If *smart_only* is True, only SMART-manifest compatible fields will be included in the output.

      """
      from indivo.views import _get_smart_version
      smart_version = _get_smart_version(self.indivo_version)
      output = {
          "name": self.name,
          "description": self.description,
          "author": self.author,
          "id": self.email,
          "version": self.version,
          "smart_version": smart_version,
          }
      if not smart_only:
          output.update({
                  "ui_app": self.app_type == 'chrome',
                  "indivo_version": self.indivo_version,
                  })
      if as_string:
          return simplejson.dumps(output)
      else:
          return output

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
