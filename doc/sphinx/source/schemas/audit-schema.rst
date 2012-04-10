Indivo Audit Log Schema
=======================

As of Beta 3, the logs will be returned as Indivo Reports according to the :doc:`Indivo Reporting Schema <reporting-schema>`. 
Each report item will be of type ``<AuditEntry>``, as defined below:

.. include:: /../../../indivo/schemas/metadata/auditlog/auditlog.xsd
   :literal:

Example:

.. include:: /../../../indivo/schemas/metadata/auditlog/auditlog.xml
   :literal:
