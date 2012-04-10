Indivo Document Schema: Problem
===============================

A problem models either a condition (e.g. asthma), or an event 
(e.g. a heart attack). We initially considered modeling them 
separately. However, they are effectively identical in their 
data fields, and they can be differentiated by their code and 
duration. Thus, like Indivo 3, we use the same model.

See the schema for :doc:`codes-schema`.

Schema:

.. include:: /../../../indivo/schemas/data/core/problem/schema.xsd
   :literal:

Example:

.. include:: /../../../indivo/schemas/data/core/problem/problem.xml
   :literal:
