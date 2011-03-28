from indivo.lib import iso8601
from indivo.models import Medication

XML = 'xml'
DOM = 'dom'

class IDP_Medication:

  def post_data(self, date_started=None,
                      date_stopped=None,
                      name=None,
                      name_type=None,
                      name_value=None,
                      name_abbrev=None,
                      brand_name=None,
                      brand_name_type=None,
                      brand_name_value=None,
                      brand_name_abbrev=None,
                      dose_unit=None,
                      dose_textvalue=None,
                      dose_value=None,
                      dose_unit_type=None, 
                      dose_unit_value=None,
                      dose_unit_abbrev=None,
                      route=None,
                      route_type=None,
                      route_value=None,
                      route_abbrev=None,
                      strength_value=None,
                      strength_textvalue=None,
                      strength_unit=None,
                      strength_unit_type=None,
                      strength_unit_value=None,
                      strength_unit_abbrev=None,
                      frequency=None,
                      frequency_type=None,
                      frequency_value=None,
                      frequency_abbrev=None,
                      prescribed_by_name=None,
                      prescribed_by_institution=None,
                      prescribed_on=None,
                      prescribed_stop_on=None,
                      dispense_as_written=None,
                      prescription_duration=None,
                      prescription_refill_info=None,
                      prescription_instructions=None):

    """
    SZ: More error checking needs to be performed in this method
    """

    try:
      if date_started:
        date_started = iso8601.parse_utc_date(date_started)
      if date_stopped:
        date_stopped = iso8601.parse_utc_date(date_stopped)

      medication_obj = Medication.objects.create( date_started= date_started,
                                                  date_stopped= date_stopped,
                                                  name=name,
                                                  name_type=name_type,
                                                  name_value=name_value,
                                                  name_abbrev=name_abbrev,
                                                  brand_name=brand_name,
                                                  brand_name_type=brand_name_type,
                                                  brand_name_value=brand_name_value,
                                                  brand_name_abbrev=brand_name_abbrev,
                                                  dose_value=dose_value,
                                                  dose_textvalue=dose_textvalue,
                                                  dose_unit=dose_unit,
                                                  dose_unit_type=dose_unit_type,
                                                  dose_unit_value=dose_unit_value,
                                                  dose_unit_abbrev=dose_unit_abbrev,
                                                  route=route,
                                                  route_type=route_type,
                                                  route_value=route_value,
                                                  route_abbrev=route_abbrev,
                                                  strength_value=strength_value,
                                                  strength_textvalue=strength_textvalue,
                                                  strength_unit=strength_unit,
                                                  strength_unit_type=strength_unit_type,
                                                  strength_unit_value=strength_unit_value,
                                                  strength_unit_abbrev=strength_unit_abbrev,
                                                  frequency=frequency,
                                                  frequency_type=frequency_type,
                                                  frequency_value=frequency_value,
                                                  frequency_abbrev=frequency_abbrev,
                                                  prescribed_by_name=prescribed_by_name,
                                                  prescribed_by_institution=prescribed_by_institution,
                                                  prescribed_on=prescribed_on,
                                                  prescribed_stop_on=prescribed_stop_on,
                                                  dispense_as_written=dispense_as_written,
                                                  prescription_duration=prescription_duration,
                                                  prescription_refill_info=prescription_refill_info,
                                                  prescription_instructions=prescription_instructions)

      return medication_obj
    except Exception, e:
      raise ValueError("problem processing medication report " + str(e))
