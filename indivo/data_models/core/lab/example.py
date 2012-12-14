from indivo.models import LabResult
from indivo.lib.iso8601 import parse_utc_date as date

lab_fact = LabResult(
    date=date("2009-05-16T12:00:00Z"),
    
    abnormal_interpretation_code_title="Normal",
    abnormal_interpretation_code_system="http://smartplatforms.org/terms/codes/LabResultInterpretation#",
    abnormal_interpretation_code_identifier="normal",

    accession_number="AC09205823577",

    name_title="Serum Sodium",
    name_code_title="Serum Sodium",
    name_code_system="http://purl.bioontology.org/ontology/LNC/",
    name_code_identifier="2951-2",

    status_code_title="Final results: complete and verified",
    status_code_system="http://smartplatforms.org/terms/codes/LabStatus#",
    status_code_identifier="final",

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
    quantitative_result_value_unit="mEq/L"
    )

