"""
Common Functionality for support of the Query API
"""

from indivo.lib.utils import carenet_filter
from indivo.lib.iso8601 import parse_utc_date
from django.db.models import Avg, Count, Max, Min, Sum

DATE = 'date'
STRING = 'string'
NUMBER = 'number'

EXPOSED_TYPES = {
  STRING: str,
  DATE: parse_utc_date,
  NUMBER: float
  }

AGG_OPS = {
'sum': (Sum, [NUMBER]),
'avg': (Avg, [NUMBER]),
'max': (Max, [NUMBER, DATE]),
'min': (Min, [NUMBER, DATE]),
'count': (Count, [NUMBER, DATE, STRING])
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

def execute_query(model, model_filters,
                  group_by, date_group, aggregate_by,
                  limit, offset, order_by,
                  status, date_range, filters,
                  record=None, carenet=None):

    '''
    New API Query Interface (to be released for Beta 3)
    Query operators are evaluated as follows:
    1. filter operators, including date_range but excluding limit and offset, are applied first.
    2. Group_by and date_group, if supplied, are evaluated next
    3. Aggregate by is evaluated
    4. order_by is applied
    5. We evaluate the query to get an ordered list of results, the apply limit and offset.
    '''

    # This is okay, Django evaluates lazily
    results = model.objects.all()

    # 1. Apply filter operators (but not limit/offset).
    results = apply_filters(results, record, carenet, filters, date_range, status, model_filters, model)

    # 2. Evaluate group_by or date_group
    results = apply_grouping(results, group_by, date_group, model_filters, model)

    # 3. Evaluate aggregate_by
    grouping_p = group_by or date_group
    flat_aggregation = aggregate_by and not grouping_p
    results = apply_aggregation(results, aggregate_by, model_filters, grouping_p, model)

    # 4. Order_by
    # ignore order_by if we have a single aggregation    
    if not flat_aggregation:
        results = apply_ordering(results, order_by, model_filters, aggregate_by, group_by, date_group, model)
    
    # 5. limit and offset. Must evaluate the queryset here, so Django doesn't do fuzzy stuff
    # with the ordering.

    # Evaluate the QuerySet and format it appropriately even with differing code paths above
    if flat_aggregation:
        results = [results] # [{'aggregation': 'value'}]
    else:
        results = list(results) # [obj1, obj2, ...] or [{'group_field': 'value', 'aggregation':'agg_value'} ..]

    # Grab the total result count before we apply paging and lose it
    trc = len(results)

    # Handle Paging, ignore if we have a single aggregation
    if not flat_aggregation:
        results = results[offset:offset+limit]

    # And we're done! Return results, total result count, and whether or not the results are an aggregate
    return (results, trc, aggregate_by)

def apply_filters(results, record, carenet, filters, date_range, status, valid_filters, model):
    if carenet:
        record = carenet.record
    
    # Need to allow queries with no record or carenet, i.e. the Audit table, which has 'record_id', not 'record'
    if record:
        results = results.filter(record=record)

    # Carenet filters.
    # DH 04-07-2011: Moved up front and changed to not evaluate the queryset
    results = carenet_filter(carenet, results)


    filter_args = {}
    for field, val in filters.iteritems():
        if valid_filters.has_key(field):
            field_type = valid_filters[field][1]
            try:
                parsed_val = EXPOSED_TYPES[field_type](val)
                filter_args[valid_filters[field][0]] = parsed_val
            except:
                raise ValueError('Invalid argument type for field %s: expected %s, got %s'%(field, field_type, val))
        else:
            raise ValueError('Invalid filter for fact type %s: %s'%(model.__name__, field))
  
    if date_range:
        if valid_filters.has_key(date_range['field']):
            field_type = valid_filters[date_range['field']][1]
            if field_type != DATE:
                raise ValueError('Date Ranges may only be calculated over fields of type "date": got %s(%s)'%(date_range['field'], field_type))

            if date_range['start_date']:
                filter_args['%s__gte'%(valid_filters[date_range['field']][0])] = date_range['start_date']
            if date_range['end_date']:
                filter_args['%s__lte'%(valid_filters[date_range['field']][0])] = date_range['end_date']
        else:
            raise ValueError('Invalid date range filter for fact type %s: %s'%(model.__name__, date_range['field']))

    if status:
        filter_args['document__status'] = status

    if filter_args:
        results = results.filter(**filter_args)
    
    # Results look like:
    # [obj1, obj2, ...] For every Fact object we haven't filtered out
    return results

def apply_grouping(results, group_by, date_group, model_filters, model):
    group_field = 'all'

    # Handle the ordinary group
    if group_by:
        if model_filters.has_key(group_by):          
            group_field = model_filters[group_by][0]
        else:
            raise ValueError('Invalid grouping field for fact type %s: %s'%(model.__name__, group_by))

    # Handle the date group
    elif date_group:
        if model_filters.has_key(date_group['field']):
            field_type = model_filters[date_group['field']][1]
            if field_type != DATE:
                raise ValueError('Date groups may only be calculated over fields of type "date": got %s(%s)'%(date_group['field'], field_type))

            group_field = model_filters[date_group['field']][0]
            date_incr = date_group['time_incr']
            if TIME_INCRS.has_key(date_incr):
                format_str = TIME_INCRS[date_incr]
                results = results.extra(select={date_incr:"to_char(%s, '%s')"%(group_field, format_str)})

                # From now on, we look at the date-formatted string only
                group_field = date_incr
            else:
                raise ValueError('Invalid date_group Increment: %s'%(time_incr))
        else:
            raise ValueError('Invalid grouping field for fact type %s: %s'%(model.__name__, date_group['field']))
    
    if group_field is not 'all':
        results = results.values(group_field)

    # Results look like:
    # [{'group_field': 'value1'}, {'group_field': 'value2'}], 1 dict per Fact object if we grouped
    # if there was no grouping, results look like: [obj1, obj2, ...]
    return results

def apply_aggregation(results, aggregate_by, model_filters, grouping_p, model):
    if aggregate_by:      
        agg_field = aggregate_by['field']
        if model_filters.has_key(agg_field):
            agg_field_type = model_filters[agg_field][1]

            # Look up the operator
            if AGG_OPS.has_key(aggregate_by['operator']):    
                agg = AGG_OPS[aggregate_by['operator']]
                agg_func_types = agg[1]
                if agg_field_type not in agg_func_types:
                    raise ValueError('Cannot apply aggregate function %s (type %s) to field %s (type %s)'%(aggregate_by['operator'], agg_func_type, agg_field, agg_field_type))

                agg_func = agg[0]
                agg_args = { 'aggregation': agg_func(model_filters[agg_field][0])}
            else:
                raise ValueError('Invalid aggregation operator: %s'%(aggregate_by['operator']))

            # If we grouped, handle differently
            if grouping_p:
                results = results.annotate(**agg_args)
            else:
                results = results.aggregate(**agg_args)
        else:
            raise ValueError('Invalid aggregation field for fact type %s: %s'%(model.__name__, agg_field))
    else:
        if grouping_p:
            raise ValueError('Cannot make grouped queries without specifying an Aggregation!')

    # Results look like:
    # [{'group_field' : value1, 'aggregation': agg_value} ...] 1 dict per each UNIQUE group_field value
    # If there was no grouping, results look like: {'aggregation': value'}
    # If there was no grouping OR aggregation, results look like: [obj1, obj2...]    
    return results

def apply_ordering(results, order_by, model_filters,
                   aggregate_by, group_by, date_group, model):

    if order_by:
        desc = order_by[0] == '-'
        order_by_field_ext = order_by if not desc else order_by[1:]

        # get the internal model field for order by
        if model_filters.has_key(order_by_field_ext):
            order_by_field = model_filters[order_by_field_ext][0]
        else:
            raise ValueError('Invalid order by field for fact type %s: %s'%(model.__name__, order_by))

        # Handle special cases of aggregation and grouping
        if aggregate_by and order_by_field_ext == aggregate_by['field']:
            order_by_field = 'aggregation'
        elif group_by and order_by_field_ext != group_by:
            raise ValueError('OrderBy fields in aggregations may only refer to the grouping field or the aggregation field. Your field was: %s'%(order_by))
        elif date_group and order_by_field_ext != date_group['field']:
            raise ValueError('OrderBy fields in aggregations may only refer to the grouping field or the aggregation field. Your field was: %s'%(order_by))
        elif date_group:
            order_by_field = date_group['time_incr']

        # Do the ordering
        order_by_str = order_by_field if not desc else '-'+order_by_field
        results = results.order_by(order_by_str)    
    else:
        # Clear ordering if none was specified, to avoid bad interactions with grouping
        results = results.order_by()

    return results
