from base import report_content_to_test_docs

hba1c = [ {'value' : '3.4', 'datetime' : '2009-01-02T12:03:10Z'},
          {'value' : '9.2', 'datetime' : '2008-01-22T17:29:59Z'},
          {'value' : '4.8', 'datetime' : '2007-11-02T12:16:38Z'},
          {'value' : '4.6', 'datetime' : '2009-04-16T03:22:24Z'},
          {'value' : '3.1', 'datetime' : '2009-09-12T12:13:43Z'},
          {'value' : '3.3', 'datetime' : '2009-01-03T11:03:23Z'},
          {'value' : '1.9', 'datetime' : '2009-08-11T02:38:32Z'},
          {'value' : '1.3', 'datetime' : '2009-01-09T12:12:20Z'},
          {'value' : '6.7', 'datetime' : '2009-03-12T02:43:39Z'},
          {'value' : '3.7', 'datetime' : '2009-02-13T02:11:17Z'}]

_TEST_MEASUREMENTS = [
    """
<HBA1C xmlns='http://indivo.org/vocab/xml/documents#' value='1.77' unit='percent' datetime='2009-07-22T01:00:00.000Z' />
""",

    """
<HBA1C xmlns='http://indivo.org/vocab/xml/documents#' value='2.13' unit='percent' datetime='2009-06-17T03:00:00.034Z' />
""",

    """
<HBA1C xmlns='http://indivo.org/vocab/xml/documents#' value='3.13' unit='percent' datetime='2009-06-17T03:00:00Z' />
""",

]

TEST_MEASUREMENTS = report_content_to_test_docs(_TEST_MEASUREMENTS)
