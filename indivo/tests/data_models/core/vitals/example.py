from indivo.models import Encounter, VitalSigns
from indivo.lib.iso8601 import parse_utc_date as date

encounter_fact = Encounter(
    startDate=date("2009-05-16T12:00:00Z"),
    endDate=date("2009-05-16T16:00:00Z"),
    facility_name="Wonder Hospital",
    facility_adr_country="Australia",
    facility_adr_city="WonderCity",
    facility_adr_postalcode="5555",
    facility_adr_street="111 Lake Drive", 
    provider_dea_number="325555555",
    provider_npi_number="5235235",
    provider_email="joshua.mandel@fake.emailserver.com",
    provider_name_given="Josuha",
    provider_name_family="Mandel",
    provider_tel_1_type="w",
    provider_tel_1_number="1-235-947-3452",
    provider_tel_1_preferred_p=True,
    encounterType_title="Ambulatory encounter",
    encounterType_system="http://smartplatforms.org/terms/codes/EncounterType#",
    encounterType_identifier="ambulatory",
    )
encounter_fact.save()

# NOTE: all vitals readings are OPTIONAL. You don't need
# to add all 56 fields here to create a VitalSigns object.
vitals_fact = VitalSigns(
    date=date("2009-05-16T12:00:00Z"),
    encounter=encounter_fact,

    # Blood Pressure
    bp_position_title="Sitting",
    bp_position_identifier="33586001",
    bp_position_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    bp_site_title="Right arm",
    bp_site_identifier="368209003",
    bp_site_system="http://purl.bioontology.org/ontology/SNOMEDCT/",
    bp_method_title="Auscultation",
    bp_method_identifier="auscultation",
    bp_method_system="http://smartplatforms.org/terms/codes/BloodPressureMethod#",
    bp_diastolic_unit="mm[Hg]",
    bp_diastolic_value=82,
    bp_diastolic_name_title="Intravascular diastolic",
    bp_diastolic_name_identifier="8462-4",
    bp_diastolic_name_system="http://purl.bioontology.org/ontology/LNC/",
    bp_systolic_unit="mm[Hg]",
    bp_systolic_value=132,
    bp_systolic_name_title="Intravascular systolic",
    bp_systolic_name_identifier="8480-6",
    bp_systolic_name_system="http://purl.bioontology.org/ontology/LNC/",

    # Body Mass Index
    bmi_unit="kg/m2",
    bmi_value=21.8,
    bmi_name_title="Body mass index",
    bmi_name_system="http://purl.bioontology.org/ontology/LNC/",
    bmi_name_identifier="39156-5",

    # Heart Rate
    heart_rate_unit="{beats}/min",
    heart_rate_value=70,
    heart_rate_name_title="Heart rate",
    heart_rate_name_system="http://purl.bioontology.org/ontology/LNC/",
    heart_rate_name_identifier="8867-4",

    # Height
    height_unit="m",
    height_value=1.8,
    height_name_title="Body height",
    height_name_system="http://purl.bioontology.org/ontology/LNC/",
    height_name_identifier="8302-2",

    # Oxygen Saturation
    oxygen_saturation_unit="%{HemoglobinSaturation}",
    oxygen_saturation_value=99,
    oxygen_saturation_name_title="Oxygen saturation",
    oxygen_saturation_name_system="http://purl.bioontology.org/ontology/LNC/",
    oxygen_saturation_name_identifier="2710-2",

    # Respiratory Rate
    respiratory_rate_unit="{breaths}/min",
    respiratory_rate_value=16,
    respiratory_rate_name_title="Respiration rate",
    respiratory_rate_name_system="http://purl.bioontology.org/ontology/LNC/",
    respiratory_rate_name_identifier="9279-1",

    # Temperature
    temperature_unit="Cel",
    temperature_value=37,
    temperature_name_title="Body temperature",
    temperature_name_system="http://purl.bioontology.org/ontology/LNC/",
    temperature_name_identifier="8310-5",

    # Weight
    weight_unit="kg",
    weight_value=70.8,
    weight_name_title="Body weight",
    weight_name_system="http://purl.bioontology.org/ontology/LNC/",
    weight_name_identifier="3141-9",
)
