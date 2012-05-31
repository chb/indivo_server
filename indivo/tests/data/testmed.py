TEST_TESTMED_JSON = '''
[
    {
        "__modelname__": "TestMed",
        "name": "med1",
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
                "date_filled": "2010-10-01T00:00:00Z",
                "supply_days": 30.0
            }, {
                "__modelname__": "TestFill",
                "date_filled": "2010-10-16T00:00:00Z",
                "supply_days": 30.0
            }
        ]
    }
]
'''
