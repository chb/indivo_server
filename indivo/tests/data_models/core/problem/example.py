from indivo.models import Problem
from indivo.lib.iso8601 import parse_utc_date as date

problem_fact = Problem(
    startDate=date("2009-05-16T12:00:00Z"),
    endDate=date("2009-05-16T16:00:00Z"),
    name_title="Backache (finding)",
    name_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    name_identifier="161891005",
    )
