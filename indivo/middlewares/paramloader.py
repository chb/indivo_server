"""
Middleware (filters) for Indivo

Pre-processes paramaters that are passed to Indivo views,
replacing id strings with their corresponding Django models, 
including records, accounts, carenets, etc...

This is helpful to view functions, accesscontrol, and auditing.
"""

from django.http import Http404
from indivo import models

ID    = 'id'
EMAIL = 'email'
TOKEN = 'token'
SEPARATOR = '_'

# Contract: new param will be named the same as the
# old param, up to the first instance of SEPARATOR.

# CHANGE URLS so param name matches primary key in DB
LOAD_PARAMS = { 
  'account_email'   : ( models.Account,  EMAIL ),
  'account_id'      : ( models.Account,  EMAIL ),
  'carenet_id'      : ( models.Carenet,  ID    ),
  'pha_email'       : ( models.PHA,      EMAIL ),
  'record_id'       : ( models.Record,   ID    ),
  'reqtoken_id'     : ( models.ReqToken, TOKEN ),
}

class ParamLoader(object):

  def process_view(self, request, view_func, view_args, view_kwargs):
    """ substitute id-strings with models in view_kwargs:
    account_email becomes account, record_id becomes record, etc."""

    # Destructively modify view_kwargs for internal layers
    for param in LOAD_PARAMS.keys():
      if view_kwargs.has_key(param):
        model_obj = self.get_object_from_param(param, view_kwargs[param])
        
        #delete the old arg, and add the new one
        new_param = param[:param.find(SEPARATOR)]
        del view_kwargs[param]
        view_kwargs[new_param] = model_obj

    return None

  def get_object_from_param(self, param, param_val):
    return object_lookup_by_id(param_val, *LOAD_PARAMS[param])

def object_lookup_by_id(object_id, django_model, id_field):
  if object_id is None:
    return None
  query_kwargs = {id_field : object_id}
  try:
    return django_model.objects.get(**query_kwargs)
  except django_model.DoesNotExist:
    raise Http404
  


