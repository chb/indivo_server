"""
Access Rule class for controlling access to views
"""
from indivo.views import *  
from indivo.models.base import BaseModel

_REGISTRY = {}

class AccessRule(object):

  @classmethod
  def register(cls, access_rule_obj):
    """
    Register a new access rule in the registry--stores a mapping
    from each view to the access function to be evaluated
    """
    for view_func in access_rule_obj.views:
      if _REGISTRY.has_key(view_func):
        raise ValueError("Can't assign the same view to multiple access rules: \
view %s assigned to access group %s AND %s"%(view_func.__name__, _REGISTRY[view_func].name, access_rule_obj.name))
      _REGISTRY[view_func] = access_rule_obj

  @classmethod
  def lookup(cls, view_func):
    """
    Lookup a view function in the registry. Gets an access function
    """
    if _REGISTRY.has_key(view_func):
      return _REGISTRY[view_func]
    return None

  def __init__(self, name, access_func, view_list):
    self.name = name
    self.rule = access_func
    self.views = view_list
    AccessRule.register(self)

  def __str__(self):
    return self.name

  #what args does this function need? With middleware or a decorator above, hopefully just principal and **kwargs
  def check(self, principal, **kwargs):
    return self.rule(principal, **kwargs)
