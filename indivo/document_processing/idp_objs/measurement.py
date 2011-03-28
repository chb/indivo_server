from indivo.lib import iso8601
from indivo.models import Measurement

XML = 'xml'
DOM = 'dom'

class IDP_Measurement:

  def __init__(self):
    self.type = 'type'
    self.attributes = ['type', 'value', 'unit', 'datetime']

  def process(self, type, doc):
    """
    moving this to etree
    """
    retval = {}
    xmldom = doc[DOM]
    if xmldom is not None:
      attributes = xmldom.attrib
      for attr_name in self.attributes:
        if attributes.has_key(attr_name):
          attr_val = attributes[attr_name]
          retval[attr_name] = attr_val
      if self.attributes.__contains__(self.type):
        retval[self.attributes[self.attributes.index(self.type)]] = type
      if retval:
        return [retval]
    return False

  def post_data(self, type, value, unit, datetime):
    try:
      measurement_obj = Measurement.objects.create( type=type,
                                  value=value,
                                  unit=unit,
                                  datetime=iso8601.parse_utc_date(datetime))
      return measurement_obj
    except Exception, e:
      raise ValueError("problem processing measurement report " + str(e))

