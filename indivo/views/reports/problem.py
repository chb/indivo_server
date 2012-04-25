"""
.. module:: views.reports.problem
   :synopsis: Indivo view implementations for the problem report.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import Problem

PROBLEM_FILTERS = {
  'name_title' : ('name_title', STRING),
  'startDate': ('startDate', DATE),
  'endDate': ('endDate', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

PROBLEM_TEMPLATE = 'reports/problem.xml'

def smart_problems(request, record):
  """ FAKE FOR TESTING: GET SMART PROBLEMS """

  # Return a static list
  return HttpResponse(RDF_PROBLEMS)

def problem_list(*args, **kwargs):
  """ List the problem data for a given record.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.problem._problem_list`.

  """

  return _problem_list(*args, **kwargs)

def carenet_problem_list(*args, **kwargs):
  """ List the problem data for a given carenet.

  For 1:1 mapping of URLs to views. Just calls
  :py:meth:`~indivo.views.reports.problem._problem_list`.

  """

  return _problem_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _problem_list(request, query_options,
                  record=None, carenet=None):
  """ List the problem objects matching the passed query parameters.
  
  See :doc:`/query-api` for a listing of valid parameters.

  Will return :http:statuscode:`200` with a list of problems on success,
  :http:statuscode:`400` if any invalid query parameters were passed.

  """

  q = FactQuery(Problem, PROBLEM_FILTERS,
                query_options,
                record, carenet)
  try:
    return q.render(PROBLEM_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))


RDF_PROBLEMS = '''
<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/9fc8b2c3-bb55-4e31-a413-522dcb7dbea8">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Problem"/>
<belongsTo xmlns="http://smartplatforms.org/terms#" rdf:resource="http://sandbox-api.smartplatforms.org/records/1540505"/>
<problemName xmlns="http://smartplatforms.org/terms#" rdf:nodeID="iDPsDPss4953"/>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss4953">
<rdf:type rdf:resource="http://smartplatforms.org/terms#CodedValue"/>
<code xmlns="http://smartplatforms.org/terms#" rdf:resource="http://www.ihtsdo.org/snomed-ct/concepts/43339004"/>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/43339004">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
<title xmlns="http://purl.org/dc/terms/">Hypokalemia</title>
<system xmlns="http://smartplatforms.org/terms#">http://www.ihtsdo.org/snomed-ct/concepts/</system>
<identifier xmlns="http://purl.org/dc/terms/">43339004</identifier>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss4953">
<title xmlns="http://purl.org/dc/terms/">Hypokalemia</title>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/9fc8b2c3-bb55-4e31-a413-522dcb7dbea8">
<startDate xmlns="http://smartplatforms.org/terms#">2005-12-30</startDate>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/43339004">
<rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/6252294e-fb11-4c21-8598-6bfb953f3edb">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Problem"/>
<belongsTo xmlns="http://smartplatforms.org/terms#" rdf:resource="http://sandbox-api.smartplatforms.org/records/1540505"/>
<problemName xmlns="http://smartplatforms.org/terms#" rdf:nodeID="iDPsDPss5305"/>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss5305">
<rdf:type rdf:resource="http://smartplatforms.org/terms#CodedValue"/>
<code xmlns="http://smartplatforms.org/terms#" rdf:resource="http://www.ihtsdo.org/snomed-ct/concepts/25374005"/>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/25374005">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
<title xmlns="http://purl.org/dc/terms/">Other and unspecified noninfectious gastroenteritis and colitis</title>
<system xmlns="http://smartplatforms.org/terms#">http://www.ihtsdo.org/snomed-ct/concepts/</system>
<identifier xmlns="http://purl.org/dc/terms/">25374005</identifier>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss5305">
<title xmlns="http://purl.org/dc/terms/">Other and unspecified noninfectious gastroenteritis and colitis</title>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/6252294e-fb11-4c21-8598-6bfb953f3edb">
<startDate xmlns="http://smartplatforms.org/terms#">2005-12-30</startDate>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/25374005">
<rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/96c08e03-92fa-4ce2-9778-a4d27ee30685">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Problem"/>
<belongsTo xmlns="http://smartplatforms.org/terms#" rdf:resource="http://sandbox-api.smartplatforms.org/records/1540505"/>
<problemName xmlns="http://smartplatforms.org/terms#" rdf:nodeID="iDPsDPss4931"/>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss4931">
<rdf:type rdf:resource="http://smartplatforms.org/terms#CodedValue"/>
<code xmlns="http://smartplatforms.org/terms#" rdf:resource="http://www.ihtsdo.org/snomed-ct/concepts/235595009"/>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/235595009">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
<title xmlns="http://purl.org/dc/terms/">Gastroesophageal reflux disease</title>
<system xmlns="http://smartplatforms.org/terms#">http://www.ihtsdo.org/snomed-ct/concepts/</system>
<identifier xmlns="http://purl.org/dc/terms/">235595009</identifier>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss4931">
<title xmlns="http://purl.org/dc/terms/">Gastroesophageal reflux disease</title>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/96c08e03-92fa-4ce2-9778-a4d27ee30685">
<startDate xmlns="http://smartplatforms.org/terms#">2005-12-30</startDate>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/235595009">
<rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/3efb1bb6-ce2d-43db-8d1b-d7b2cbf2bcda">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Problem"/>
<belongsTo xmlns="http://smartplatforms.org/terms#" rdf:resource="http://sandbox-api.smartplatforms.org/records/1540505"/>
<problemName xmlns="http://smartplatforms.org/terms#" rdf:nodeID="iDPsDPss4627"/>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss4627">
<rdf:type rdf:resource="http://smartplatforms.org/terms#CodedValue"/>
<code xmlns="http://smartplatforms.org/terms#" rdf:resource="http://www.ihtsdo.org/snomed-ct/concepts/59455009"/>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/59455009">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
<title xmlns="http://purl.org/dc/terms/">Acidosis</title>
<system xmlns="http://smartplatforms.org/terms#">http://www.ihtsdo.org/snomed-ct/concepts/</system>
<identifier xmlns="http://purl.org/dc/terms/">59455009</identifier>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss4627">
<title xmlns="http://purl.org/dc/terms/">Acidosis</title>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/3efb1bb6-ce2d-43db-8d1b-d7b2cbf2bcda">
<startDate xmlns="http://smartplatforms.org/terms#">2005-12-30</startDate>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/59455009">
<rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/c3a23bfb-c962-403b-8359-9c24ba2d50f1">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Problem"/>
<belongsTo xmlns="http://smartplatforms.org/terms#" rdf:resource="http://sandbox-api.smartplatforms.org/records/1540505"/>
<problemName xmlns="http://smartplatforms.org/terms#" rdf:nodeID="iDPsDPss5316"/>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss5316">
<rdf:type rdf:resource="http://smartplatforms.org/terms#CodedValue"/>
<code xmlns="http://smartplatforms.org/terms#" rdf:resource="http://www.ihtsdo.org/snomed-ct/concepts/44054006"/>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/44054006">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
<title xmlns="http://purl.org/dc/terms/">Diabetes mellitus type 2</title>
<system xmlns="http://smartplatforms.org/terms#">http://www.ihtsdo.org/snomed-ct/concepts/</system>
<identifier xmlns="http://purl.org/dc/terms/">44054006</identifier>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss5316">
<title xmlns="http://purl.org/dc/terms/">Diabetes mellitus type 2</title>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/c3a23bfb-c962-403b-8359-9c24ba2d50f1">
<startDate xmlns="http://smartplatforms.org/terms#">2005-03-12</startDate>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/44054006">
<rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/d16b8288-bc2b-48e3-b916-a30fd81bc5fe">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Problem"/>
<belongsTo xmlns="http://smartplatforms.org/terms#" rdf:resource="http://sandbox-api.smartplatforms.org/records/1540505"/>
<problemName xmlns="http://smartplatforms.org/terms#" rdf:nodeID="iDPsDPss5011"/>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss5011">
<rdf:type rdf:resource="http://smartplatforms.org/terms#CodedValue"/>
<code xmlns="http://smartplatforms.org/terms#" rdf:resource="http://www.ihtsdo.org/snomed-ct/concepts/34095006"/>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/34095006">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
<title xmlns="http://purl.org/dc/terms/">Dehydration</title>
<system xmlns="http://smartplatforms.org/terms#">http://www.ihtsdo.org/snomed-ct/concepts/</system>
<identifier xmlns="http://purl.org/dc/terms/">34095006</identifier>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss5011">
<title xmlns="http://purl.org/dc/terms/">Dehydration</title>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/d16b8288-bc2b-48e3-b916-a30fd81bc5fe">
<startDate xmlns="http://smartplatforms.org/terms#">2005-12-30</startDate>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/34095006">
<rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/c7521186-511d-4f7a-9fb9-75be23301dc7">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Problem"/>
<belongsTo xmlns="http://smartplatforms.org/terms#" rdf:resource="http://sandbox-api.smartplatforms.org/records/1540505"/>
<problemName xmlns="http://smartplatforms.org/terms#" rdf:nodeID="iDPsDPss5012"/>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss5012">
<rdf:type rdf:resource="http://smartplatforms.org/terms#CodedValue"/>
<code xmlns="http://smartplatforms.org/terms#" rdf:resource="http://www.ihtsdo.org/snomed-ct/concepts/25064002"/>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/25064002">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
<title xmlns="http://purl.org/dc/terms/">Headache</title>
<system xmlns="http://smartplatforms.org/terms#">http://www.ihtsdo.org/snomed-ct/concepts/</system>
<identifier xmlns="http://purl.org/dc/terms/">25064002</identifier>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss5012">
<title xmlns="http://purl.org/dc/terms/">Headache</title>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/c7521186-511d-4f7a-9fb9-75be23301dc7">
<startDate xmlns="http://smartplatforms.org/terms#">2006-04-10</startDate>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/25064002">
<rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/da4e8632-f7a6-4b20-9ba9-4b06e64c94aa">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Problem"/>
<belongsTo xmlns="http://smartplatforms.org/terms#" rdf:resource="http://sandbox-api.smartplatforms.org/records/1540505"/>
<problemName xmlns="http://smartplatforms.org/terms#" rdf:nodeID="iDPsDPss5120"/>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss5120">
<rdf:type rdf:resource="http://smartplatforms.org/terms#CodedValue"/>
<code xmlns="http://smartplatforms.org/terms#" rdf:resource="http://www.ihtsdo.org/snomed-ct/concepts/13200003"/>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/13200003">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
<title xmlns="http://purl.org/dc/terms/">Peptic ulcer without hemorrhage, without perforation AND without obstruction</title>
<system xmlns="http://smartplatforms.org/terms#">http://www.ihtsdo.org/snomed-ct/concepts/</system>
<identifier xmlns="http://purl.org/dc/terms/">13200003</identifier>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss5120">
<title xmlns="http://purl.org/dc/terms/">Peptic ulcer without hemorrhage, without perforation AND without obstruction</title>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/da4e8632-f7a6-4b20-9ba9-4b06e64c94aa">
<startDate xmlns="http://smartplatforms.org/terms#">2005-03-09</startDate>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/13200003">
<rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/aadba3b7-0c03-4238-afc6-60a3a365289b">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Problem"/>
<belongsTo xmlns="http://smartplatforms.org/terms#" rdf:resource="http://sandbox-api.smartplatforms.org/records/1540505"/>
<problemName xmlns="http://smartplatforms.org/terms#" rdf:nodeID="iDPsDPss5225"/>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss5225">
<rdf:type rdf:resource="http://smartplatforms.org/terms#CodedValue"/>
<code xmlns="http://smartplatforms.org/terms#" rdf:resource="http://www.ihtsdo.org/snomed-ct/concepts/162031009"/>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/162031009">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
<title xmlns="http://purl.org/dc/terms/">Dyspepsia and other specified disorders of function of stomach</title>
<system xmlns="http://smartplatforms.org/terms#">http://www.ihtsdo.org/snomed-ct/concepts/</system>
<identifier xmlns="http://purl.org/dc/terms/">162031009</identifier>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss5225">
<title xmlns="http://purl.org/dc/terms/">Dyspepsia and other specified disorders of function of stomach</title>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/aadba3b7-0c03-4238-afc6-60a3a365289b">
<startDate xmlns="http://smartplatforms.org/terms#">2005-03-09</startDate>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/162031009">
<rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/0f96bcf0-1861-42ab-9d52-76c7f1100830">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Problem"/>
<belongsTo xmlns="http://smartplatforms.org/terms#" rdf:resource="http://sandbox-api.smartplatforms.org/records/1540505"/>
<problemName xmlns="http://smartplatforms.org/terms#" rdf:nodeID="iDPsDPss4416"/>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss4416">
<rdf:type rdf:resource="http://smartplatforms.org/terms#CodedValue"/>
<code xmlns="http://smartplatforms.org/terms#" rdf:resource="http://www.ihtsdo.org/snomed-ct/concepts/301717006"/>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/301717006">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
<title xmlns="http://purl.org/dc/terms/">Right upper quadrant pain</title>
<system xmlns="http://smartplatforms.org/terms#">http://www.ihtsdo.org/snomed-ct/concepts/</system>
<identifier xmlns="http://purl.org/dc/terms/">301717006</identifier>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss4416">
<title xmlns="http://purl.org/dc/terms/">Right upper quadrant pain</title>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/0f96bcf0-1861-42ab-9d52-76c7f1100830">
<startDate xmlns="http://smartplatforms.org/terms#">2005-03-25</startDate>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/301717006">
<rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/4e64aaef-b07b-4880-b189-b8a45d063489">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Problem"/>
<belongsTo xmlns="http://smartplatforms.org/terms#" rdf:resource="http://sandbox-api.smartplatforms.org/records/1540505"/>
<problemName xmlns="http://smartplatforms.org/terms#" rdf:nodeID="iDPsDPss5196"/>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss5196">
<rdf:type rdf:resource="http://smartplatforms.org/terms#CodedValue"/>
<code xmlns="http://smartplatforms.org/terms#" rdf:resource="http://www.ihtsdo.org/snomed-ct/concepts/14760008"/>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/14760008">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
<title xmlns="http://purl.org/dc/terms/">Constipation</title>
<system xmlns="http://smartplatforms.org/terms#">http://www.ihtsdo.org/snomed-ct/concepts/</system>
<identifier xmlns="http://purl.org/dc/terms/">14760008</identifier>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss5196">
<title xmlns="http://purl.org/dc/terms/">Constipation</title>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/4e64aaef-b07b-4880-b189-b8a45d063489">
<startDate xmlns="http://smartplatforms.org/terms#">2005-12-30</startDate>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/14760008">
<rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/e463fd04-ed08-4ada-86f7-9ddeaa4a6a01">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Problem"/>
<belongsTo xmlns="http://smartplatforms.org/terms#" rdf:resource="http://sandbox-api.smartplatforms.org/records/1540505"/>
<problemName xmlns="http://smartplatforms.org/terms#" rdf:nodeID="iDPsDPss4707"/>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss4707">
<rdf:type rdf:resource="http://smartplatforms.org/terms#CodedValue"/>
<code xmlns="http://smartplatforms.org/terms#" rdf:resource="http://www.ihtsdo.org/snomed-ct/concepts/267432004"/>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/267432004">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
<title xmlns="http://purl.org/dc/terms/">Pure hypercholesterolemia</title>
<system xmlns="http://smartplatforms.org/terms#">http://www.ihtsdo.org/snomed-ct/concepts/</system>
<identifier xmlns="http://purl.org/dc/terms/">267432004</identifier>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss4707">
<title xmlns="http://purl.org/dc/terms/">Pure hypercholesterolemia</title>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/e463fd04-ed08-4ada-86f7-9ddeaa4a6a01">
<startDate xmlns="http://smartplatforms.org/terms#">2005-12-30</startDate>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/267432004">
<rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/d832fa1b-394f-4952-961b-890d2677b766">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Problem"/>
<belongsTo xmlns="http://smartplatforms.org/terms#" rdf:resource="http://sandbox-api.smartplatforms.org/records/1540505"/>
<problemName xmlns="http://smartplatforms.org/terms#" rdf:nodeID="iDPsDPss4988"/>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss4988">
<rdf:type rdf:resource="http://smartplatforms.org/terms#CodedValue"/>
<code xmlns="http://smartplatforms.org/terms#" rdf:resource="http://www.ihtsdo.org/snomed-ct/concepts/29857009"/>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/29857009">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
<title xmlns="http://purl.org/dc/terms/">Chest pain</title>
<system xmlns="http://smartplatforms.org/terms#">http://www.ihtsdo.org/snomed-ct/concepts/</system>
<identifier xmlns="http://purl.org/dc/terms/">29857009</identifier>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss4988">
<title xmlns="http://purl.org/dc/terms/">Chest pain</title>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/d832fa1b-394f-4952-961b-890d2677b766">
<startDate xmlns="http://smartplatforms.org/terms#">2005-11-20</startDate>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/29857009">
<rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/04f8962c-915e-4f65-a2c1-f9764f67b390">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Problem"/>
<belongsTo xmlns="http://smartplatforms.org/terms#" rdf:resource="http://sandbox-api.smartplatforms.org/records/1540505"/>
<problemName xmlns="http://smartplatforms.org/terms#" rdf:nodeID="iDPsDPss4861"/>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss4861">
<rdf:type rdf:resource="http://smartplatforms.org/terms#CodedValue"/>
<code xmlns="http://smartplatforms.org/terms#" rdf:resource="http://www.ihtsdo.org/snomed-ct/concepts/14302001"/>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/14302001">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
<title xmlns="http://purl.org/dc/terms/">Absence of menstruation</title>
<system xmlns="http://smartplatforms.org/terms#">http://www.ihtsdo.org/snomed-ct/concepts/</system>
<identifier xmlns="http://purl.org/dc/terms/">14302001</identifier>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss4861">
<title xmlns="http://purl.org/dc/terms/">Absence of menstruation</title>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/04f8962c-915e-4f65-a2c1-f9764f67b390">
<startDate xmlns="http://smartplatforms.org/terms#">2005-12-30</startDate>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/14302001">
<rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/a82fdae4-da75-4435-abae-49a5539191d4">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Problem"/>
<belongsTo xmlns="http://smartplatforms.org/terms#" rdf:resource="http://sandbox-api.smartplatforms.org/records/1540505"/>
<problemName xmlns="http://smartplatforms.org/terms#" rdf:nodeID="iDPsDPss4819"/>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss4819">
<rdf:type rdf:resource="http://smartplatforms.org/terms#CodedValue"/>
<code xmlns="http://smartplatforms.org/terms#" rdf:resource="http://www.ihtsdo.org/snomed-ct/concepts/38341003"/>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/38341003">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
<title xmlns="http://purl.org/dc/terms/">Essential hypertension</title>
<system xmlns="http://smartplatforms.org/terms#">http://www.ihtsdo.org/snomed-ct/concepts/</system>
<identifier xmlns="http://purl.org/dc/terms/">38341003</identifier>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss4819">
<title xmlns="http://purl.org/dc/terms/">Essential hypertension</title>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/a82fdae4-da75-4435-abae-49a5539191d4">
<startDate xmlns="http://smartplatforms.org/terms#">2006-04-10</startDate>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/38341003">
<rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/ef5711cb-6507-4491-9905-d8088784a785">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Problem"/>
<belongsTo xmlns="http://smartplatforms.org/terms#" rdf:resource="http://sandbox-api.smartplatforms.org/records/1540505"/>
<problemName xmlns="http://smartplatforms.org/terms#" rdf:nodeID="iDPsDPss5188"/>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss5188">
<rdf:type rdf:resource="http://smartplatforms.org/terms#CodedValue"/>
<code xmlns="http://smartplatforms.org/terms#" rdf:resource="http://www.ihtsdo.org/snomed-ct/concepts/21522001"/>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/21522001">
<rdf:type rdf:resource="http://smartplatforms.org/terms#Code"/>
<title xmlns="http://purl.org/dc/terms/">Abdominal pain</title>
<system xmlns="http://smartplatforms.org/terms#">http://www.ihtsdo.org/snomed-ct/concepts/</system>
<identifier xmlns="http://purl.org/dc/terms/">21522001</identifier>
</rdf:Description>

<rdf:Description rdf:nodeID="iDPsDPss5188">
<title xmlns="http://purl.org/dc/terms/">Abdominal pain</title>
</rdf:Description>

<rdf:Description rdf:about="http://sandbox-api.smartplatforms.org/records/1540505/problems/ef5711cb-6507-4491-9905-d8088784a785">
<startDate xmlns="http://smartplatforms.org/terms#">2005-03-12</startDate>
</rdf:Description>

<rdf:Description rdf:about="http://www.ihtsdo.org/snomed-ct/concepts/21522001">
<rdf:type rdf:resource="http://smartplatforms.org/terms/codes/SNOMED"/>
</rdf:Description>

</rdf:RDF>
'''
