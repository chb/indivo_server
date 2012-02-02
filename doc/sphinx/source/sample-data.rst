Sample Data in Indivo
=====================

Testing out new Indivo apps is difficult at best with no patient data to run against.
That's why we've added the capability to create records with sample patient data
pre-loaded into them. There are two pathways for getting sample data into Indivo:
using the indivo_data.xml file and the reset.py script, and putting Indivo into 
Demo Mode.

Using indivo_data.xml
---------------------

The simplest way to get sample data into Indivo is to use the basic reset script.
When you're setting up ``indivo_data.xml``, just add a ``data_profile`` attribute to any
``<record>`` tags that you're creating. The default ``indivo_data.xml`` file has an
example of this already: it loads the data profile for ``patient_2`` into the
John S. Smith record.

As described :ref:`below<sample-data-dir>`, you can determine available data profiles
by looking at the subdirectories of ``settings.SAMPLE_DATA_DIR``.

Using Demo Mode
---------------

If you would like to run Indivo fully populated by sample data (as we do on our 
developer's sandbox), you can put Indivo into :dfn:`Demo Mode`. In this mode, all
newly created accounts are immediately set up with records pre-loaded with sample
data.

You can do this by configuring the following settings in ``settings.py``:

.. glossary::

   ``SAMPLE_DATA_DIR``
     The directory where sample data is located.

   ``DEMO_MODE``
     Puts Indivo into Demo Mode if set to ``True``.

   ``DEMO_PROFILES``
     A dictionary mapping record labels to data profiles to load for each new account. 
     For example, if the value of this settings were::
     
       {'John Doe':'patient_1', 
        'Robert Frost':'bob', 
	'Ted Kennedy':'patient_2',
	}

     Then for each new account, three new records would be created. The first would
     have a label of 'John Doe', and be populated by the data profile 'patient_1'. The
     second would have a label of 'Robert Frost', and be populated by the data profile
     'bob'. The third would have a label of 'Ted Kennedy', and be populated by the data
     profile 'patient_2'.

**Note:** Demo Mode autocreates records any time the API call to create an account,
:http:post:`/accounts/`, is called. This means that any records created through other
means (i.e. by a call to :http:post:`/records/`) will not be populated with data. If 
your registration UI or admin app handles record creation, this could lead to the 
existence of some records populated with sample data, and others without it.


.. _sample-data-dir:

Available Sample Data
---------------------

Any data in the directory specified by ``settings.SAMPLE_DATA_DIR`` 
(``settings.APP_HOME/sample_data`` by default) is available for loading into Indivo.
Data in ``SAMPLE_DATA_DIR`` should look like::

  profile_1/  # Data profiles. Each directory should correspond to a single patient.
  bob/        # For example, this is the data profile that can be referenced as 'bob'
    ...
  profile_n/
    Contact.xml # An optional contact document.
    Demographics.xml # An optional demographics document.

    doc_1.xml # XML Data to load goes here.
    doc_2.xml # File names MUST be prefixed with 'doc_'.
       ...
    doc_n.xml

    doc_1.pdf # Other extensions are treated as binary docs.
    doc_2.pdf # Also prefix names with 'doc_'.
       ...

Namely, the data directory should have multiple subdirectories, each representing one 
patient's data. Within a patient's directory, there might be a ``Contact.xml`` file
and/or a ``Demographics.xml`` file. There will also be any number of data files,
labeled ``doc_{NAME}.{EXTENSION}``, where ``NAME`` can be anything, and ``EXTENSION``
describes the type of data in the file.

We've provided you with a few sample patients to get started with, but you should 
feel free to add data that is useful to your specific Indivo installation.

Adding To the Available Sample Data
-----------------------------------

Adding sample data to Indivo is trivial: simply add files to 
``settings.SAMPLE_DATA_DIR``, making sure to preserve the directory structure described
:ref:`above<sample-data-dir>`. You can either:

* Add data to an existing profile, by dropping new data files into that profile's 
  directory, or

* Add a new profile, by creating a new subdirectory of ``SAMPLE_DATA_DIR``. Make sure
  to add a contact/demographics document for the new profile.
