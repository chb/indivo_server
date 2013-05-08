"""
Decorators for views
"""
import inspect
from functools import update_wrapper,wraps

from django.http import Http404, HttpResponseBadRequest
from django.db import IntegrityError
from django.db import transaction

from indivo import models
from indivo import check_safety
from indivo.lib import iso8601

DEFAULT_ORDERBY = 'created_at'
QUERY_OPTIONS_ARG = 'query_options'

def marsloader(query_api_support = False):
  def marsloader_decorator(func):
    def marsloader_func(request, *args, **kwargs):
      """MARS_loader (Modifying Arguments for the Result Set) 
      
      adds arguments specifically meant to modify the result set 
      (eg. limit, offset and order_by)

      04-05-2011: Modified to Handle the New Query Interface
      New arguments are: group_by, aggregate_by, date_group,
      date_range, generic report_specific_filters.
      
      Also: No longer checks that the URL ends in a '/'. We assume
      that if you didn't want to call this function, you wouldn't
      have decorated the view with it.
      """
      
      def parse_string(value):
          return value
      
      def parse_int(value):
          return int(value)
      
      def parse_status(value):
          return models.StatusName.objects.get(name=value)
      
      def parse_aggregate_by(value):
          operator, field = value.split('*')
          field = None if field == '' else field
          return {'operator':operator, 'field':field}
      
      def parse_date_range(value):
          field, start_date, end_date = value.split('*')
          start_date = None if start_date == '' else iso8601.parse_iso8601_datetime(start_date)
          end_date = None if end_date == '' else iso8601.parse_iso8601_datetime(end_date)
          return {'field':field, 'start_date':start_date, 'end_date':end_date}
      
      def parse_date_group(value):
          field, time_incr = value.split('*')
          return {'field':field, 'time_incr':time_incr}
      
      def parse_date(value):
          return iso8601.parse_iso8601_datetime(value)
      
      check_safety()
      
      parse_map = {
        'limit': parse_int,
        'offset': parse_int,
        'order_by': parse_string,
        'status': parse_status,
        'group_by': parse_string,
        'aggregate_by': parse_aggregate_by,  
        'date_range': parse_date_range,   
        'date_group': parse_date_group,
        'date_from': parse_date,  # SMART v0.5, transformed to date_range in smart views
        'date_to': parse_date,    # SMART v0.5, transformed to date_range in smart views
      }
      
      ignore_map = {
        'response_format': True              
      }
      
      # This should be abstracted
      # StatusName 'active' should always be available
      arg_defaults = {
        'limit': None, 
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
     
      base_options = {}
      report_specific_filters = {}
      
      # set defaults
      base_options.update(arg_defaults)
      if query_api_support:
          base_options.update(query_api_defaults)
          base_options['filters'] = report_specific_filters
      
      for _arg, value in request.GET.iteritems():
        arg = str(_arg)
        try:
          if parse_map.has_key(arg):
              base_options[arg] = parse_map[arg](value)
          elif ignore_map.has_key(arg):
              pass
          else:
              # might be field-specific query parameter, allow individual reports to type-check
              report_specific_filters[arg] = value
        except models.StatusName.DoesNotExist:
          raise Http404
        except ValueError:
          return HttpResponseBadRequest('Argument %s must be formatted according to the Indivo Query API'%(arg))

      # Check that the new query_options argument is in func()
      if len(inspect.getargspec(func)) > 0:
        if QUERY_OPTIONS_ARG not in inspect.getargspec(func)[0]:
          raise Exception("Missing arg " + QUERY_OPTIONS_ARG + " in " + func.func_name)
      
      # update args
      kwargs[QUERY_OPTIONS_ARG] = base_options
      
      # call the view
      return func(request, **kwargs)

    # Return the wrapped Function
    return update_wrapper(marsloader_func, func)

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
  which we wrap around ourselves, except if we got an IntegrityError from postgres, which
  commit_on_success doesn't handle correctly.
  """

  @wraps(func)
  def _inner_commit(*args, **kwargs):
    try:
      result = func(*args, **kwargs)
    except IntegrityError:
      transaction.set_dirty()
      raise

    if not hasattr(result, 'status_code') or result.status_code != 200:
      transaction.rollback()

    return result

  # layer the commit_on_successoutside of our first check for 200
  # note that, if the wrapped func raises an exception, it goes 
  # right through our decorator here (like butter), and hits the commit_on_success
  # handler which will roll back the transaction then. We keep it simple.
  return transaction.commit_on_success(_inner_commit)
      
def handle_integrity_error(msg=''):
  """
  Roll back the transaction and Return an HttpResponseBadRequest (400) with the passed message
  if the call raises an IntegrityError. This is useful to avoid Postgres aborting transactions
  after an IntegrityError such as a unique constraint violation.
  """
  def integrity_error_decorator(func):

    @wraps(func)
    def _inner_decorator(*args, **kwargs):
      try:
        return func(*args, **kwargs)
      except IntegrityError:
        transaction.rollback()
        return HttpResponseBadRequest(msg)


    return _inner_decorator
  
  return integrity_error_decorator
