"""
Validators useful for attaching to data models.
"""

from django.core.exceptions import ValidationError

class ValueInSetValidator(object):
    """ Validates that a value is within a set of possible values.

    The optional 'nullable' flag determines whether or not the value
    may also be empty.
    
    """

    def __init__(self, valid_values, nullable=False):
        self.valid_values = valid_values
        self.nullable = nullable

    def __call__(self, value):
        if self.nullable and not value:
            return

        if value not in self.valid_values:
            raise ValidationError("Invalid value: %s. Expected one of: %s"%(value, ", ".join(map(str, self.valid_values))))


class ExactValueValidator(ValueInSetValidator):
    """ Validates that a value is exactly equal to a certain value.

    The optional 'nullable' flag determines whether or not the value
    may also be empty.
    
    """

    def __init__(self, valid_value, nullable=False):
        return super(ExactValueValidator, self).__init__([valid_value], nullable=nullable)
       
 
class NonNullValidator(object):
    """ Validates that a value is not null.
    
    A 'null' value is anything that Django would store as NULL in a database: ``None``, ``""``, ``[]``,
    ``()``, or ``{}``. Note that other python objects that evaluate to false (``0``, ``False``) are not 
    actually null values, as they represent data. 

    This validator is useful for validating that strings are non-empty, for example.
    
    """

    # This is a special validator: it is actually just a proxy for setting blank=False on the field
    pass
