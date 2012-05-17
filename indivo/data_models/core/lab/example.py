from indivo.models import LabResult
from indivo.lib.iso8601 import parse_utc_date as date

lab_fact = LabResult(
    abnormal_interpretation_title="Normal",
    abnormal_interpretation_system="http://smartplatforms.org/terms/codes/LabResultInterpretation#",
    abnormal_interpretation_identifier="normal",

    accession_number="AC09205823577",

    test_name_title="Serum Sodium",
    test_name_system="http://purl.bioontology.org/ontology/LNC/",
    test_name_identifier="2951-2",

    status_title="Final results: complete and verified",
    status_system="http://smartplatforms.org/terms/codes/LabStatus#",
    status_identifier="final",

    notes="Blood sample appears to have hemolyzed",

    quantitative_result_non_critical_range_max_value="155",
    quantitative_result_non_critical_range_max_unit="mEq/L",
    quantitative_result_non_critical_range_min_value="120",
    quantitative_result_non_critical_range_min_unit="mEq/L",

    quantitative_result_normal_range_max_value="145",
    quantitative_result_normal_range_max_unit="mEq/L",
    quantitative_result_normal_range_min_value="135",
    quantitative_result_normal_range_min_unit="mEq/L",

    quantitative_result_value_value="140", 
    quantitative_result_value_unit="mEq/L",

    collected_at=date("2010-12-27T17:00:00Z"), 

    collected_by_org_name="City Lab",
    collected_by_org_adr_country="USA",
    collected_by_org_adr_city="Springfield",
    collected_by_org_adr_postalcode="11111",
    collected_by_org_adr_region="MA",
    collected_by_org_adr_street="20 Elm St",

    collected_by_name_family="Finnialispi",
    collected_by_name_given="Tad",

    collected_by_role="Lab Specialist",
    )

