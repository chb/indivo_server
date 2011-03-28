"""
some report utilities
"""

import functools

ORDER_BY_MAPPINGS = {
    'creator' : 'document__creator__email'
}

ORDER_BY = 'order_by'

def report_orderby_update(order_by):
    """
    update the order_by given the mappings above
    """
    if not order_by:
        return None

    if order_by[1] == '-':
        return '-' + ORDER_BY_MAPPINGS.get(order_by[1:], order_by)
    else:
        return ORDER_BY_MAPPINGS.get(order_by, order_by)
    

##
## NOTE: we cannot use this decorator yet
## because marsloader looks at inspect.argspec, which inherently
## kills the ability to use decorators. We should move away from
## using inspect in our code, there's no good reason to do this.
##
def report_orderby(func):
    """
    adjust the order_by parameter to be appropriately massaged
    to pull order_by from the right join table
    """
    
    def _inner_report_orderby(*args, **kwargs):
        order_by = kwargs.get(ORDER_BY, None)
        new_order_by = report_orderby_update(order_by)
        if new_order_by:
            kwargs[ORDER_BY] = new_order_by

        return func(*args, **kwargs)

    new_func = functools.update_wrapper(_inner_report_orderby, func)
    import pdb; pdb.set_trace()
    return new_func
            
        
