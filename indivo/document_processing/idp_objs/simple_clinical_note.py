from indivo.lib import iso8601
from indivo.models import SimpleClinicalNote

XML = 'xml'
DOM = 'dom'

class IDP_SimpleClinicalNote:

  def post_data(self,  date_of_visit=None, 
                       finalized_at = None,
                       visit_type=None, 
                       visit_type_type=None,
                       visit_type_value=None,
                       visit_type_abbrev=None,
                       visit_location=None,
                       specialty=None, 
                       specialty_type=None,
                       specialty_value=None,
                       specialty_abbrev=None,
                       signed_at=None,
                       provider_name=None, 
                       provider_institution=None, 
                       chief_complaint=None,
                       content=None):
    """
    SZ: More error checking needs to be performed in this method
    """

    if date_of_visit: date_of_visit = iso8601.parse_utc_date(date_of_visit)
    if finalized_at: finalized_at = iso8601.parse_utc_date(finalized_at)
    if signed_at: signed_at = iso8601.parse_utc_date(signed_at)

    try:
      simple_clinical_note = SimpleClinicalNote.objects.create( date_of_visit=date_of_visit, 
                                                                finalized_at = finalized_at,
                                                visit_type=visit_type, 
                                                visit_type_type=visit_type_type, 
                                                visit_type_value=visit_type_value, 
                                                visit_type_abbrev=visit_type_abbrev, 
                                                visit_location=visit_location, 
                                                specialty=specialty, 
                                                specialty_type=specialty_type,
                                                specialty_value=specialty_value,
                                                specialty_abbrev=specialty_abbrev,
                                                signed_at=signed_at,
                                                provider_name=provider_name,
                                                provider_institution=provider_institution,
                                                chief_complaint=chief_complaint,
                                                content=content)
      return simple_clinical_note
    except Exception, e:
      raise ValueError("problem processing clinical note report " + str(e))
