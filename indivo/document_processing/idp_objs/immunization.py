from indivo.lib import iso8601
from indivo.models import Immunization

XML = 'xml'
DOM = 'dom'

class IDP_Immunization:

  def post_data(self,   date_administered=None, 
                        administered_by=None, 
                        vaccine_type=None,
                        vaccine_type_type=None, 
                        vaccine_type_value=None,
                        vaccine_type_abbrev=None,
                        vaccine_manufacturer=None,
                        vaccine_lot=None,
                        vaccine_expiration=None,
                        sequence=None,
                        anatomic_surface=None,
                        anatomic_surface_type=None,
                        anatomic_surface_value=None,
                        anatomic_surface_abbrev=None,
                        adverse_event=None):
    """
    SZ: More error checking needs to be performed in this method
    """

    if date_administered: date_administered = iso8601.parse_utc_date(date_administered)

    try:
      immunization_obj = Immunization.objects.create( date_administered=date_administered,
                                                      administered_by=administered_by,
                                                      vaccine_type=vaccine_type,
                                                      vaccine_type_type=vaccine_type_type,
                                                      vaccine_type_value=vaccine_type_value,
                                                      vaccine_type_abbrev=vaccine_type_abbrev,
                                                      vaccine_manufacturer=vaccine_manufacturer,
                                                      vaccine_lot=vaccine_lot,
                                                      vaccine_expiration=vaccine_expiration,
                                                      sequence=sequence,
                                                      anatomic_surface=anatomic_surface,
                                                      anatomic_surface_type=anatomic_surface_type,
                                                      anatomic_surface_value=anatomic_surface_value,
                                                      anatomic_surface_abbrev=anatomic_surface_abbrev,
                                                      adverse_event=adverse_event)
      return immunization_obj
    except Exception, e:
      raise ValueError("problem processing immunization report " + str(e))
