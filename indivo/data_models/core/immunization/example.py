from indivo.models import Immunization
from indivo.lib.iso8601 import parse_utc_date as date

immunization_fact = Immunization(
  date_administered=date("2009-05-16T12:00:00Z"),
  administered_by="Children's Hospital Boston",
  vaccine_type="Hepatitis B",
  vaccine_type_type="http://codes.indivo.org/vaccines#",
  vaccine_type_value="123",
  vaccine_type_abbrev="hep-B",
  vaccine_manufacturer="Oolong Pharmaceuticals",
  vaccine_lot="AZ1234567",
  vaccine_expiration=date("2009-06-01"),
  sequence=2,
  anatomic_surface="Shoulder",
  anatomic_surface_type="http://codes.indivo.org/anatomy/surfaces#",
  anatomic_surface_value="234",
  adverse_event="Pain and rash."
  )

