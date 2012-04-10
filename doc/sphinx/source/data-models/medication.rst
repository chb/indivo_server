Indivo Data Model: Medication
=============================

Model Definition
----------------

As :ref:`SDML <sdml>`:

.. include:: /../../../indivo/data_models/core/medication/model.sdml
   :literal:

**Note**: Since SDML doesn't provide for Boolean Fields, we are unable to define the *dispense_as_written* field 
properly in SDML. Our actual implementation of the Medication data model uses a Django Model Class for this reason.

As a Django Model Class:

.. include:: /../../../indivo/data_models/core/medication/model.py
   :literal:

Examples
--------

As :ref:`SDMJ <sdmj>`:

.. include:: /../../../indivo/data_models/core/medication/example.sdmj
   :literal:

As :ref:`SDMX <sdmx>`:

.. include:: /../../../indivo/data_models/core/medication/example.sdmx
   :literal:

As a :term:`Fact object <fact>`:

.. include:: /../../../indivo/data_models/core/medication/example.py
   :literal:
