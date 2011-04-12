"""
Indivo Views -- Lab
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.utils import render_template, carenet_filter
from indivo.models import *
from reportutils import report_orderby_update
from indivo.lib.iso8601 import parse_utc_date
import re

from django.db.models import Avg, Count, Max, Min, Sum

def parse_str(val):
  return str(val)

def parse_float(val):
  return float(val)

ANY = 'any'
DATE = 'date'
STRING = 'string'
NUMBER = 'number'

AGG_OPS = {
'sum': (Sum, 'number'),
'avg': (Avg, 'number'),
'max': (Max, 'number'),
'min': (Min, 'number'),
'count': (Count, 'any')
}

EXPOSED_TYPES = {
  STRING: parse_str,
  DATE: parse_utc_date,
  NUMBER: parse_float
  }

LAB_FILTERS = {
  'lab_type': ('lab_type', 'string'),
  'date_measured': ('date_measured', 'date'),
  'lab_test_name': ('first_lab_test_name', 'string'),
  'lab_test_value': ('first_lab_test_value', 'string'),
  DEFAULT_ORDERBY : ('created_at', 'date')
}

TIME_INCRS = {
  'hour': 'YYYY-MM-DD-HH24',
  'day': 'YYYY-MM-DD',
  'week': 'YYYY-WW',
  'month': 'YYYY-MM',
  'year': 'YYYY',
  'hourofday': 'HH24',
  'dayofweek': 'D',
  'weekofyear': 'WW',
  'monthofyear': 'MM'
}

@marsloader(query_api_support=True)
def lab_list(request, status, 
             group_by, aggregate_by, date_range, date_group, filters,
             limit, offset, order_by, record=None, carenet=None):

  # New API Query Interface (to be released for Beta 3)
  # Query operators are evaluated as follows:
  # 1. filter operators, including date_range but excluding limit and offset, are applied first.
  # 2. Group_by and date_group, if supplied, are evaluated next
  # 3. Aggregate by is evaluated
  # 4. order_by, limit and offset are applied.

  if carenet:
    record = carenet.record
  if not record:
    return HttpResponseBadRequest('Called Lab list with invalid record and/or carenet')

  # This is okay, Django evaluates lazily
  labs = Lab.objects.filter(record=record)

  # 1. Apply filter operators (but not limit/offset). Carenet filters will also need to come here

  # Carenet filters. With aggregation, this is now WRONG: Carenet filters must be applied 
  # before aggregation, to avoid including documents outside the carenet.
  # DH 04-07-2011: Moved and fixed
  labs = carenet_filter(carenet, labs)

  filter_args = {}
  for field, val in filters.iteritems():
    if LAB_FILTERS.has_key(field):
      field_type = LAB_FILTERS[field][1]
      try:
        parsed_val = EXPOSED_TYPES[field_type](val)
      except:
        return HttpResponseBadRequest('Invalid argument type for field %s: expected %s, got %s'%(field, field_type, val))
      filter_args[LAB_FILTERS[field][0]] = parsed_val
    else:
      return HttpResponseBadRequest('Invalid filter for Labs: %s'%(field))
  
  if date_range:
    if LAB_FILTERS.has_key(date_range['field']):
      field_type = LAB_FILTERS[date_range['field']][1]
      if field_type != DATE:
        return HttpResponseBadRequest('Date Ranges may only be calculated over fields of type "date": got %s(%s)'%(date_range['field'], field_type))

      if date_range['start_date']:
        filter_args['%s__gte'%LAB_FILTERS[date_range['field']][0]] = date_range['start_date']
      if date_range['end_date']:
        filter_args['%s__lte'%LAB_FILTERS[date_range['field']][0]] = date_range['end_date']
    else:
      return HttpResponseBadRequest('Invalid date range filter for Labs: %s'%(date_range['field']))

  if status:
    filter_args['document__status'] = status

  if filter_args:
    labs = labs.filter(**filter_args)

  # AFTER ITEM 1: Results look like:
  # [obj1, obj2, ...] For every Fact object we haven't filtered out

  # 2. Evaluate group_by or date_group
  group_field = 'all'

  # Handle the ordinary group
  if group_by:
    if LAB_FILTERS.has_key(group_by):          
      group_field = LAB_FILTERS[group_by][0]
    else:
      return HttpResponseBadRequest('Invalid grouping field for Labs: %s'%(group_by))

  # Handle the date group
  elif date_group:
    if LAB_FILTERS.has_key(date_group['field']):
      field_type = LAB_FILTERS[date_group['field']][1]
      if field_type != DATE:
        return HttpResponseBadRequest('Date groups may only be calculated over fields of type "date": got %s(%s)'%(date_group['field'], field_type))

      group_field = LAB_FILTERS[date_group['field']][0]
      date_incr = date_group['time_incr']
      if TIME_INCRS.has_key(date_group['time_incr']):
        format_str = TIME_INCRS[date_group['time_incr']]
        labs = labs.extra(select={date_incr:"to_char(%s, '%s')"%(group_field, format_str)})

        # From now on, we look at the date-formatted string only
        group_field = date_incr
      else:
        return HttpResponseBadRequest('Invalid date_group Increment: %s'%(time_incr))
    else:
      return HttpResponseBadRequest('Invalid grouping field for Labs: %s'%(date_group['field']))
    
  if group_field is not 'all':
    labs = labs.values(group_field)

  # AFTER ITEM 2: Results look like:
  # [{'group_field': 'value1'}, {'group_field': 'value2'}], 1 dict per Fact object if we grouped
  # if there was no grouping, results look like: [obj1, obj2, ...]

  # 3. Evaluate aggregate_by
  flat_aggregation = False
  if aggregate_by:      
    agg_field = aggregate_by['field']
    if LAB_FILTERS.has_key(agg_field):
      agg_field_type = LAB_FILTERS[agg_field][1]
               
      #Look up the operator
      if AGG_OPS.has_key(aggregate_by['operator']):    
        agg = AGG_OPS[aggregate_by['operator']]
        agg_func_type = agg[1]
        if agg_field_type != agg_func_type and agg_func_type != ANY:
          return HttpResponseBadRequest('Cannot apply aggregate function %s (type %s) to field %s (type %s)'%(aggregate_by['operator'], agg_func_type, agg_field, agg_field_type))

        agg_func = agg[0]
        agg_args = { 'aggregation': agg_func(LAB_FILTERS[agg_field][0])}
      else:
        return HttpResponseBadRequest('Invalid aggregation operator: %s'%(aggregate_by['operator']))

      # If we grouped, handle differently
      if group_by or date_group:
        labs = labs.annotate(**agg_args)
      else:
        flat_aggregation = True
        labs = labs.aggregate(**agg_args)

    else:
      return HttpResponseBadRequest('Invalid aggregation field for Labs: %s'%(agg_field))
  else:
    if group_by or date_group:
      return HttpResponseBadRequest('Cannot make grouped queries without specifying an Aggregation!')


  # AFTER ITEM 3: results look like:
  # [{'group_field' : value1, 'aggregation': agg_value} ...] 1 dict per each UNIQUE group_field value
  # If there was no grouping, results look like: {'aggregation': value'}
  # If there was no grouping OR aggregation, results look like: [obj1, obj2...]

  # 4. Order_by, limit, and offset. Must evaluate the queryset here, so Django doesn't do fuzzy stuff
  # with the ordering. Also, evaluate carenet filter here (should be earlier for max efficiency).

  # ignore order_by if we have a single aggregation
  if order_by and not flat_aggregation:
    desc = order_by[0] == '-'
    order_by_field_ext = order_by if not desc else order_by[1:]

    # get the internal model field for order by
    if LAB_FILTERS.has_key(order_by_field_ext):
      order_by_field = LAB_FILTERS[order_by_field_ext][0]
    else:
      return HttpResponseBadRequest('Invalid order by field for Labs: %s'%(order_by))

    # Handle special cases of aggregation and grouping
    if aggregate_by and order_by_field_ext == aggregate_by['field']:
      order_by_field = 'aggregation'
    elif group_by and order_by_field_ext != group_by:
      return HttpResponseBadRequest('OrderBy fields in aggregations may only refer to the grouping field or the aggregation field. Your field was: %s'%(order_by))
    elif date_group and order_by_field_ext != date_group['field']:
        return HttpResponseBadRequest('OrderBy fields in aggregations may only refer to the grouping field or the aggregation field. Your field was: %s'%(order_by))
    elif date_group:
      order_by_field = date_incr

    # Do the ordering
    order_by_str = order_by_field if not desc else '-'+order_by_field
    labs = labs.order_by(order_by_str)    
  else:
    # Clear ordering if none was specified, to avoid bad interactions with grouping
    if not flat_aggregation:
      labs = labs.order_by()


  # Evaluate the Query right here, and format it appropriately even with differing code paths above
  if flat_aggregation:
    labs = [labs] # [{'aggregation': 'value'}]
  else:
    labs = list(labs) # [obj1, obj2, ...] or [{'group_field': 'value', 'aggregation':'agg_value'} ..]

  # Handle Paging, ignore if we have a single aggregation
  trc = len(labs)
  if not flat_aggregation:
    labs = labs[offset:offset+limit]

  # And we're done! output the appropriate template
  if aggregate_by:
    template = 'reports/aggregate'
    template_args = {'data': labs,
                     'trc': trc, 
                     'limit': limit,
                     'offset': offset,
                     'order_by' : None if flat_aggregation else order_by}
    # Hack until we build the aggregate schema
    return HttpResponse(str(labs))

  else:
    template = 'reports/labs'
    template_args = { 'labs' : labs, 
                      'trc' : trc,
                      'limit' : limit,
                      'offset' : offset,
                      'order_by' : order_by } 
    
  return render_template(template, template_args, type="xml")
