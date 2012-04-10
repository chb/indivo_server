from indivo.models import Problem
from indivo.lib.iso8601 import parse_utc_date as date

problem_fact = Problem(
    date_onset=date("2009-05-16T12:00:00Z"),
    date_resolution=date("2009-05-16T16:00:00Z"),
    name="Myocardial Infarction",
    name_type="http://codes.indivo.org/problems/",
    name_value="123",
    name_abbrev="MI",
    comments="Mild Heart Attack",
    diagnosed_by="Dr. Mandl"
    )
