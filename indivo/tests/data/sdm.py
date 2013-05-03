TEST_SDML_DOCS = ['''
{
    "__modelname__": "TestMedication2",
    "name": "String",
    "date_started": "Date",
    "date_stopped": "Date",
    "brand_name": "String", 
    "route": "String",
    "prescription": {
        "__modelname__": "TestPrescription2",
        "prescribed_by_name": "String",
        "prescribed_by_institution": "String",
        "prescribed_on": "Date",
        "prescribed_stop_on": "Date"
        },
    "fills": [{
            "__modelname__": "TestFill2",
            "date_filled": "Date",
            "supply_days": "Number",
            "filled_at_name": "String",
            "code": "CodedValue",
            "quantity": "ValueAndUnit",
            "pharmacy": "Pharmacy",
            "prescriber": "Provider"
            }]
}
''',
]

TEST_SDMJ_DOCS = ['''
{
    "__modelname__": "TestMedication2",
    "name": "ibuprofen",
    "date_started": "2010-10-01T00:00:00Z",
    "date_stopped": "2010-10-31T00:00:00Z",
    "brand_name": "Advil",
    "route": "Oral",
    "prescription": {
        "__modelname__": "TestPrescription2",
        "prescribed_by_name": "Kenneth D. Mandl",
        "prescribed_by_institution": "Children's Hospital Boston",
        "prescribed_on": "2010-09-30T00:00:00Z",
        "prescribed_stop_on": "2010-10-31T00:00:00Z"
    },
    "fills": [
        {
            "__modelname__": "TestFill2",
            "date_filled": "2010-10-01T00:00:00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        },
        {
            "__modelname__": "TestFill2",
            "date_filled": "2010-10-16T00:00:00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        }
    ]
}
''',
'''
{
    "__modelname__": "TestModelA",
    "date": "2009-05-16T12:00:00Z",
    "text": "I am a TestModelA",
    "myBs" : [
        {
            "__modelname__": "TestModelB",
            "date": "2011-05-16",
            "text": "I am TestModelB 1"
        },
        {
            "__modelname__": "TestModelB",
            "date": "2012-05-16T14:23:00Z",
            "text": "I am TestModelB 2"
        },
        {
            "__modelname__": "TestModelB",
            "date": "2012-05-16T14:23:00Z",
            "text": "I am TestModelB 3"
        }
    ],
    "myC": {
        "__modelname__": "TestModelC",
        "date": "2012-05-16",
        "text": "I am TestModelC 1"
    },
    "myDs": [
        {
            "__modelname__": "TestModelD",
            "date": "2011-05-16",
            "text": "I am TestModelD 1"
        },
        {
            "__modelname__": "TestModelD",
            "date": "2012-05-12",
            "text": "I am TestModelD 2"
        }
    ]
}
''',
]

TEST_SDMX_DOCS = ['''
<Models>
  <Model name="TestMedication2">
    <Field name="date_started">2010-10-01T00:00:00Z</Field>
    <Field name="name">ibuprofen</Field>
    <Field name="brand_name">Advil</Field>
    <Field name="date_stopped">2010-10-31T00:00:00Z</Field>
    <Field name="route">Oral</Field>
    <Field name="prescription">
      <Model name="TestPrescription2">
        <Field name="prescribed_by_name">Kenneth D. Mandl</Field>
        <Field name="prescribed_by_institution">Children's Hospital Boston</Field>
        <Field name="prescribed_on">2010-09-30T00:00:00Z</Field>
        <Field name="prescribed_stop_on">2010-10-31T00:00:00Z</Field>
      </Model>
    </Field>
    <Field name="fills">
      <Models>
        <Model name="TestFill2">
          <Field name="date_filled">2010-10-01T00:00:00Z</Field>
          <Field name="supply_days">15</Field>
          <Field name="filled_at_name">CVS</Field>
        </Model>
        <Model name="TestFill2">
          <Field name="date_filled">2010-10-16T00:00:00Z</Field>
          <Field name="supply_days">15</Field>
          <Field name="filled_at_name">CVS</Field>
        </Model>
      </Models>
    </Field>
  </Model>
</Models>
''',
'''
<Models>
  <Model name="TestModelA">
    <Field name="date">2009-05-16T12:00:00Z</Field>
    <Field name="text">I am a TestModelA</Field>
    <Field name="myBs">
      <Models>
          <Model name="TestModelB">
            <Field name="date">2011-05-16</Field>
            <Field name="text">I am TestModelB 1</Field>
          </Model>
          <Model name="TestModelB">
            <Field name="date">2012-05-16T14:23:00Z</Field>
            <Field name="text">I am TestModelB 2</Field>
          </Model>
          <Model name="TestModelB">
            <Field name="date">2012-05-16T14:23:00Z</Field>
            <Field name="text">I am TestModelB 3</Field>
          </Model>
      </Models>
    </Field>
    <Field name="myC">
        <Model name="TestModelC">
            <Field name="date">2012-05-16</Field>
            <Field name="text">I am TestModelC 1</Field>
        </Model>
    </Field>
    <Field name="myDs">
        <Models>
            <Model name="TestModelD">
                <Field name="date">2012-05-16</Field>
                <Field name="text">I am TestModelD 1</Field>
            </Model>
            <Model name="TestModelD">
                <Field name="date">2012-05-12</Field>
                <Field name="text">I am TestModelD 2</Field>
            </Model>
        </Models>
    </Field>
  </Model>
</Models>
''',
]

INVALID_TEST_SDML_DOCS = ['''
{
    "__modelname__": "TestMedication3",
    "name": "String",
    "date_started": "Boink",
    "date_stopped": "Date",
    "brand_name": "String", 
    "route": "String",
    "prescription": {
        "__modelname__": "TestPrescription3",
        "prescribed_by_name": "String",
        "prescribed_by_institution": "String",
        "prescribed_on": "Date",
        "prescribed_stop_on": "Date"
        },
    "fills": [{
            "__modelname__": "TestFill3",
            "date_filled": "Date",
            "supply_days": "Number",
            "filled_at_name": "String"
            }]
}
''',
'''
{
    "__modelname__": "TestMedication3",
    "name": "String",
    "date_started": "Date",
    "date_stopped": "Date",
    "brand_name": "String", 
    "route": "String",
    "prescription": {
        "__modelname__": "TestPrescription3",
        "prescribed_by_name": "String",
        "prescribed_by_institution": "String",
        "prescribed_on": "Date",
        "prescribed_stop_on": "Date"
        },
    "fills": [{
            "__modelname__": "TestFill3",
            "date_filled": "Date",
            "supply_days": "Number",
            "filled_at_name": "String"
            },
            {
            "__modelname__": "TestFillTooManyModels",
            "date_filled": "Date",
            "supply_days": "Number",
            "filled_at_name": "String"
            }]
}
''',
'''
{
    "name": "String",
    "date_started": "Date",
    "date_stopped": "Date",
    "brand_name": "String", 
    "route": "String",
    "EXTRA_FIELD": "String",
    "prescription": {
        "__modelname__": "TestPrescription3",
        "prescribed_by_name": "String",
        "prescribed_by_institution": "String",
        "prescribed_on": "Date",
        "prescribed_stop_on": "Date"
        },
    "fills": [{
            "__modelname__": "TestFill3",
            "date_filled": "Date",
            "supply_days": "Number",
            "filled_at_name": "String"
            }]
}
''',
]

INVALID_TEST_SDMJ_DOCS = ['''
{
    "__modelname__": "TestMedicationNonExistent",
    "name": "ibuprofen",
    "date_started": "2010-10-01T00:00:00Z",
    "date_stopped": "2010-10-31T00:00:00Z",
    "brand_name": "Advil",
    "route": "Oral",
    "prescription": {
        "__modelname__": "TestPrescription2",
        "prescribed_by_name": "Kenneth D. Mandl",
        "prescribed_by_institution": "Children's Hospital Boston",
        "prescribed_on": "2010-09-30T00:00:00Z",
        "prescribed_stop_on": "2010-10-31T00:00:00Z"
    },
    "fills": [
        {
            "__modelname__": "TestFill2",
            "date_filled": "2010-10-01T00:00:00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        },
        {
            "__modelname__": "TestFill2",
            "date_filled": "2010-10-16T00:00:00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        }
    ]
}
''',
'''
{
    "__modelname__": "TestMedication2",
    "name": "ibuprofen",
    "NON-FIELD": "somedata",
    "date_started": "2010-10-01T00:00:00Z",
    "date_stopped": "2010-10-31T00:00:00Z",
    "brand_name": "Advil",
    "route": "Oral",
    "prescription": {
        "__modelname__": "TestPrescription2",
        "prescribed_by_name": "Kenneth D. Mandl",
        "prescribed_by_institution": "Children's Hospital Boston",
        "prescribed_on": "2010-09-30T00:00:00Z",
        "prescribed_stop_on": "2010-10-31T00:00:00Z"
    },
    "fills": [
        {
            "__modelname__": "TestFill2",
            "date_filled": "2010-10-01T00:00:00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        },
        {
            "__modelname__": "TestFill2",
            "date_filled": "2010-10-16T00:00:00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        }
    ]
}
''',
'''
{
    "__modelname__": "TestMedication2",
    "name": "ibuprofen",
    "date_started": "2010-10-01T1a00:34Z",
    "date_stopped": "2010-10-31T00:00:00Z",
    "brand_name": "Advil",
    "route": "Oral",
    "prescription": {
        "__modelname__": "TestPrescription2",
        "prescribed_by_name": "Kenneth D. Mandl",
        "prescribed_by_institution": "Children's Hospital Boston",
        "prescribed_on": "2010-09-30T00:00:00Z",
        "prescribed_stop_on": "2010-10-31T00:00:00Z"
    },
    "fills": [
        {
            "__modelname__": "TestFill2",
            "date_filled": "2010-10-01T00:00:00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        },
        {
            "__modelname__": "TestFill2",
            "date_filled": "2010-10-16T00:00:00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        }
    ]
}
''',
'''
{
    "__modelname__": "TestMedication2",
    "name": "ibuprofen",
    "date_started": "2010-10-01T00:00:00Z",
    "date_stopped": "2010-10-31T00:00:00Z",
    "brand_name": "Advil",
    "route": "Oral",
    "prescription": {
        "__modelname__": "TestPrescription2",
        "prescribed_by_name": "Kenneth D. Mandl",
        "prescribed_by_institution": "Children's Hospital Boston",
        "prescribed_on": "2010-09-30T00:00:00Z",
        "prescribed_stop_on": "2010-10-31T00:00:00Z"
    },
    "fills": [
        {
            "__modelname__": "TestFill2",
            "date_filled": "2010-10-01T00:00:00Z",
            "supply_days": "notafloat15",
            "filled_at_name": "CVS"
        },
        {
            "__modelname__": "TestFill2",
            "date_filled": "2010-10-16T00:00:00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        }
    ]
}
''',
'''
{
    "__modelname__": "TestMedication2",
    "name": "ibuprofen",
    "date_started": "2010-10-01T00:00:00Z",
    "date_stopped": "2010-10-31T00:00:00Z",
    "brand_name": "Advil",
    "route": "Oral",
    "prescription": {
        "__modelname__": "TestPrescription2",
        "prescribed_by_name": "Kenneth D. Mandl",
        "prescribed_by_institution": "Children's Hospital Boston",
        "prescribed_on": "2010-09-30T00:00:00Z",
        "prescribed_stop_on": "2010-10-31T00:00:00Z"
    },
    "fills": [
        {
            "__modelname__": "TestFill2",
            "date_filled": "2010-10-01T00:00:00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        },
        {
            "date_filled": "2010-10-16T00:00:00Z",
            "supply_days": "15",
            "filled_at_name": "CVS"
        }
    ]
}
''',
]

INVALID_TEST_SDMX_DOCS = ['''
<Models>
  <Model name="TestMedicationNonExistent">
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
'''
<Models>
  <Model name="TestMedication2">
    <Field name="date_started">2010-10-01T00:00:00Z</Field>
    <Field name="NONEXISTENT">somedata</Field>
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
'''
<Models>
  <Model name="TestMedication2">
    <Field name="date_started">2010-10-01T00:00:00Zabc</Field>
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
'''
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
          <Field name="supply_days">notafloat15</Field>
          <Field name="filled_at_name">CVS</Field>
        </Model>
      </Models>
    </Field>
  </Model>
</Models>
''',
'''
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
        <Model name="TestFillNonExistent">
          <Field name="date_filled">2010-10-16T00:00:00Z</Field>
          <Field name="supply_days">15</Field>
          <Field name="filled_at_name">CVS</Field>
        </Model>
      </Models>
    </Field>
  </Model>
</Models>
''',
'''
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
        <Model>
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
