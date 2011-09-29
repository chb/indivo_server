"""
Decorators for views
"""

from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from indivo import models
from indivo import check_safety
from indivo.middlewares.paramloader import object_lookup_by_id
from indivo.lib import iso8601

from django.db.transaction import commit_on_success, rollback
from functools import wraps

import inspect
import functools, copy, logging

DEFAULT_ORDERBY = 'created_at'

def marsloader(query_api_support = False):
  def marsloader_decorator(func):
    def marsloader_func(request, *args, **kwargs):
      """MARS_loader (Modifying Arguments for the Result Set) 
      
      adds arguments specifically meant to modify the result set 
      (eg. limit, offset and order_by)

      04-05-2011: Modified to Handle the New Query Interface
      New arguments are: group_by, aggregate_by, date_group,
      date_range, generic filters.
      
      Also: No longer checks that the URL ends in a '/'. We assume
      that if you didn't want to call this function, you wouldn't
      have decorated the view with it.
      """

      check_safety()

      # This should be abstracted
      # StatusName 'active' should always be available
      arg_defaults = {
        'limit': 100, 
        'offset': 0,
        'order_by': '-%s'%(DEFAULT_ORDERBY) if not request.GET.has_key('aggregate_by') or not query_api_support else None,
        'status': models.StatusName.objects.get(name='active'),
        }
      query_api_defaults = {
        'group_by': None,
        'aggregate_by': None,
        'date_range': None,
        'date_group': None,
        }

      # Every get paramater should be useful: otherwise we have to treat it as
      # an invalid filter
      new_args = copy.copy(kwargs)
      filters = {}
      for _arg, value in request.GET.iteritems():
        arg = str(_arg)
        try:
          if arg == 'limit':
            new_args[arg] = int(value)
          elif arg == 'offset':
            new_args[arg] = int(value)
          elif arg == 'order_by':
            new_args[arg] = value
          elif arg == 'status':
            new_args[arg] = models.StatusName.objects.get(name=value)
          elif arg == 'group_by' and query_api_support:
            new_args[arg] = value
          elif arg == 'aggregate_by' and query_api_support:
            operator, field = value.split('*')
            field = None if field == '' else field
            new_args[arg] = {'operator':operator, 'field':field} 
          elif arg == 'date_range' and query_api_support:
            field, start_date, end_date = value.split('*')
            start_date = None if start_date == '' else iso8601.parse_utc_date(start_date)
            end_date = None if end_date == '' else iso8601.parse_utc_date(end_date)
            new_args[arg] = {'field':field, 'start_date':start_date, 'end_date':end_date}
          elif arg == 'date_group' and query_api_support:
            field, time_incr = value.split('*')
            new_args[arg] = {'field':field, 'time_incr':time_incr}

          # We assume that all remaining parameters are field-specific query parameters 
          # (i.e. 'lab_type=hematology') if this is a query_api call
          else:
            if query_api_support: 
              
              # Don't do type-checking here: the individual report defines the types of filters
              filters[arg] = value
        except models.StatusName.DoesNotExist:
          raise Http404
        except ValueError:
          return HttpResponseBadRequest('Argument %s must be formatted according to the Indivo Query API'%(arg))

      if query_api_support:
        new_args['filters'] = filters

      # Add defaults for missing params
      for arg, default in arg_defaults.iteritems():
        if not new_args.has_key(arg):
          new_args[arg] = default
    
      if query_api_support:
        for arg, default in query_api_defaults.iteritems():
          if not new_args.has_key(arg):
            new_args[arg] = default

      # Check that the new arguments are all in func()
      if len(inspect.getargspec(func)) > 0:
        for new_arg in new_args.keys():
          if new_arg not in inspect.getargspec(func)[0]:
            raise Exception("Missing arg " + new_arg + " in " + func.func_name)
      
      # call the view
      return func(request, **new_args)

    # Return the wrapped Function
    return functools.update_wrapper(marsloader_func, func)

  # Return the function decorator
  return marsloader_decorator


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
      
      
