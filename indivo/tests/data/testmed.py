TEST_TESTMED_JSON = '''
[
    {
        "__modelname__": "TestMed",
        "name": "ibuprofen",
        "brand_name": "Advil",
        "frequency": 2.0,
        "date_started": "2010-10-01T00:00:00Z",
        "prescription": {
            "__modelname__": "TestPrescription",
            "prescribed_by_name": "Kenneth D. Mandl",
            "prescribed_on": "2010-09-30T00:00:00Z"
        },
        "fills": [
            {
                "__modelname__": "TestFill",
                "dateFilled": "2010-10-01T00:00:00Z",
                "supplyDays": "15"
            }, {
                "__modelname__": "TestFill",
                "dateFilled": "2010-10-16T00:00:00Z",
                "supplyDays": "15"
            }
        ]
    }
]
'''

TEST_TESTMED_XML = '''
<Models>
  <Model name="TestMed">
    <Field name="date_started">2010-10-01T00:00:00Z</Field>
    <Field name="name">ibuprofen</Field>
    <Field name="brand_name">Advil</Field>
    <Field name="frequency">2</Field>
    <Field name="prescription">
      <Model name="TestPrescription">
        <Field name="prescribed_by_name">Kenneth D. Mandl</Field>
        <Field name="prescribed_on">2010-09-30T00:00:00Z</Field>
      </Model>
    </Field>
    <Field name="fills">
      <Models>
        <Model name="TestFill">
          <Field name="date_filled">2010-10-01T00:00:00Z</Field>
          <Field name="supply_days">15</Field>
        </Model>
        <Model name="TestFill">
          <Field name="date_filled">2010-10-16T00:00:00Z</Field>
          <Field name="supply_days">15</Field>
        </Model>
      </Models>
    </Field>
  </Model>
</Models>
'''