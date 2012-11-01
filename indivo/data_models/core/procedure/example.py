from indivo.models import Procedure
from indivo.lib.iso8601 import parse_utc_date as date

procedure_fact = Procedure(
    date=date("2011-02-15T12:00:00Z"),
    notes="Went great!",
    name_code_title="Appendectomy",
    name_code_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    name_code_identifier="80146002",
    status_code_title="Complete",
    status_code_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    status_code_identifier="385658003",
    provider_dea_number="325555555",
    provider_npi_number="5235235",
    provider_email="joshua.mandel@fake.emailserver.com",
    provider_name_given="Josuha",
    provider_name_family="Mandel",
    provider_tel_1_type="w",
    provider_tel_1_number="1-235-555-55555",
    provider_tel_1_preferred_p=True,
    )
