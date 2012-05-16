from indivo.models import Procedure
from indivo.lib.iso8601 import parse_utc_date as date

procedure_fact = Procedure(
    date_performed=date("2009-05-16T12:00:00"),
    name="Appendectomy",
    name_type="http://codes.indivo.org/procedures#",
    name_value="123",
    name_abbrev="append",
    provider_name="Kenneth Mandl",
    provider_institution="Children's Hospital Boston",
    location="300 Longwood Ave, Boston MA 02115",
    comments="Went great!"
    )



