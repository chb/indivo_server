API Query Interface
===================

When a list of results are returned, the URL ends in a ``/`` and the HTTP method 
is a ``GET``, as is typical of REST design. In that case, Indivo X supports a 
generic query string that determines paging and ordering of the results::

  ?offset={offset}&limit={limit}&order_by={order_by}&status={document_status}

* ``offset`` indicates which item number to start with, e.g. when getting a 
  second batch of items.

* ``limit`` indicates the maximum number of items to return. This is used in 
  combination with offset to accomplish paging.

* ``order_by`` is dependent on the fields returned in the list of items, and each 
  call must thus define which fields are valid. Using an invalid field in 
  order_by results in no effect on the output, as if order_by were absent.

* ``status`` can be used where applicable. It pertains to the status of documents 
  and can currently be set to one of three options: 'void', 'archived' or 'active'

For minimal (url ends in ``/reports/minimal/{report_type}/``) and 
:doc:`generic <generic-reports>` reports, we expose an expanded query interface, 
allowing for filtering, date constraints, and aggregation. Note that this interface 
only makes sense to implement for reports that function solely to retrieve 
and display fact objects. The interface will not be implemented for any more 
complex report types that deal with multiple fact objects (what would it mean for 
a CCR report to group by lab type?). Other reports will still have access to the 
Beta2-style paging operations. The interface will be available for other API calls to implement as well (i.e. the
Audit interface)

Output
------

Minimal Reports
^^^^^^^^^^^^^^^

In the previous interface, reports were templated into schemas for output as 
specified by :doc:`the Indivo Reporting Schema <schemas/reporting-schema>`. This output 
method will be preserved for queries that return sets of fact objects, but for 
queries that return aggregates or groups, we will output data according to the 
:doc:`Indivo Aggregate Report Schema <schemas/aggregate-schema>`.

Generic Reports
^^^^^^^^^^^^^^^

Non-Aggregate
	:doc:`Generic Reports <generic-reports>` provide :ref:`sdmj` or :ref:`sdmx` 
	output based on the requested response format. Please see the documentation 
	for :ref:`response formats <response_formats>` for more information.
	
Aggregate
	Also based on the requested :ref:`response format <response_formats>`

* XML

	Formatted according to the 
	:doc:`Indivo Generic Aggregate Reports Schema <schemas/aggregate-generic-schema>`
	
* JSON

	Formatted as :ref:`sdmj` with AggregateReport as the data model and without 
	a ``__documentid__``. Below is an example of retrieving the max value using
	the :ref:`date_group <query-date-operators>` operator ::
	
		[
			{
				"__modelname__": "AggregateReport",
				"group": "2009-07",
				"value": 1
			}, {
				"__modelname__": "AggregateReport",
				"group": "2009-08",
				"value": 4
			}
		]
		
Data Fields
-----------

As in ``order_by`` in the Beta2 interface, each report must expose a set of data 
fields on which they may be filtered, grouped, or ordered. These fields can be 
found :ref:`below <valid-query-fields>`.

.. _query-operators:

Query Operators
---------------

Filtering Operators
^^^^^^^^^^^^^^^^^^^

* `offset`, `limit`: Syntax is: `?offset={offset}&limit={limit}`. These operators 
  will function as previously, taking integer indexes into the result set, and 
  returning a sliced portion of the result set from indices ``offset`` to 
  ``offset + limit``.

* Custom Filters: Syntax is: ``?{field}={value[|value]...}``. Limits result sets to items 
  where the passed field is in the set of pipe delimited values. If no items have such a value in 
  the passed field, the query will return an empty result set. Field names must 
  be data fields exposed by the desired report type.

Ordering Operators
^^^^^^^^^^^^^^^^^^

* ``order_by``: Syntax is ``?order_by={field}``. Functions as previously. Takes a 
  data field exposed by the desired report type, and returns the result set 
  sorted by that field. Fields are sorted in ascending order by default, and 
  prefixing them with a '-' will reverse the order to descending. 

  **Note:** If ``order_by`` is used with a grouping, ``{field}`` may only refer 
  to the field used with ``group_by``, ``date_group``, or ``aggregate_by``.

Grouping and Aggregating Operators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Note: Calls using grouping and aggregating operators will return data according 
to the aggregation schema, not the standard query schema**

* ``group_by``: Syntax is: ``?group_by={field}``. Groups result sets by the 
  passed field, which must be a data field exposed by the desired report type. 
  **Must be used with an aggregation operator**, and will throw a 400 Bad Request 
  error otherwise. **If used with** ``order_by``, **the ordering field must be 
  identical to the grouping field or the field passed in** ``aggregate_by``.

* ``aggregate_by``: Syntax is ``?aggregate_by={operator}*{field}``. Combines 
  multiple items in a result set (or a group within a result set) into a single 
  item using the passed operator applied to the passed field (which must be a 
  data field exposed by the desired report type). See below for examples. 
  Available operators are:

  * ``sum``: returns the sum of all values of ``{field}``. Will throw a 400 Bad 
    Request error if the passed field does not contain numerical data.

  * ``avg``: returns the arithmetic mean of all values of ``{field}``. Will throw 
    a 400 Bad Request error if the passed field does not contain numerical data.

  * ``max``: returns the maximum value of all values of ``{field}``. Will throw a 
    400 Bad Request error if the passed field does not contain numerical data or 
    date/time data.

  * ``min``: returns the minimum value of all values of ``{field}``. Will throw a 
    400 Bad Request error if the passed field does not contain numerical data or 
    date/time data.

  * ``count``: returns the total number of items passed. If ``{field}`` is 
    specified, only counts rows where <tt>{field}</tt> is not empty.

.. _query-date-operators:

Date-based Operators
^^^^^^^^^^^^^^^^^^^^

* ``date_range``: Syntax is ``?date_range={field}*{start_date}*{end_date}``. A 
  filtering operation that limits result sets to items with values of ``{field}`` 
  between ``{start_date}`` and ``{end_date}`` (inclusive). If either 
  ``{start_date}`` or ``{end_date}`` is not specified, the range will be 
  open-ended. If both are unspecified, the filter will do nothing. ``{field}`` 
  must be a data field exposed by the desired report type. If ``field`` is not a 
  date/time field, a 400 Bad Request error will be raised. ``{start_date}`` and 
  ``{end_date}`` must be entered as valid UTC timestamp strings, as described in 
  :doc:`Basic Data Formats <data-formats>`. See below for examples.

* ``date_group``: Syntax is: ``?date_group={field}*{time_increment}``. A grouping 
  operator that, rather than grouping by a single field value, forms groups based 
  on common increments of time. Has same restraints of use as ``group_by`` above, 
  with the additional constraint that ``{field}`` must be a date/time data field. 

  **If used with** ``order_by``, **the ordering field must be identical to the 
  grouping field or the field passed in** ``aggregate_by``.

  **Note: using this operator will result in the return of an aggregation 
  schema.** 

  Valid increments are:
  
  * ``hour``: items are placed in the same group if they occurred within the same 
    hour.

  * ``day``: items are placed in the same group if they occurred within the same 
    day.

  * ``week``: items are placed in the same group if they occurred within the same 
    week.

  * ``month``: items are placed in the same group if they occurred within the same
    month.

  * ``year``: items are placed in the same group if they occurred within the same 
    year.

  * ``hourofday``: items are placed in the same group if they occurred during the 
    same hour of day (even on separate days).

  * ``dayofweek``: items are placed in the same group if they occurred on the same
    day of the week (even in separate weeks).

  * ``weekofyear``: items are placed in the same group if they occurred during the
    same week of the year (indexed from 1 - 52), even in separate years.

  * ``monthofyear``: items are placed in the same group if they occurred during 
    the same month of the year (indexed from 1-12), even in separate years.

Query Operator Evaluation
-------------------------
Query operators are evaluated as follows:

#. filter operators, including ``date_range`` but excluding ``limit`` and 
   ``offset``, are applied first.

#. If ``group_by`` or ``date_group`` is passed, it is evaluated next.

#. ``aggregate_by`` is evaluated next.

#. ``order_by``, ``limit`` and ``offset`` are applied.

#. The result set is templated into the standard schema or the aggregated schema 
   as appropriate and returned.

Notes on Aggregation
--------------------
Aggregation over Indivo medical data types could be very useful in certain cases 
where the data is known (by an app-developer, who generated the data, say) to be 
highly structured. For example, consider a 'Pedometer-Visualizer' app, which 
reads in data from an electric pedometer worn by a patient, stores that data as 
Indivo Measurements, and displays to the patient aggregate views of their steps 
taken (weekly/daily averages, total miles walked, etc.). This app could take full 
advantage of aggregation functions such as 'sum', 'avg', etc. However, there are 
many cases in Indivo where the data, in spite of conforming to Indivo schemas, is 
not necessarily clean enough to run these aggregations. Consider the case of lab 
test results: the schema field is by necessity a string, as not all lab results 
have numerical values. Thus, an incoming query might assume that it could ask for 
an 'average lab result value', when in fact the data wouldn't support it. We 
therefore cannot allow numerical aggregations over fields not explicitly labeled 
as 'Number' types (see :ref:`below <valid-query-fields>`). If such a case is 
necessary for the app, the appropriate design is for the app to make a 
non-aggregate query, and then process the results itself (i.e., get all lab 
result values, and then do some data cleaning to insure that only relevant data 
points are counted in the averaging).

Default Operator Values
-----------------------
If omitted, the following query operators are assigned default values:

* ``limit``: 100

* ``offset``: 0

* ``order_by``: '-created_at' (the date when the fact object was added to 
  indivo). **Only Applied to Non-aggregate Queries: no default ordering for 
  aggregate queries**

* ``status``: active

.. _valid-query-fields:

Valid Query Fields
------------------

With the new pluggable data models, valid query fields are defined by the data 
models themselves. See the :ref:`Data Models documentation <queryable-fields>` 
for a more complete explanation.

Example Queries
---------------
Below are a number of sample queries that demonstrate the power of the new 
interface.

Get all labs of type 'Hematology' within a date range
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::
  
  GET /records/{record_id}/reports/minimal/labs/?lab_type=Hematology&
  date_range=date_measured*2009-05-04T00:00:00Z*2011-03-09T00:00:00Z

Get all labs of type 'Hematology' or 'Chemistry' 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::
  
  GET /records/{record_id}/reports/minimal/labs/?lab_type=Hematology|Chemistry

.. 
  Get the average result value of all labs of type 'Hematology'
  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  ::

  GET /records/{record_id}/reports/minimal/labs/?lab_type=Hematology&
  aggregate_by=avg*first_lab_test_value 


Get the number of lab results per type over the last year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::
  
  GET /records/{record_id}/reports/minimal/labs/?group_by=lab_type&
  aggregate_by=count*lab_test_name&date_range=date_measured*2010-03-10T00:00:00Z*

Get the number of Hematology labs per month over the last year, ordered by date
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  GET /records/{record_id}/reports/minimal/labs/?lab_type=Hematology&
  date_group=date_measured*month&aggregate_by=count*lab_type&
  order_by=-date_measured&date_range=date_measured*2010-03-10T00:00:00Z*
