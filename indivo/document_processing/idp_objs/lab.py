from indivo.lib import iso8601
from indivo.models import Lab

XML = 'xml'
DOM = 'dom'

class IDP_Lab:

  def post_data(self,  date_measured,
                lab_type=None, 
                lab_name=None, 
                lab_address=None, 
                lab_comments=None,
                first_panel_name=None,
                first_lab_test_name=None,
                first_lab_test_value=None,
                normal_range_minimum=None,
                normal_range_maximum=None,
                non_critical_range_minimum=None,
                non_critical_range_maximum=None):
    """
    SZ: More error checking needs to be performed in this method
    """

    if date_measured:
      date_measured = iso8601.parse_utc_date(date_measured)

    try:
      lab_obj = Lab.objects.create( date_measured=date_measured, 
                                    lab_type=lab_type, 
                                    lab_name=lab_name, 
                                    lab_address=lab_address, 
                                    lab_comments=lab_comments,
                                    first_panel_name = first_panel_name,
                                    first_lab_test_name = first_lab_test_name,
                                    first_lab_test_value = first_lab_test_value,
                                    normal_range_minimum = normal_range_minimum,
                                    normal_range_maximum = normal_range_maximum,
                                    non_critical_range_minimum = non_critical_range_minimum,
                                    non_critical_range_maximum = non_critical_range_maximum)

      return lab_obj
    except Exception, e:
      raise ValueError("problem processing lab report " + str(e))
