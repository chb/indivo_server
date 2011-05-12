"""
Common Functionality for support of the Query API
"""

from indivo.lib.utils import carenet_filter, render_template
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

OUTPUT_TEMPLATE = 'reports/report'
AGGREGATE_TEMPLATE = 'reports/aggregate.xml'

class FactQuery(object):
    def __init__(self, model, model_filters,
                 group_by, date_group, aggregate_by,
                 limit, offset, order_by,
                 status, date_range, filters,
                 record=None, carenet=None):
        self.model = model
        self.valid_filters = model_filters
        self.group_by = group_by
        self.date_group = date_group
        self.aggregate_by = aggregate_by
        self.limit = limit
        self.offset = offset
        self.order_by = order_by
        self.status = status
        self.date_range = date_range
        self.query_filters = filters
        
        self.results = None
        self.trc = None
        self.aggregate_p = None
        self.grouping_p = None
        self.flat_aggregation = None

        self.carenet = carenet
        self.record = carenet.record if carenet else record

    def render(self, item_template, output_template=OUTPUT_TEMPLATE):
        if self.results is None:
            self.execute()

        if self.aggregate_by:
            item_template = AGGREGATE_TEMPLATE
        template_args = {'fobjs': self.results,
                         'trc': self.trc,
                         'group_by': self.group_by, 
                         'date_group': self.date_group, 
                         'aggregate_by': self.aggregate_by,
                         'limit': self.limit, 
                         'offset': self.offset,
                         'order_by': self.order_by,
                         'status': self.status,
                         'date_range': self.date_range, 
                         'filters': self.query_filters,        
                         'item_template': item_template
                         }
        return render_template(output_template, template_args, type="xml")

    def execute(self):
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
        results = self.model.objects.all()

        # 1. Apply filter operators (but not limit/offset).
        results = self._apply_filters(results)

        # 2. Evaluate group_by or date_group
        results = self._apply_grouping(results)

        # 3. Evaluate aggregate_by
        self.grouping_p = self.group_by or self.date_group
        self.flat_aggregation = self.aggregate_by and not self.grouping_p
        results = self._apply_aggregation(results)

        # 4. Order_by
        # ignore order_by if we have a single aggregation    
        if not self.flat_aggregation:
            results = self._apply_ordering(results)
    
        # 5. limit and offset. Must evaluate the queryset here, so Django doesn't do fuzzy stuff
        # with the ordering.

        # Evaluate the QuerySet and format it appropriately even with differing code paths above
        if self.flat_aggregation:
            results = [results] # [{'aggregation': 'value'}]
        else:
            results = list(results) # [obj1, obj2, ...] or [{'group_field': 'value', 'aggregation':'agg_value'} ..]

        # Grab the total result count before we apply paging and lose it
        self.trc = len(results)

        # Handle Paging, ignore if we have a single aggregation
        if not self.flat_aggregation:
            results = results[self.offset:self.offset+self.limit]

        # And we're done!
        self.results = results

    def _apply_filters(self, results):
        # Carenet filters.
        # DH 04-07-2011: Moved up front and changed to not evaluate the queryset

        # Need to allow queries with no record or carenet, i.e., Audit, which isn't constrained to a single record
        if self.record:
            results = results.filter(record=self.record)
        results = carenet_filter(self.carenet, results)


        filter_args = {}
        for field, val in self.query_filters.iteritems():
            if self.valid_filters.has_key(field):
                field_type = self.valid_filters[field][1]
                try:
                    parsed_val = EXPOSED_TYPES[field_type](val)
                    filter_args[self.valid_filters[field][0]] = parsed_val
                except:
                    raise ValueError('Invalid argument type for field %s: expected %s, got %s'%(field, field_type, val))
            else:
                raise ValueError('Invalid filter for fact type %s: %s'%(self.model.__name__, field))
  
        if self.date_range:
            if self.valid_filters.has_key(self.date_range['field']):
                field_type = self.valid_filters[self.date_range['field']][1]
                if field_type != DATE:
                    raise ValueError('Date Ranges may only be calculated over fields of type "date": got %s(%s)'%(self.date_range['field'], field_type))

                if self.date_range['start_date']:
                    filter_args['%s__gte'%(self.valid_filters[self.date_range['field']][0])] = self.date_range['start_date']
                if self.date_range['end_date']:
                    filter_args['%s__lte'%(self.valid_filters[self.date_range['field']][0])] = self.date_range['end_date']
            else:
                raise ValueError('Invalid date range filter for fact type %s: %s'%(self.model.__name__, date_range['field']))

        if self.status:
            filter_args['document__status'] = self.status

        if filter_args:
            results = results.filter(**filter_args)
    
        # Results look like:
        # [obj1, obj2, ...] For every Fact object we haven't filtered out
        return results

    def _apply_grouping(self, results):
        group_field = 'all'

        # Handle the ordinary group
        if self.group_by:
            if self.valid_filters.has_key(self.group_by):          
                group_field = self.valid_filters[self.group_by][0]
            else:
                raise ValueError('Invalid grouping field for fact type %s: %s'%(model.__name__, group_by))

        # Handle the date group
        elif self.date_group:
            if self.valid_filters.has_key(self.date_group['field']):
                field_type = self.valid_filters[self.date_group['field']][1]
                if field_type != DATE:
                    raise ValueError('Date groups may only be calculated over fields of type "date": got %s(%s)'%(self.date_group['field'], self.field_type))

                group_field = self.valid_filters[self.date_group['field']][0]
                date_incr = self.date_group['time_incr']
                if TIME_INCRS.has_key(date_incr):
                    format_str = TIME_INCRS[date_incr]
                    results = results.extra(select={date_incr:"to_char(%s, '%s')"%(group_field, format_str)})

                    # From now on, we look at the date-formatted string only
                    group_field = date_incr
                else:
                    raise ValueError('Invalid date_group Increment: %s'%(time_incr))
            else:
                raise ValueError('Invalid grouping field for fact type %s: %s'%(self.model.__name__, self.date_group['field']))
    
        if group_field is not 'all':
            results = results.values(group_field)

        # Results look like:
        # [{'group_field': 'value1'}, {'group_field': 'value2'}], 1 dict per Fact object if we grouped
        # if there was no grouping, results look like: [obj1, obj2, ...]
        return results

    def _apply_aggregation(self, results):
        if self.aggregate_by:      
            agg_field = self.aggregate_by['field']
            if self.valid_filters.has_key(agg_field):
                agg_field_type = self.valid_filters[agg_field][1]

                # Look up the operator
                if AGG_OPS.has_key(self.aggregate_by['operator']):    
                    agg = AGG_OPS[self.aggregate_by['operator']]
                    agg_func_types = agg[1]
                    if agg_field_type not in agg_func_types:
                        raise ValueError('Cannot apply aggregate function %s (type %s) to field %s (type %s)'%(self.aggregate_by['operator'], agg_func_type, agg_field, agg_field_type))

                    agg_func = agg[0]
                    agg_args = { 'aggregation': agg_func(self.valid_filters[agg_field][0])}
                else:
                    raise ValueError('Invalid aggregation operator: %s'%(self.aggregate_by['operator']))

                # If we grouped, handle differently
                if self.grouping_p:
                    results = results.annotate(**agg_args)
                else:
                    results = results.aggregate(**agg_args)
            else:
                raise ValueError('Invalid aggregation field for fact type %s: %s'%(self.model.__name__, agg_field))
        else:
            if self.grouping_p:
                raise ValueError('Cannot make grouped queries without specifying an Aggregation!')

        # Results look like:
        # [{'group_field' : value1, 'aggregation': agg_value} ...] 1 dict per each UNIQUE group_field value
        # If there was no grouping, results look like: {'aggregation': value'}
        # If there was no grouping OR aggregation, results look like: [obj1, obj2...]    
        return results

    def _apply_ordering(self, results):
        if self.order_by:
            desc = self.order_by[0] == '-'
            order_by_field_ext = self.order_by if not desc else self.order_by[1:]

            # get the internal model field for order by
            if self.valid_filters.has_key(order_by_field_ext):
                order_by_field = self.valid_filters[order_by_field_ext][0]
            else:
                raise ValueError('Invalid order by field for fact type %s: %s'%(self.model.__name__, self.order_by))

            # Handle special cases of aggregation and grouping
            if self.aggregate_by and order_by_field_ext == self.aggregate_by['field']:
                order_by_field = 'aggregation'
            elif self.group_by and order_by_field_ext != self.group_by:
                raise ValueError('OrderBy fields in aggregations may only refer to the grouping field or the aggregation field. Your field was: %s'%(self.order_by))
            elif self.date_group and order_by_field_ext != self.date_group['field']:
                raise ValueError('OrderBy fields in aggregations may only refer to the grouping field or the aggregation field. Your field was: %s'%(self.order_by))
            elif self.date_group:
                order_by_field = self.date_group['time_incr']

            # Do the ordering
            order_by_str = order_by_field if not desc else '-'+order_by_field
            results = results.order_by(order_by_str)    
        else:
            # Clear ordering if none was specified, to avoid bad interactions with grouping
            results = results.order_by()

        return results
