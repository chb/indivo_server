Indivo Transforms
=================

Introduction
------------

For the pipeline to be functional, data must be transformed from its original format into processed medical facts ready
to be stored in the database. Each schema in Indivo therefore defines a :term:`transform` that can be applied to any 
document that validates against the schema.

.. _transform-output-types:

Transform Outputs
-----------------

The ultimate output of the transformation step in the data pipeline is a set of :term:`Fact objects <Fact>` ready for 
storage in the database. However, technologies like XSLT are incapable of producing python objects as output. We looked
around for a simple, standard way of modeling data that would meet our needs, and came up empty (though we're open to
suggestions if you think you have the silver bullet). As a result, we've created our own language, 
:doc:`sdm`, to both define our data models and represent documents (in XML or JSON) that match them.

Thus, transforms may output data in any of the following formats:

* :ref:`Simple Data Model JSON (SDMJ) <sdmj>`
* :ref:`Simple Data Model XML (SDMX) <sdmx>`
* Python Fact objects

Outputs are validated on a per-datamodel-basis. For data model definitions and example outputs, 
see :doc:`data-models/index`.


Types of Transforms
-------------------

Indivo currently accepts Transforms in two formats:

* XSLT documents
* Python classes

This may change as Indivo begins to accept data in more, varied formats.

XSLTs
^^^^^

We won't cover XSLTs in any detail here, as their format and use is clearly outlined 
`in the specification <http://www.w3.org/TR/xslt>`_. Since XSLT is traditionally used to transform XML to XML, the
most natural output format for XSLTs is :ref:`SDMX <sdmx>`.

.. _python-transforms:

Python
^^^^^^

For those unskilled in the arts of XSLT, we also allow transforms to be defined using python. To define a
transform, simply subclass :py:class:`indivo.document_processing.BaseTransform` and define a valid transformation
method. Valid methods are:

.. automethod:: indivo.document_processing.BaseTransform.to_facts


.. automethod:: indivo.document_processing.BaseTransform.to_sdmj


.. automethod:: indivo.document_processing.BaseTransform.to_sdmx


.. _add-transform:

Adding Custom Transforms to Indivo
----------------------------------

Associating a new transform with an Indivo-supported schema is simple: 

* Write your transform, as either an XSLT or a Python module, as described above.

* Drop the file containing your transform (``transform.xslt`` or ``transform.py``: make sure to name the file 
  'transform') into the directory containing the schema. See :ref:`add-schema` for more details. 

* Make sure to restart Indivo after moving transform files around, or the changes won't take effect.
