"""
Indivo Models
"""

from django.db import models
from django.conf import settings

import hashlib
import uuid
import copy
import string
import logging

from datetime import datetime, timedelta
from oauth import oauth

from indivo.fields import DummyField

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

  def _get_subclasses(self):
    """ Returns a dict of 'type_name':class key-value pairs for each subclass of Principal."""
    return dict([(rel.var_name, rel.field.model) 
                 for rel in self._meta.get_all_related_objects() 
                 if isinstance(rel.field, models.OneToOneField) 
                 and issubclass(rel.field.model, self.__class__)])

  def get_subclass(self):
    """ Return the instance of a subclass of this object of type ``self.type``. 
    
    Returns ``self`` if no such instance exists (i.e., we have no subclasses).

    Normally, this is available through ``getattr(self, self.type.lower())``,
    but sometimes that just gets us another principal object. We'll try the
    above approach first, since it allows us to use select_related to be
    more efficient, but if that fails, we'll have to use a call to
    ``objects.get()``, which will always go to the DB. Because of this behavior,
    this call should be used sparingly.
    
    """

    # If we are already an instance of our lowest subclass, avoid extra computation
    if self.__class__.__name__ == self.type:
      return self

    # First try to get at the child through Django's OneToOne attribute
    # i.e. Principal.account or Principal.pha
    try:
      subclass_obj = getattr(self, self.type.lower().strip())
      if subclass_obj.__class__.__name__ == self.type:
        return subclass_obj
    except:
      
      # This shouldn't happen, if Django is working properly and self.type is set correctly
      pass

    # Had trouble with the standard lookup, so select_related won't work.
    # Just use subclass.objects.get(), which will go straight to the DB
    try:
      model_class = self._get_subclasses()[self.type.lower().strip()]
    except KeyError:

      # we're already an instance of the lowest subclass
      return self

    try:
      return model_class.objects.get(id=self.id)
    except model_class.DoesNotExist:

      # Shouldn't happen: our subclass didn't exist
      return self

  def descriptor(self):

    """ Get a name for the Principal instance.

    Returns the email id if we don't have a name (i.e. accesstokens)

    """

    subclass_obj = self.get_subclass()    
    return getattr(subclass_obj, 'full_name', None) or getattr(subclass_obj, 'name', None) or subclass_obj.email
    
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

class DataModelBase(models.base.ModelBase):
    """ Subclass of the Django Model metaclass that handles Dummy Fields on Indivo Data Models. 
    
    Also setting all fields to blank=True, so it won't interfere with our datamodel validation.
    This is fine because we aren't using the Django admin.

    """

    def __new__(cls, name, bases, attrs):

        def replace_field(fields_dict, field_name, field):
            new_fields_dict = copy.copy(fields_dict)
            
            # build the new fields to replace the old field with
            for suffix, new_field_params in field.__class__.replacements.iteritems():
                new_name = "%s_%s"%(field_name, suffix)
                new_field_class, new_field_kwargs = new_field_params
                new_field = new_field_class(**new_field_kwargs)
                # use db_column name if specified, otherwise default to suffix
                new_field.db_column = "%s_%s" % ((field.db_column or field_name), (new_field.db_column or suffix))
                new_field.blank = True
                new_fields_dict[new_name] = new_field

                # recurse if the new field is actually a replaceable DummyField
                if issubclass(new_field_class, DummyField):
                    new_fields_dict = replace_field(new_fields_dict, new_name, new_field)

            del new_fields_dict[field_name]
            return new_fields_dict

        # Iterate over the fields in the model, and replace all of the dummy fields
        new_attrs = copy.copy(attrs)
        for field_name, field_val in attrs.iteritems():
            if isinstance(field_val, DummyField):
                new_attrs = replace_field(new_attrs, field_name, field_val)
            elif isinstance(field_val, models.Field):
                field_val.blank = True
        return super(DataModelBase, cls).__new__(cls, name, bases, new_attrs)
