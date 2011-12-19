Coding Systems
==============

For Indivo, and in general for a number of health applications, coding systems are used for interoperability. 
Examples include vaccine disease codes, allergy codes, procedure codes, etc. This page documents a web-based 
mechanism for documenting and publishing, in a machine-readable manner, these coding systems.

Abstract Model
--------------

Beyond the basic attributes (name, publisher, description), a coding system includes:

* a way to list all codes

* a way to look up a single code

* a way to search for codes matching a simple text query (e.g. "diab" should match "diabetes.")

A single code entry will have, at least:

* a code

* an abbreviation

* a full title

* (optionally) a description

* (optionally) relationships to other codes.

Data Representation
-------------------

JSON

RESTful Calls
-------------

The URL templates define RESTful calls to obtain a single code, and to search for a number of codes. Specifically, 
given the example above, the following URL returns a single code "123"::

  http://codes.indivo.org/systems/allergies/123

And the following URL searches the list of allergy codes for "peanut"::

  http://codes.indivo.org/systems/allergies/search?q=peanut


Sources
-------

The coding systems used in Indivo X are as follows. Individual installations need to download the coding systems on 
their own, as the licenses for these do not permit redistribution, so we cannot package them with Indivo.

Immunizations: HL7 v3
^^^^^^^^^^^^^^^^^^^^^

The easiest way to get the HL7 V3 file in vertical-bar-separated format, as required by the codingystem loader, is 
to use bioontology.org.

We specifically used the REST service at http://rest.bioontology.org/bioportal. The ontology code we used to 
download our version appears to no longer exist, so we'll look into the latest codes soon. In the meantime, 
documentation for the REST service is at http://www.bioontology.org/wiki/index.php/NCBO_REST_services

Labs: LOINC
^^^^^^^^^^^

Available at http://loinc.org

There is an encoding issue which forced us to truncate the LOINC file for now at line 43504.

Problems: SNOMED CT
^^^^^^^^^^^^^^^^^^^

Available by signing up to UMLS: https://login.nlm.nih.gov/cas/login?service=http://umlsks.nlm.nih.gov/uPortal/Login

An encoding conversion is required to get to utf8, should be doable using the iconv program on most Linux installations.

Medications: RxTerms
^^^^^^^^^^^^^^^^^^^^

Available from http://wwwcf.nlm.nih.gov/umlslicense/rxtermApp/rxTerm.cfm

Note that we may move to RxNorm instead of RxTerms.

