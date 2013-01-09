Architecture Overview
=====================

This document provides a basic overview of the Indivo X system architecture. This document should 
be read before continuing on to :doc:`Indivo Authentication <authentication>` and :doc:`the Indivo API overview <api-overview>`.

Basic Indivo Concepts
---------------------

**Indivo Record**: the complete set of medical information stored by Indivo about a single individual.

**Indivo Account**: a username/password to log into Indivo. One account may be able to access any number 
of Indivo Records, and one Indivo Record may be accessible by multiple Indivo Accounts.

**Indivo Document**: a piece of medical information stored in an Indivo Record.

Components
----------

Indivo X comprises multiple components, each running as its own web server. Small installations may choose 
to install multiple components on a single physical server. The Indivo X Server is the core of the system; 
other components, including the Indivo User Interface, can be easily substituted by custom implementations.

.. image:: /images/indivo-arch.png

Indivo X Server
^^^^^^^^^^^^^^^

For a given Indivo installation, the Indivo X server:

* stores all Indivo account information, as well as the medical records and documents,

* is responsible for authentication and authorization before granting access to Indivo data,

* exposes an API for access by administrative and user applications, and by the Indivo User Interface.

Indivo User Interface / Indivo Chrome
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Indivo User Interface, also known as the "Indivo Chrome", implements the web-based visual interface 
that an Indivo user will view and use. The branding/colors/details of the user interface are all controlled 
by the Indivo Chrome. Indivo Chrome connects to Indivo X using the standard Indivo API, including some 
specific calls accessible only to the Chrome component.

Indivo X will ship with a default implementation of the Indivo Chrome which can be customized while maintaining 
a clean interface to the Indivo X API. Customizations are encouraged for re-branding or for entirely different 
devices, e.g. iPhone.

(The term "Chrome" is often used to describe the visual portions of a web browser that are part of the web browser 
itself, and not part of the web site content, e.g. the back button. Here, with "Indivo Chrome", we mean the Indivo 
user interface that is part of the core Indivo service, not part of a user application that extends 
Indivo functionality.)

Administrative Application
^^^^^^^^^^^^^^^^^^^^^^^^^^

An Admin Application can connect to Indivo X and

* create new Indivo accounts and records

* reset of passwords

* manage ownership of records, i.e. assigning an account as the owner of a record.

An admin application cannot access medical data, it can only manage a record's metadata. An admin app is thus ideal 
for a hospital administrator, an Indivo help-desk staffer, a research administrator, etc.

User Application / Personal Health Application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A user application, or Personal Health Application, is an application that Indivo users manually add to their 
record to provide incremental functionality. Examples of PHA functionality include:

* Diabetes management

* Genomic data display

* Clinical trial matching and messaging

User applications generally provide a web interface to the Indivo user, while connecting to the user's Indivo record 
directly with the Indivo X Server. Users are fully in control of what data a user application can access. They can, 
at any time, change those permissions or remove the application entirely. Thus, an Indivo user application connects 
to Indivo in much the same way that a Facebook application connects to Facebook.

Communication Protocols
-----------------------

All communication between components is over HTTPS, with an API that abides by the REST design philosophy. 
Authentication is via oAuth.

More about :doc:`Indivo Authentication <authentication>`.

More about :doc:`the Indivo API <api-overview>`.
