from indivo.lib import iso8601
from indivo.models import Procedure

XML = 'xml'
DOM = 'dom'

class IDP_Procedure:

  def post_data(self,  date_performed=None, 
                       name=None, 
                       name_type=None,
                       name_value=None,
                       name_abbrev=None,
                       provider_name=None, 
                       provider_institution=None, 
                       location=None,
                       comments=None):
    """
    SZ: More error checking needs to be performed in this method
    """

    if date_performed: date_performed = iso8601.parse_utc_date(date_performed)

    try:
      procedure_obj = Procedure.objects.create( date_performed=date_performed, 
                                                name=name, 
                                                name_type=name_type, 
                                                name_value=name_value, 
                                                name_abbrev=name_abbrev, 
                                                provider_name=provider_name,
                                                provider_institution=provider_institution,
                                                location=location,
                                                comments=comments)
      return procedure_obj
    except Exception, e:
      raise ValueError("problem processing procedure report " + str(e))
