Indivo Coded Values
===================

A coded value is a value taken from a coding system. It consists of a 
reference to the coding system (a URL), the code value, and the 
human-readable string. When the coding system is not used but a manual 
value is entered, the coding system and coded value are absent, leaving 
only the human-readable string.

Schema:

.. include:: /../../../schemas/doc_schemas/codes.xsd
   :literal:

* When a document comes into Indivo, its coded values may be expanded 
  (with abbreviation and element content) or not (just the code and coding system).

* We will encourage applications to provide expanded coded values, but this will not be required.

* Reports will provide abbreviations and full names for all relevant codes by looking up 
  against Indivo-stored copies of the coding systems. Documents will not be modified 
  from what the sources send us, to follow the principles of store exactly the original 
  data source (that's required because the documents might be digitally signed.)

* Reports can flag codes whose abbreviations and full names do not match the coding system 
  data (but we always show by default what the document says, we trust the source, not the 
  coding system.)

* We then need a code lookup API for viewing single documents.

* codes.indivo.org will provide an API for interpreting codes.
