"""
Validators useful for attaching to data models.
"""

from django.core.exceptions import ValidationError

class ValueInSetValidator(object):
    def __init__(self, valid_values, nullable=False):
        self.valid_values = valid_values
        if nullable:
            valid_values.append(None)
            valid_values.append('')

    def __call__(self, value):
        if value not in self.valid_values:
            raise ValidationError("Invalid value: %s. Expected one of: %s"%(value, ", ".join(self.valid_values)))


