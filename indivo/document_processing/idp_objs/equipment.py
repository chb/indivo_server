from indivo.lib import iso8601
from indivo.models import Equipment

XML = 'xml'
DOM = 'dom'

class IDP_Equipment:

  def post_data(self,  date_started=None,
                date_stopped=None,
                name=None, 
                vendor=None, 
                description=None):
    """
    SZ: More error checking needs to be performed in this method
    """

    try:
      if date_started:
        date_started = iso8601.parse_utc_date(date_started)

      if date_stopped:
        date_stopped = iso8601.parse_utc_date(date_stopped)

      equipment_obj = Equipment.objects.create( date_started=date_started,
                                                date_stopped=date_stopped,
                                                name=name, 
                                                vendor=vendor, 
                                                description=description)

      return equipment_obj
    except Exception, e:
      raise ValueError("problem processing equipment report " + str(e))
