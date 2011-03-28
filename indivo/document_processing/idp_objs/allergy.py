from indivo.lib import iso8601
from indivo.models import Allergy

XML = 'xml'
DOM = 'dom'

class IDP_Allergy:

  def post_data(self,  date_diagnosed=None, 
                       diagnosed_by=None, 
                       allergen_type=None, 
                       allergen_type_type=None, 
                       allergen_type_value=None, 
                       allergen_type_abbrev=None, 
                       allergen_name=None,
                       allergen_name_type=None,
                       allergen_name_value=None,
                       allergen_name_abbrev=None,
                       reaction=None,
                       specifics=None):
    """
    SZ: More error checking needs to be performed in this method
    """

    if date_diagnosed:
      date_diagnosed = iso8601.parse_utc_date(date_diagnosed)

    try:
      allergy_obj = Allergy.objects.create( date_diagnosed=date_diagnosed, 
                                            diagnosed_by=diagnosed_by, 
                                            allergen_type=allergen_type, 
                                            allergen_type_type=allergen_type_type, 
                                            allergen_type_value=allergen_type_value, 
                                            allergen_type_abbrev=allergen_type_abbrev, 
                                            allergen_name=allergen_name, 
                                            allergen_name_type=allergen_name_type, 
                                            allergen_name_value=allergen_name_value, 
                                            allergen_name_abbrev=allergen_name_abbrev, 
                                            reaction=reaction, 
                                            specifics=specifics)

      return allergy_obj
    except Exception, e:
      raise ValueError("problem processing allergy report " + str(e))
