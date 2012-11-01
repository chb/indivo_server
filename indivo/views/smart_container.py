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

def smart_capabilities(request):
    """SMART Capabilities"""
    capabilites = '''{
    "http://smartplatforms.org/terms#Alert": {
        "methods": [
            "POST"
        ]
    }, 
    "http://smartplatforms.org/terms#Allergy": {
        "methods": [
            "GET"
        ]
    }, 
    "http://smartplatforms.org/terms#AppManifest": {
        "methods": [
            "GET"
        ]
    }, 
    "http://smartplatforms.org/terms#Capabilities": {
        "methods": [
            "GET"
        ]
    }, 
    "http://smartplatforms.org/terms#Demographics": {
        "methods": [
            "GET"
        ]
    }, 
    "http://smartplatforms.org/terms#Encounter": {
        "methods": [
            "GET"
        ]
    }, 
    "http://smartplatforms.org/terms#Fulfillment": {
        "methods": [
            "GET"
        ]
    }, 
    "http://smartplatforms.org/terms#Immunization": {
        "methods": [
            "GET"
        ]
    }, 
    "http://smartplatforms.org/terms#LabResult": {
        "methods": [
            "GET"
        ]
    }, 
    "http://smartplatforms.org/terms#Medication": {
        "methods": [
            "GET"
        ]
    }, 
    "http://smartplatforms.org/terms#Ontology": {
        "methods": [
            "GET"
        ]
    }, 
    "http://smartplatforms.org/terms#Problem": {
        "methods": [
            "GET"
        ]
    }, 
    "http://smartplatforms.org/terms#User": {
        "methods": [
            "GET"
        ]
    }, 
    "http://smartplatforms.org/terms#UserPreferences": {
        "methods": [
            "DELETE", 
            "GET", 
            "PUT"
        ]
    }, 
    "http://smartplatforms.org/terms#VitalSignSet": {
        "methods": [
            "GET"
        ]
    }
}'''
    return HttpResponse(capabilites, mimetype='application/json')