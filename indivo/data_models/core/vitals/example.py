from indivo.models import Vitals
from indivo.lib.iso8601 import parse_utc_date as date

vitals_fact = Vitals(
    date_measured=date("2009-05-16T15:23:21Z"),
    name="Blood Pressure Systolic",
    name_type="http://codes.indivo.org/vitalsigns/",
    name_value="123",
    name_abbrev="BPsys",
    value="145",
    unit="millimeters of mercury",
    unit_type="http://codes.indivo.org/units/",
    unit_value="234",
    unit_abbrev="mmHg",
    site="left arm",
    position="sitting down",
    comments="Patient seemed nervous."
    )

