"""
.. module:: view.smart_container
   :synopsis: Indivo views to support SMART container-level API calls

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>

"""

from base import *
import urllib2

def smart_ontology(request):
    """Fetch the SMART ontology as RDF/XML."""

    # just fetch it from the smart server
    # TODO: cache this file and serve it statically
    url = 'http://sandbox-api.smartplatforms.org/ontology'

    ontology = urllib2.urlopen(url).read()
    return HttpResponse(ontology, mimetype="application/rdf+xml")
