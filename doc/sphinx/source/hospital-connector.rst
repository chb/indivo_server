Connecting Indivo to a Hospital
===============================

To connect Indivo to a hospital data feed, you need:

* A hospital that provides an appropriate interface we like to call "Point-of-Care API" 
  (we've previously called this Hospital API, but it's not just hospitals.)

* An Indivo app that reads that data feed and pushes the data into Indivo.

To help this along, we've produced:

* the Indivo app in question, which we call Indivo Hospital Connector, and

* a "Mock Hospital", effectively a fake hospital that implements the Point-of-Care API we think most 
  hospitals should provide.

Once a point of care exposes the Point of Care API, it should then be possible for any PCHR 
(Indivo, Google Health, Microsoft HealthVault) to connect to the Hospital and lead a user 
through the data-download process. Of course, this process requires "patient identity proofing", 
where the point-of-care will ensure that the person connecting is accessing their data alone.

.. image:: /images/poc-api.png

PoC API
-------

The PoC API is REST API with oAuth used to generate an access token that can then be used for long-term 
access to the Point-of-care record that needs to be integrated with a PCHR. In every oAuth transaction, 
the user must authenticate to the data source and authorize access to the connector application 
(all components are diagrammed above.) Each Point of Care can authenticate users in the way it sees fit: 
with an account, with one-time credentials, with personal questions only the right patient can answer, etc... 
this decision is orthogonal to the oAuth process and does not need to be specified for a connector app to 
function properly. The authentication process, whatever it is, should be implemented as part of the Point 
of Care's oAuth log-in-and-authorize process. In addition, each Point of Care can choose which connector 
apps it wants to enable, by providing only those approved connector apps with oAuth consumer tokens. This 
means that a Point of Care can implement the PoC API, but only allow specific PCHRs to connect, once proper 
privacy/HIPAA arrangements have been made with each. In other words, the protocols are independent of the 
policy decisions regarding which apps can connect and how users are authenticated: points of care retain 
full control at all times.

At the end of the oAuth process, a PoC is expected to return the normal oAuth parameters: ``oauth_token`` 
and ``oauth_token_secret``, and an additional parameter ``xoauth_hospital_record_id``, which identifies 
the hospital record that has been connected to the token in question. This record ID is needed to make 
the appropriate REST call to obtain data.

In the PoC API, data is provided in individual documents. The API is then really simple: an Atom feed of 
documents, and a REST call for each document. Each Point of Care can choose which data format it supports. We 
encourage Points of Care to use the :doc:`Indivo Schemas <schemas/index>`. ::

  GET /data/{hospital_record_id}/documents/
  { atom feed of documents }

  GET /data/{hospital_record_id}/documents/{document_id}
  { a single document of data, using identifiers provided in the atom feed }

Mock Hospital
-------------

The Mock Hospital software we provide implements the PoC REST API. Patient identity proofing is done using 
the patient's last name and a confirmation code. In a real-world setting, this confirmation code could be 
provided in person to the patient, or by mail. It might be preferable to ask the patient to enter more than 
just their last name, too, and to lock down access if too many incorrect confirmation codes are entered. We do 
not concern ourselves with this for now: we simply show feasibility of patient-proofing during the oAuth process.

* Download MockHospital v0.1

* Untar in ``/web/mock_hospital``

* Like Indivo, create a PostgreSQL database, preferably called mockhospital, with appropriate PG username access.

* Load the data::
  
    ./reset.sh

  This will load up data included in the ``data/`` directory, which you can edit to your preference before 
  setting up mockhospital.

  Check out ``/web/mock_hospital/hospital/dataimport.py`` to understand the XML and file structure format 
  of the ``data/`` directory

* Run the service::

    python manage.py runserver 7000



Indivo Hospital Connector
-------------------------

Indivo Hospital Connector is an Indivo app that also functions as an oAuth client to Mock Hospital (or to any 
PoC-API-compliant endpoint).

* Download Indivo Hospital Connector

* Set up in ``/web/indivo_hospital_connector``

* Check ``settings.py`` for the correct connectivity parameters to Mock Hospital and Indivo.

* Run ``./reset.sh`` to create and initialize the "connector" database and database user 

* Run the app::

    python manage.py runserver 8003


* Periodically (cron) run the following command to load docs from Mock Hospital to Indivo::

    python manage.py load_documents
