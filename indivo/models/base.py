"""
Indivo Models
"""

from django.db import models
from django.conf import settings

import hashlib
import uuid

import string
import logging

from datetime import datetime, timedelta
from oauth import oauth

# generate the right meta class
INDIVO_APP_LABEL = 'indivo'

def BaseMeta(abstract_p=False):
  class Meta:
    app_label = INDIVO_APP_LABEL
    abstract = abstract_p
  return Meta

class BaseModel(models.Model):
  """
  The base for all indivo models
  """
  Meta = BaseMeta(True)

  @classmethod
  def setup(cls):
    """
    called automatically after this class has been prepared into the server
    """
    pass

# SZ: Why is this called Object?
class Object(BaseModel):

  id = models.CharField(max_length = 50, primary_key = True)
  created_at = models.DateTimeField(auto_now_add = True)
  modified_at = models.DateTimeField(auto_now_add = True, auto_now = True)
  creator = models.ForeignKey('Principal', related_name = '%(class)s_created_by', null = True)

  def __unicode__(self):
    return "Core Object %s" % self.id

  Meta = BaseMeta(True)

  def save(self, **kwargs):
    if not self.id:
      self.id = str(uuid.uuid4())
    super(Object, self).save(**kwargs)


class Principal(Object):
  Meta = BaseMeta()

  # every principal is associated with an email address
  email = models.CharField(max_length = 255, unique = True)

  # effectively the descendent table
  type = models.CharField(max_length = 100)

  def save(self, *args, **kwargs):
    """
    make sure some fields are set
    """
    if not self.type or self.type == '':
      self.type = self.__class__.__name__
    super(Principal,self).save(*args, **kwargs)
    
  def name(self):
    """
    FIXME: this should be better optimized
    """
    if self.type == 'Account':
      return self.account.full_name

    if self.type == 'PHA':
      return self.pha.name

    return ''
    
  # Accesscontrol:
  # Default Role Implmentations (deny-by-default):
  def isType(self, type_str):
    """
    The principal is of the specified type.
    """
    return self.type == type_str # What are the options for self.type? Where does it get set?

  def isSame(self, arg):
    """
    The principal is the same object as arg. Semantics: if the
    effective principal is the same object as arg, also return true.
    """
    # Note: the django Model overloaded __eq__ operator makes this equivalent
    # to comparing the ids of the models.
    return self == arg or self.effective_principal == arg

  def isProxiedByApp(self, app):
    """
    The principal is proxied by an app, i.e., an accesstoken may be proxied by a PHA
    """
    return False

  def createdAccount(self, account):
    """
    The principal created the account
    """
    return False

  def createdRecord(self, record):
    """
    The principal created the specified record
    """
    return False

  def ownsRecord(self, record):
    """
    The principal is the owner of the specified record
    """
    return False

  def scopedToRecord(self, record):
    """
    The principal is bound to the record at a whole-record level. (i.e., not limited to a carenet)
    """
    return False

  def fullySharesRecord(self, record):
    """
    The record is fully shared with the principal
    """
    return False

  def isInCarenet(self, carenet):
    """
    The principal is located within the scope of the carenet
    """
    return False

  def basicPrincipalRole(self):
    """
    The Principal is a principal. Always returns true, and
    shouldn't be overwritten by subclasses
    """
    return True


  @property
  def effective_principal(self):
    """
    In some cases, a principal's effective principal is not quite itself,
    e.g. a token's identity is really the PHA it comes from.
    """
    return self

  @property
  def proxied_by(self):
    """
    Principals are sometimes proxied by other principals, e.g. a PHA
    By default, principals are not proxied.
    """
    return None

  @property
  def effective_email(self):
    return self.effective_principal

  def __unicode__(self):
    return 'Principal %s' % self.email

  def __eq__(self, other):
    if not other or not isinstance(other, Principal):
      return False

    return self.id == other.id

