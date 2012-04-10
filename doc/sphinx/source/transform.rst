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

   As an example, here's how you might implement this for a transform from our 
   :doc:`Allergy Schema <schemas/allergy-schema>` to our :doc:`Allergy Data Model <data-models/allergy>`::

     from indivo.document_processing import BaseTransform
     from indivo.models import Allergy
     from lxml import etree

     NS = "http://indivo.org/vocab/xml/documents#"

     class Transform(BaseTransform):

         def to_facts(self, doc_etree):
             args = self._get_data(doc_etree)

   	     # Create the fact and return it
             # Note: This method must return a list
             return [Allergy(**args)]

         def _tag(self, tagname):
             return "{%s}%s"%(NS, tagname)

         def _get_data(self, doc_etree):
             """ Parse the etree and return a dict of key-value pairs for object construction. """
             ret = {}
             _t = self._tag

	     # Get the date_diagnosed
             ret['date_diagnosed'] = doc_etree.findtext(_t('dateDiagnosed'))
        
             # Get the diagnosed_by
             ret['diagnosed_by'] = doc_etree.findtext(_t('diagnosedBy'))

             # Get the allergen_type, allergen_type_type, allergen_type_value, allergen_type_abbrev
             allergen_type_node = doc_etree.find(_t('allergen')).find(_t('type'))
             ret['allergen_type'] = allergen_type_node.text
             ret['allergen_type_type'] = allergen_type_node.get('type')
             ret['allergen_type_value'] = allergen_type_node.get('value')
             ret['allergen_type_abbrev'] = allergen_type_node.get('abbrev')

             # Get the allergen_name, allergen_name_name, allergen_name_value, allergen_name_abbrev
             allergen_name_node = doc_etree.find(_t('allergen')).find(_t('name'))
             ret['allergen_name'] = allergen_name_node.text
             ret['allergen_name_type'] = allergen_name_node.get('type')
             ret['allergen_name_value'] = allergen_name_node.get('value')
             ret['allergen_name_abbrev'] = allergen_name_node.get('abbrev')

             # Get the Comments
             ret['reaction'] = doc_etree.findtext(_t('reaction'))

             # Get the Diagnosed_by
             ret['specifics'] = doc_etree.findtext(_t('specifics'))
        
             return ret

.. automethod:: indivo.document_processing.BaseTransform.to_sdmj

   As an example, here's how you might implement this for a transform from our 
   :doc:`Allergy Schema <schemas/allergy-schema>` to our :doc:`Allergy Data Model <data-models/allergy>`. Note the 
   reuse of the ``_get_data()`` function from above::

     from indivo.document_processing import BaseTransform

     SDMJ_TEMPLATE = '''
     { "__modelname__": "Allergy",
       "date_diagnosed": "%(date_diagnosed)s",
       "diagnosed_by": "%(diagnosed_by)s",
       "allergen_type": "%(allergen_type)s",
       "allergen_type_type": "%(allergen_type_type)s",
       "allergen_type_value": "%(allergen_type_value)s",
       "allergen_type_abbrev": "%(allergen_type_abbrev)s",
       "allergen_name": "%(allergen_name)s",
       "allergen_name_type": "%(allergen_name_type)s",
       "allergen_name_value": "%(allergen_name_value)s",
       "allergen_name_abbrev": "%(allergen_name_abbrev)s",
       "reaction": "%(reaction)s",
       "specifics": "%(specifics)s"
     }
     '''

     class Transform(BaseTransform):

         def to_sdmj(self, doc_etree):
             args = self._get_data(doc_etree)
             return SDMJ_TEMPLATE%args

.. automethod:: indivo.document_processing.BaseTransform.to_sdmx

   As an example, here's how you might implement this for a transform from our 
   :doc:`Allergy Schema <schemas/allergy-schema>` to our :doc:`Allergy Data Model <data-models/allergy>`. Note the 
   reuse of the ``_get_data()`` function from above::

     from indivo.document_processing import BaseTransform
     from indivo.models import Allergy
     from lxml import etree
     from StringIO import StringIO

     SDMX_TEMPLATE = '''
     <Models>
       <Model name="Allergy">
         <date_diagnosed>%(date_diagnosed)s</date_diagnosed>
      	 <diagnosed_by>%(diagnosed_by)s</diagnosed_by>
      	 <allergen_type>%(allergen_type)s</allergen_type>
      	 <allergen_type_type>%(allergen_type_type)s</allergen_type_type>
      	 <allergen_type_value>%(allergen_type_value)s</allergen_type_value>
      	 <allergen_type_abbrev>%(allergen_type_abbrev)s</allergen_type_abbrev>
      	 <allergen_name>%(allergen_name)s</allergen_name>
      	 <allergen_name_type>%(allergen_name_type)s</allergen_name_type>
      	 <allergen_name_value>%(allergen_name_value)s</allergen_name_value>
      	 <allergen_name_abbrev>%(allergen_name_abbrev)s</allergen_name_abbrev>
      	 <reaction>%(reaction)s</reaction>
      	 <specifics>%(specifics)s</specifics>
       </Model>
     </Models>
     '''

     class Transform(BaseTransform):

         def to_sdmx(self, doc_etree):
             args = self._get_data(doc_etree)
             return etree.parse(StringIO(SDMX_TEMPLATE%args))

.. _add-transform:

Adding Custom Transforms to Indivo
----------------------------------

Associating a new transform with an Indivo-supported schema is simple: 

* Write your transform, as either an XSLT or a Python module, as described above.

* Drop the file containing your transform (``transform.xslt`` or ``transform.py``: make sure to name the file 
  'transform') into the directory containing the schema. See :ref:`add-schema` for more details. 

* Make sure to restart Indivo after moving transform files around, or the changes won't take effect.
