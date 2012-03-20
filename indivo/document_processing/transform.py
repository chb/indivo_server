from indivo.lib.simpledatamodel import SDMXData, SDMJData
from lxml import etree

class BaseTransform(object):
    """ Base class for python transforms.

    All transforms (classes that take an etree representing a document
    and output processed data in a different form) should derive from
    this class. 
    
    Subclasses should implement any number of to_* methods. When 
    called (like a function), BaseTransform will find and evaluate the
    first valid transformation method it finds (with no promises about
    ordering).
    
    """
    
    def __init__(self):
        pass # Nothing to do yet

    @classmethod
    def from_transformation_func(cls, transform_func, override_method):
        """ Get a BaseTransform object with a transformation method already overridden. """
        ret = cls()
        setattr(ret, override_method, transform_func)
        return ret

    def to_facts(self, doc_etree):
        """ Transform an etree into a list of Indivo Fact objects.

        Subclasses should implement this method, which takes an
        ``lxml.etree._ElementTree`` (the result of calling ``etree.parse()``),
        and returns a list of ``indivo.models.Fact`` subclasses.

        """

        raise NotImplementedError

    def to_sdmj(self, doc_etree):
        """ Transform an etree into a string of valid Simple Data Model JSON.

        Subclasses should implement this method, which takes an
        ``lxml.etree._ElementTree`` (the result of calling ``etree.parse()``),
        and returns a string in valid SDMJ format.

        """

        raise NotImplementedError

    def to_sdmx(self, doc_etree):
        """ Transform an etree into a string of valid Simple Data Model XML.

        Subclasses should implement this method, which takes an
        ``lxml.etree._ElementTree`` (the result of calling ``etree.parse()``),
        and returns another ``lxml.etree._ElementTree`` instance representing 
        an XML document in valid SDMX format.

        """

        raise NotImplementedError


    def __call__(self, doc_etree):
        
        # Look for a valid method, then call it
        
        # Try conversion to facts first
        ret = self._call_func('to_facts', doc_etree)
        if ret:
            return ret

        # Try conversion to SDMJ
        ret = self._call_func('to_sdmj', doc_etree)
        if ret and isinstance(ret, str):
            return self._sdmj_to_facts(ret)

        # Try conversion to SDMX
        ret = self._call_func('to_sdmx', doc_etree)
        if ret and isinstance(ret, etree._ElementTree):
            return self._sdmx_to_facts(ret)

        # Give up
        return None

    def _call_func(self, funcname, *args, **kwargs):
        func = getattr(self, funcname, None)
        if func:
            try:
                return func(*args, **kwargs)
            except NotImplementedError:
                return None


    def _sdmx_to_facts(self, sdmx_etree):
        """ Transform Simple Data Model XML to Indivo Facts.
        
        Takes an ``lxml.etree._ElementTree`` instance, and returns a list of
        ``indivo.model.Fact`` subclasses.

        """

        parser = SDMXData(sdmx_etree)
        return [instance for instance in parser.get_output()]


    def _sdmj_to_facts(self, sdmj_string):
        """ Transform Simple Data Model JSON to Indivo Facts.
        
        Takes a string of valid SDMJ and returns a list of
        ``indivo.model.Fact`` subclasses.

        """

        parser = SDMJData(sdmj_string)
        return [instance for instance in parser.get_output()]
