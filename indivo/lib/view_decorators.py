"""
Decorators for views
"""

from django.http import HttpResponse, HttpResponseRedirect, Http404
from indivo import models
from indivo import check_safety
from indivo.middlewares.paramloader import object_lookup_by_id

from django.db.transaction import commit_on_success, rollback
from functools import wraps

import inspect
import functools, copy, logging

def marsloader(func):
  def marsloader_func(request, *args, **kwargs):
    """MARS_loader (Modifying Arguments for the Result Set) 
      
      adds arguments specifically meant to modify the result set 
      (eg. limit, offset and order_by)
    """

    check_safety()

    STATUS = 'status'

    # This should be abstracted
    # StatusName 'active' should always be available
    arg_list = [  ('limit', 100), 
                  ('offset', 0),
                  ('order_by', '-created_at'),
                  (STATUS, models.StatusName.objects.get(name='active'))]

    new_args = copy.copy(kwargs)
    rsm_arg_list = {}
    for arg in arg_list:
      rsm_arg_list[arg[0]] = arg[1]

    # All paths that end in a slash and have an HTTP method of GET will return a result set
    rsm_cand = request.method == 'GET' and request.META['PATH_INFO'][-1] == '/'
    if rsm_cand:
      for rsm_arg, qdefault in rsm_arg_list.items():
        if request.GET.has_key(rsm_arg):
          if rsm_arg == STATUS:
            try:
              new_args[rsm_arg] = models.StatusName.objects.get(name=request.GET[rsm_arg])
            except models.StatusName.DoesNotExist:
              raise Http404
              new_args[rsm_arg] = qdefault
          else:
            try:
              new_args[rsm_arg] = int(request.GET[rsm_arg])
            except:
              new_args[rsm_arg] = request.GET[rsm_arg]
        else:
          new_args[rsm_arg] = qdefault

    # Check that the new arguments are all in func()
    if len(inspect.getargspec(func)) > 0:
      for new_arg in new_args.keys():
        if new_arg not in inspect.getargspec(func)[0]:
          raise Exception("Missing arg " + new_arg + " in " + func.func_name)
    return func(request, **new_args)
  return functools.update_wrapper(marsloader_func, func)


##
## transaction management
##

def commit_on_200(func):
  """
  Commit changes to the database only if the response is a 200.
  Anything else causes a rollback.
  This is a more stringent version of commit_on_success, which
  only rolls back in the case of an exception.

  The idea here is that first we call the func, and if it returns a bad result
  we do a rollback. The exception catching, we leave to the commit_on_success wrapper,
  which we wrap around ourselves
  """

  @wraps(func)
  def _inner_commit(*args, **kwargs):
    result = func(*args, **kwargs)
    if not hasattr(result, 'status_code') or result.status_code != 200:
      rollback()

    return result

  # layer the commit_on_successoutside of our first check for 200
  # note that, if the wrapped func raises an exception, it goes 
  # right through our decorator here (like butter), and hits the commit_on_success
  # handler which will roll back the transaction then. We keep it simple.
  return commit_on_success(_inner_commit)
      
      
