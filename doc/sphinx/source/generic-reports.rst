Generic Reports
================================================================================

Overview
--------------------------------------------------------------------------------

To compliment the introduction of pluggable data models, Indivo provides the 
ability to run 'generic' reports over all :doc:`data models <data-models/index>`.
These reports support the :doc:`API Query Interface <query-api>`, and provide an 
out of the box solution for reporting over core and contributed data models, 
with the possibility for :ref:`customization <response_format_customization>`.  


API Calls
--------------------------------------------------------------------------------

* :http:get:`/records/{RECORD_ID}/reports/{DATA_MODEL}/`
 
* :http:get:`/carenets/{CARENET_ID}/reports/{DATA_MODEL}/`


.. _response_formats:

Response Formats
--------------------------------------------------------------------------------

Generic reports provide two default response formats, and the ability to 
implement custom implementations for each.  Formats are specified through a 
``response_format`` query parameter, and the response's Internet media type will
match the requested value.


JSON
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``../reports/{DATA_MODEL}/?response_format=application/json``

Reports are formatted as :ref:`sdmj`


XML
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``../reports/{DATA_MODEL}/?response_format=application/xml`` OR ``../reports/{DATA_MODEL}/?response_format=text/xml`` 

Reports are formatted as :ref:`sdmx`

.. _response_format_customization:

Customization
--------------------------------------------------------------------------------

The selection of items for return in generic reports can already be customized 
by taking advantage of the functionality made available throught the 
:doc:`Query API <query-api>`. In order to customize the format in which those
items are returned, you can 
:ref:`implement custom serializers <custom-serializers>` for individual data
models.

Limitations
--------------------------------------------------------------------------------

The provided processing mechanisms for JSON and XML response formats have 
protections against recursion, which might produce undesirable output for 
certain use cases

* If data models have circular or repeated references, all repeated references 
  after the first will be excluded



 
