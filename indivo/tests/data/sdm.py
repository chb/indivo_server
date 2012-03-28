TEST_SDMJ_SCHEMAS = ['''
{
    "__modelname__": "TestMedication",
    "name": "String",
    "date_started": "Date",
    "date_stopped": "Date",
    "brand_name": "String", 
    "route": "String",
    "prescription": {
        "__modelname__": "TestPrescription",
        "prescribed_by_name": "String",
        "prescribed_by_institution": "String",
        "prescribed_on": "Date",
        "prescribed_stop_on": "Date"
        },
    "fills": [{
            "__modelname__": "TestFill",
            "date_filled": "Date",
            "supply_days": "Number",
            "filled_at_name": "String"
            }]
}
''',
]

TEST_SDMJ_DOCS = ['''
{
    "__modelname__": "TestMedication",
    "name": "ibuprofen",
    "date_started": "2010-10-01T00:00:00Z",
    "date_stopped": "2010-10-31T00:00:00Z",
    "brand_name": "Advil",
    "route": "Oral",
    "prescription": {
        "__modelname__": "TestPrescription",
        "prescribed_by_name": "Kenneth D. Mandl",
        "prescribed_by_institution": "Children's Hospital Boston",
        "prescribed_on": "2010-09-30T00:00:00Z",
        "prescribed_stop_on": "2010-10-31T00:00:00Z"
    },
    "fills": [
        {
            "__modelname__": "TestFill",
            "date_filled": "2010-10-01T00:00:00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        },
        {
            "__modelname__": "TestFill",
            "date_filled": "2010-10-16T00:00:00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        }
    ]
}
''',
]

TEST_SDMX_DOCS = ['''
<Models>
  <Model name="TestMedication">
    <Field name="date_started">2010-10-01T00:00:00Z</Field>
    <Field name="name">ibuprofen</Field>
    <Field name="brand_name">Advil</Field>
    <Field name="date_stopped">2010-10-31T00:00:00Z</Field>
    <Field name="route">Oral</Field>
    <Field name="prescription">
      <Model name="TestPrescription">
        <Field name="prescribed_by_name">Kenneth D. Mandl</Field>
        <Field name="prescribed_by_institution">Children's Hospital Boston</Field>
        <Field name="prescribed_on">2010-09-30T00:00:00Z</Field>
        <Field name="prescribed_stop_on">2010-10-31T00:00:00Z</Field>
      </Model>
    </Field>
    <Field name="fills">
      <Models>
        <Model name="TestFill">
          <Field name="date_filled">2010-10-01T00:00:00Z</Field>
          <Field name="supply_days">15</Field>
          <Field name="filled_at_name">CVS</Field>
        </Model>
        <Model name="TestFill">
          <Field name="date_filled">2010-10-16T00:00:00Z</Field>
          <Field name="supply_days">15</Field>
          <Field name="filled_at_name">CVS</Field>
        </Model>
      </Models>
    </Field>
  </Model>
</Models>
''',
]
