from indivo.lib import iso8601
from indivo.models import Problem

XML = 'xml'
DOM = 'dom'

class IDP_Problem:

  def post_data(self,  date_onset=None, 
                       date_resolution=None, 
                       name=None,
                       name_type=None,
                       name_value=None,
                       name_abbrev=None, 
                       comments=None,
                       diagnosed_by=None):
    """
    SZ: More error checking needs to be performed in this method
    """

    if date_onset:
      date_onset=iso8601.parse_utc_date(date_onset)

    if date_resolution:
      date_resolution=iso8601.parse_utc_date(date_resolution)

    try:
      problem_obj = Problem.objects.create( date_onset=date_onset,
                                            date_resolution=date_resolution,
                                            name=name,
                                            name_type=name_type,
                                            name_value=name_value,
                                            name_abbrev=name_abbrev,
                                            comments=comments,
                                            diagnosed_by=diagnosed_by)

      return problem_obj
    except Exception, e:
      raise ValueError("problem processing problemlist report " + str(e))
