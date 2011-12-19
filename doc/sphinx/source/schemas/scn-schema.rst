Indivo Document Schema: Simple Clinical Note
============================================

A full clinical note needs to contain a number of coded problems, etc. 
Some hospital systems do not have fully normalized clinical notes, in 
which case they can use this schema to store some simple attributes and 
the main free-form text of the note.

See also :doc:`codes-schema` and :doc:`provider-schema`.

Schema:

.. include:: /../../../schemas/doc_schemas/simplenote.xsd
   :literal:

Example:

.. include:: /../../../schemas/doc_schemas/simplenote.xml
   :literal:
