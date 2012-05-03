from django.db import models

class DummyField(models.Field):
    """ A field that should be replaced by other fields.
    
    *replacements* should be a mapping from field_suffix to (fieldclass, field_kwargs).
    This instructs the datamodel loader to remove this field, and for each entry in the mapping,
    to add a new field with the original name concatenated with field_suffix, which is an instance
    of class fieldclass instantiated with field_kwargs.

    Eventually, when Django supports fields mapping to multiple database columns, these
    fields should actually manage multiple DB columns, but for now we're just using strict substitution.
    
    """
    replacements = {}

class CodedValueField(DummyField):
    """ A field for representing coded data elements.

    Creating a CodedValueField named 'value', for example, will (under the hood) create thee fields:
    
    * ``value_identifier``, the system-specific identifier that represents the element (i.e. an RXNorm CUI)
    * ``value_title``, the human-readable title of the element
    * ``value_system``, the coding system used to represent the element

    When describing instances of your model (either when defining a
    :ref:`transform output <transform-output-types>` or when referencing fields using 
    :ref:`the Indivo Query API <queryable-fields>`), you must refer to these field names, not the original
    ``value`` field name.

    """

    replacements = {
        '_identifier': (models.CharField, {'max_length':255, 'null':True}),
        '_title': (models.CharField, {'max_length':255, 'null':True}),
        '_system': (models.CharField, {'max_length':255, 'null':True}),
        }
    
class ValueAndUnitField(DummyField):
    """ A field for representing data elements with both a value and a unit. 

    Creating a ValueAndUnitField named 'frequency', for example, will (under the hood) create the fields:
    
    * ``frequency_value``, the value of the element
    * ``frequency_unit``, the units in which the value is measured

    When describing instances of your model (either when defining a
    :ref:`transform output <transform-output-types>` or when referencing fields using 
    :ref:`the Indivo Query API <queryable-fields>`), you must refer to these field names, not the original
    ``frequency`` field name.

    """
    
    replacements = {
        '_value': (models.CharField, {'max_length':255, 'null':True}), # consider making this a float?
        '_unit': (models.CharField, {'max_length':255, 'null':True}),
        }

class AddressField(DummyField):
    """ A field for representing a physical address.

    Creating an AddressField named 'address', for example, will (under the hood) create the fields:
    
    * ``address_country``, the country in which the address is located
    * ``address_city``, the city in which the address is located
    * ``address_postalcode``, the postalcode of the address
    * ``address_region``, the region (state, in the US) in which the address is located
    * ``address_street``, the street address (including street number, apartment number, etc.) at which the address
      is located

    When describing instances of your model (either when defining a
    :ref:`transform output <transform-output-types>` or when referencing fields using 
    :ref:`the Indivo Query API <queryable-fields>`), you must refer to these field names, not the original
    ``address`` field name.

    """
    
    replacements = {
        '_country': (models.CharField, {'max_length':255, 'null':True}),
        '_city': (models.CharField, {'max_length':255, 'null':True}),
        '_postalcode': (models.CharField, {'max_length':12, 'null':True}),
        '_region': (models.CharField, {'max_length':255, 'null':True}),
        '_street': (models.CharField, {'max_length':255, 'null':True}),
        }


class PharmacyField(DummyField):
    """ A field for representing a pharmacy.

    Creating a PharmacyField named 'pharmacy', for example, will (under the hood) create three fields:
    
    * ``pharmacy_ncpdpid``, the pharmacy's National Council for Prescription Drug Programs (NCPDP) ID number
    * ``pharmacy_adr``, the address at which the pharmacy is located (an :py:class:`~indivo.fields.AddressField`)
    * ``pharmacy_org``, the name of the organization that owns the pharmacy

    When describing instances of your model (either when defining a
    :ref:`transform output <transform-output-types>` or when referencing fields using 
    :ref:`the Indivo Query API <queryable-fields>`), you must refer to these field names, not the original
    ``pharmacy`` field name.

    """
    
    replacements = {
        '_ncpdpid': (models.CharField, {'max_length':255, 'null':True}),
        '_org': (models.CharField, {'max_length':255, 'null':True}),
        '_adr': (AddressField, {}),
        }

class NameField(DummyField):
    """ A field for representing a person's name.
    
    Creating a NameField named 'name', for example, will (under the hood) create the fields:

    * ``name_family``, the family (last) name of the person
    * ``name_given``, the given (first) name of the person
    * ``name_prefix``, the prefix (i.e. 'Mr.', 'Sir', etc.) for the person's name
    * ``name_suffix``, the suffix (i.e. 'Jr.', 'Ph.D.', etc.) for the person's name

    When describing instances of your model (either when defining a
    :ref:`transform output <transform-output-types>` or when referencing fields using 
    :ref:`the Indivo Query API <queryable-fields>`), you must refer to these field names, not the original
    ``name`` field name.

    """
    
    replacements = {
        '_family': (models.CharField, {'max_length':255, 'null':True}),
        '_given': (models.CharField, {'max_length':255, 'null':True}),
        '_prefix': (models.CharField, {'max_length':255, 'null':True}),
        '_suffix': (models.CharField, {'max_length':255, 'null':True}),
        }

class TelephoneField(DummyField):
    """ A field for representing a telephone number.

    Creating a TelephoneField named 'phone', for example, will (under the hood) create the fields:

    * ``phone_type``, The type of the phone number, limited to ``h`` (home), ``w`` (work), or ``c`` (cell)
    * ``phone_number``, The actual phone number
    * ``phone_preferred_p``, Whether or not this number is a preferred method of contact (``True`` or ``False``)

    When describing instances of your model (either when defining a
    :ref:`transform output <transform-output-types>` or when referencing fields using 
    :ref:`the Indivo Query API <queryable-fields>`), you must refer to these field names, not the original
    ``phone`` field name.

    """

    phone_number_type_choices = ( ('h', 'Home'), ('w', 'Work'), ('c', 'Cell'), )

    replacements = {
        '_type': (models.CharField, {'max_length':1, 'null':True, 'choices':phone_number_type_choices}),
        '_number': (models.CharField, {'max_length':20, 'null':True}),
        '_preferred_p': (models.BooleanField, {'default':False}),
        }

class ProviderField(DummyField):
    """ A field for representing a medical provider. 

    Creating a ProviderField named 'doc', for example, will (under the hood) create the fields:

    * ``doc_dea_number``, the provider's Drug Enforcement Agency (DEA) number
    * ``doc_ethnicity``, the provider's ethnicity
    * ``doc_npi_number``, the provider's National Provider Identification (NPI) number
    * ``doc_preferred_language``, the provider's preferred language
    * ``doc_race``, the provider's race
    * ``doc_adr``, the provider's address (an :py:class:`~indivo.fields.AddressField`)
    * ``doc_bday``, the provider's birth date
    * ``doc_email``, the provider's email address
    * ``doc_name``, the provider's name (a :py:class:`~indivo.fields.NameField`)
    * ``doc_tel_1``, the provider's primary phone number (a :py:class:`~indivo.fields.TelephoneField`)
    * ``doc_tel_2``, the provider's secondary phone number (a :py:class:`~indivo.fields.TelephoneField`)
    * ``doc_gender``,  the provider's gender, limited to ``m`` (male) or ``f`` (female)

    When describing instances of your model (either when defining a
    :ref:`transform output <transform-output-types>` or when referencing fields using 
    :ref:`the Indivo Query API <queryable-fields>`), you must refer to these field names, not the original
    ``doc`` field name.

    """
    
    gender_choices = ( ('m', 'male'), ('f', 'female'), )
    
    replacements = {
        '_dea_number': (models.CharField, {'max_length':255, 'null':True}),
        '_ethnicity': (models.CharField, {'max_length':255, 'null':True}),
        '_npi_number': (models.CharField, {'max_length':255, 'null':True}),
        '_preferred_language': (models.CharField, {'max_length':255, 'null':True}),
        '_race': (models.CharField, {'max_length':255, 'null':True}),
        '_adr': (AddressField, {}),
        '_bday': (models.DateField, {'null':True}),
        '_email': (models.EmailField, {'max_length':255, 'null':True}),
        '_name': (NameField, {'max_length':255, 'null':True}),
        '_tel_1': (TelephoneField, {'max_length':255, 'null':True}),
        '_tel_2': (TelephoneField, {'max_length':255, 'null':True}),
        '_gender': (models.CharField, {'max_length':255, 'null':True, 'choices':gender_choices}),
        }
    
