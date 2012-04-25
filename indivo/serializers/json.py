"""
Indivo JSON Serializer

"""

import datetime
from indivo.lib.iso8601 import format_utc_date
from indivo.serializers.python import Serializer as IndivoPythonSerializer
from django.utils import simplejson

try:
    import decimal
except ImportError:
    from django.utils import _decimal as decimal    # Python 2.3 fallback

class Serializer(IndivoPythonSerializer):
    """
    Convert a queryset to JSON.
    """
    internal_use_only = False

    def end_serialization(self):
        self.options.pop('stream', None)
        self.options.pop('fields', None)
        simplejson.dump(self.objects, self.stream, cls=IndivoJSONEncoder, **self.options)

    def getvalue(self):
        if callable(getattr(self.stream, 'getvalue', None)):
            return self.stream.getvalue()

class IndivoJSONEncoder(simplejson.JSONEncoder):
    """
    Encodes datetime/date/time as ISO8601
    """

    def default(self, o):
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.time):
            return format_utc_date(o)
        elif isinstance(o, datetime.date):
            return format_utc_date(o, date_only=True) 
        else:
            return super(IndivoJSONEncoder, self).default(o)