"""
Indivo Models for Carenets
"""

import urllib, datetime

from django.db import models
from django.conf import settings

from base import Object, Principal, INDIVO_APP_LABEL

class Carenet(Object):
  name = models.CharField(max_length=40)
  record = models.ForeignKey('Record',          null=False)

  def __unicode__(self):
    return 'Carenet %s' % self.id

  class Meta:
    app_label = INDIVO_APP_LABEL
    unique_together = (("name","record"))

  # special documents
  
  def __get_special_doc(self, special_doc_name):
    """
    look at the special document and see if it's visible in this carenet
    """
    candidate_doc = getattr(self.record, special_doc_name)

    if not candidate_doc:
      return None

    # check that it's in this carenet
    if self.contains_doc(candidate_doc):
      return candidate_doc
    else:
      return None

  def add_doc(self, doc):
    """
    add the doc to the carenet
    """
    if doc.record != self.record:
      raise ValueError("document is not in the right record")

    return CarenetDocument.objects.get_or_create(carenet = self, document = doc)[0]

  def remove_doc(self, doc):
    CarenetDocument.objects.filter(carenet=self, document=doc).delete()
    
  def contains_doc(self, doc):
    return len(self.carenetdocument_set.filter(document = doc)) > 0

  @property
  def contact(self):
    return self.__get_special_doc('contact')

  @property
  def demographics(self):
    return self.__get_special_doc('demographics')


class CarenetDocument(Object):
  carenet   = models.ForeignKey('Carenet',      null=False)
  document  = models.ForeignKey('Document',     null=False)

  # a negative share, where share_p is false, is an exception to an autoshare rule
  share_p   = models.BooleanField(default=True, null=False)

  def __unicode__(self):
    return 'CarenetDocument %s' % self.id

  class Meta:
    app_label = INDIVO_APP_LABEL
    unique_together = (("carenet","document"))

class CarenetPHA(Object):
  carenet = models.ForeignKey('Carenet',        null=False)
  pha     = models.ForeignKey('PHA',            null=False)

  def __unicode__(self):
    return 'CarenetPHA %s' % self.id

  class Meta:
    app_label = INDIVO_APP_LABEL
    unique_together = (("carenet","pha"))

class CarenetAccount(Object):
  carenet = models.ForeignKey('Carenet',        null=False)
  account = models.ForeignKey('Account',        null=False)
  can_write = models.BooleanField(default=False)

  def __unicode__(self):
    return 'CarenetAccount %s' % self.id

  class Meta:
    app_label = INDIVO_APP_LABEL
    unique_together = (("carenet","account"))

class CarenetAutoshare(Object):
  carenet = models.ForeignKey('Carenet',        null=False)
  record  = models.ForeignKey('Record',         null=False)
  type    = models.ForeignKey('DocumentSchema', null=True)

  def __unicode__(self):
    return 'CarenetAutoshare %s' % self.id

  class Meta:
    app_label = INDIVO_APP_LABEL
    unique_together = (("carenet","record","type"))


# SZ: We are no longer using for people
# Ben Adida 2010-12-09: actually, for whole-record share, we are still using this for accounts.
class Share(Object):
  """
  Sharing a record with a principal
  """

  # the record that's being shared
  record = models.ForeignKey('Record', related_name = 'shares')
  
  # we could be smart here and have just a reference to a Principal
  # however, this would make querying for all PHAs and individuals difficult.
  # so there doesn't seem to be a need for this "smarts"
  with_account = models.ForeignKey('Account', related_name='shares_to', null=True)
  with_pha = models.ForeignKey('PHA', related_name='shares_to', null=True)

  # authorized
  authorized_at = models.DateTimeField(null=True, blank=True)

  # the user who added this share
  # there might not be one if this was primed, thus nullable
  authorized_by = models.ForeignKey('Account', null=True, related_name = 'shares_authorized_by')

  # limited to a particular carenet
  # this is when an app is *strictly* limited to a carenet,
  # not when an app is accessed by a user who happens to be in a carenet for that record.
  carenet = models.ForeignKey('Carenet', null=True)

  # a label for full-shares with *accounts*. This will probably go away in a future release,
  # but it's important to tag for now the role that various shares have.
  # this is called a "label" because it has no enforcement value
  role_label = models.CharField(max_length = 50, null=True)

  # does this share enable offline access?
  # this only makes sense for PHA shares
  # REMOVED 2010-07-27, since now the apps are the ones
  # that hold the autonomous information
  # offline = models.BooleanField(default = False)

  class Meta:
    app_label = INDIVO_APP_LABEL
    unique_together = (('record', 'with_account'),
                       ('record', 'with_pha'),)
    

  def new_access_token(self, token_str, token_secret, account=None, carenet=None):
    """
    create a new access token based on this share

    an account must be specified if the app is not autonomous.

    if the app is autonomous, the specified account should have full access
    over the record, or this will fail.

    if a carenet is specified, then this further limits the token to a specific carenet within the share
    we sanity check that the carenet matches the record of the share.

    an autonomous app should not be limited to a carenet, so specifying a carenet in that case should fail.
    """

    if carenet and carenet.record != self.record:
      raise Exception("bad carenet")


    access_token_params = {
      'token' : token_str,
      'token_secret' : token_secret,
      'share' : self,
      'carenet' : carenet
      }

    if self.with_pha.is_autonomous:
      if account:
        if not self.record.can_admin(account):
          raise Exception("an autonomous app can only be accessed by an account with full access to the record.")

        # we don't record the account for autonomous apps at this point
      if carenet:
        raise Exception("carenet should not be specified for autonomous apps")

      access_token_params['expires_at'] = None
    else:
      if account:
        # if no account with non-autonomous app, this
        # is certainly a case of app-priming. In this case,
        # we return a short-lived token with no account
        # specified, since we may not have an account to specify yet!
        access_token_params['account'] = account

      # FIXME: parameterize length of token validity
      access_token_params['expires_at'] = datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)

    return AccessToken.objects.create(**access_token_params)

class Token(object):
  """
  Some common features of access and request tokens
  """

  def __str__(self):
    vars = {'oauth_token' : self.token, 'oauth_token_secret' : self.token_secret}
    if self.share and not self.carenet:
      vars['xoauth_indivo_record_id'] = self.share.record.id
      ## DISABLED FOR NOW
      # vars['xoauth_indivo_carenet_id'] = self.share.record.carenet_alias_id
    if self.carenet:
      vars['xoauth_indivo_carenet_id'] = self.carenet.id
    return urllib.urlencode(vars)

  @property
  def secret(self):
    return self.token_secret

  to_string = __str__
  

class AccessToken(Principal, Token):
  # the token, secret, and PHA this corresponds to
  token = models.CharField(max_length=40)
  token_secret = models.CharField(max_length=60)

  # derived from a share
  share = models.ForeignKey('Share')

  # who is this token on behalf of? Might be nulls here.
  # when this is carenet-limited, the account scopes permissions
  # appropriately. 
  account = models.ForeignKey('Account', null = True)

  # this might seem redundant, given that we have share+account,
  # but it is
  # (a) cleaner to know immediately a carenet restriction, and
  # (b) conceivable that a user could be in two carenets for 
  #     the same record, and thus the rights of this access token
  #     would be ambiguous. Let's be extra explicit.
  # plus this makes permission checking a lot more natural
  carenet = models.ForeignKey('Carenet', null = True)

  # if null, it never expires, so BE CAREFUL
  expires_at = models.DateTimeField(null = True)

  # make sure email is set 
  def save(self, *args, **kwargs):
    self.email = "%s@accesstokens.indivo.org" % self.token
    super(AccessToken,self).save(*args, **kwargs)
  
  @property
  def effective_principal(self):
    # is it a session for the account?
    if self.account:
      return self.account
    else:
      return self.share.with_pha

  @property
  def proxied_by(self):
    if self.account:
      return self.share.with_pha
    else:
      return None

  # Accesscontrol:
  # roles that an accesstoken could have
  def isProxiedByApp(self, app):
    """
    Only true if the AccessToken is an account coming in via a PHA
    """
    return self.proxied_by == app

  def scopedToRecord(self, record):
    """
    True if the AccessToken is bound to the whole record, not a carenet
    """
    try:
      return self.share.record == record and not self.carenet
    except:
      return False

  def isInCarenet(self, carenet):
    """
    True if the AccessToken is bound to the carenet
    """
    try:
      return self.carenet == carenet
    except:
      return False

class ReqToken(Principal, Token):
  token = models.CharField(max_length=40)
  token_secret = models.CharField(max_length=60)
  verifier = models.CharField(max_length=60)
  oauth_callback = models.CharField(max_length=500, null=True)

  pha = models.ForeignKey('PHA')

  # record or carenet
  record = models.ForeignKey('Record', null=True)
  carenet = models.ForeignKey('Carenet', null=True)

  # when authorized
  authorized_at = models.DateTimeField(null=True)

  # authorized by can be used to bind the request token first, before the authorized_at is set.
  authorized_by = models.ForeignKey('Account', null = True)

  # the share that this results in
  share = models.ForeignKey('Share', null=True)

  # is this request token for offline access?
  # REMOVED 2010-07-27, since now the apps contain the indication of autonomy
  # NOT the tokens
  # offline_capable = models.BooleanField(default = False)

  # make sure email is set 
  def save(self, *args, **kwargs):
    self.email = "%s@requesttokens.indivo.org" % self.token
    super(ReqToken,self).save(*args, **kwargs)
  
  @property
  def effective_principal(self):
    """
    a request token's identity is really the PHA it comes from.
    """
    return self.pha
  
  # Accesscontrol:
  # Request tokens do not implement any roles, as they
  # are unrelated to the data

  @property
  def authorized(self):
    # only look for authorized_at, because sometimes 
    # it's primed, and not authorized by a particular user
    return self.authorized_at != None



