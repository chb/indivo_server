"""
.. module:: view.smart_container
   :synopsis: Indivo views to support SMART container-level API calls

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>

"""

from base import *
import urllib2

from django.conf import settings

def smart_ontology(request):
    """Fetch the SMART ontology as RDF/XML."""

    # just fetch it from the smart server
    # TODO: cache this file and serve it statically
    url = 'http://sandbox-api.smartplatforms.org/ontology'

    ontology = urllib2.urlopen(url).read()
    return HttpResponse(ontology, mimetype="application/rdf+xml")

def smart_manifest(request):
    """SMART Container Manifest"""
    
    manifest = '''
    {{
        "smart_version": "0.5.0",
        "api_base": "{api_base}",
        "name": "SMART v0.5 Sandbox",
        "description": "{site_description}",
        "admin": "{admin}",
    
        "launch_urls": {{
            "authorize_token": "{ui_base}/oauth/authorize", 
            "exchange_token": "{api_base}/oauth/access_token", 
            "request_token": "{api_base}/oauth/request_token"
        }}, 
    
        "capabilities": {{
            "http://smartplatforms.org/terms#Allergy": {{
                "methods": [
                    "GET"
                ]
            }}, 
            "http://smartplatforms.org/terms#AppManifest": {{
                "methods": [
                    "GET"
                ]
            }},
            "http://smartplatforms.org/terms#ClinicalNote": {{
                "methods": [
                    "GET"
                ]
            }}, 
            "http://smartplatforms.org/terms#ContainerManifest": {{
                "methods": [
                    "GET"
                ]
            }},
            "http://smartplatforms.org/terms#Demographics": {{
                "methods": [
                    "GET"
                ]
            }}, 
            "http://smartplatforms.org/terms#Encounter": {{
                "methods": [
                    "GET"
                ]
            }}, 
            "http://smartplatforms.org/terms#Fulfillment": {{
                "methods": [
                    "GET"
                ]
            }}, 
            "http://smartplatforms.org/terms#Immunization": {{
                "methods": [
                    "GET"
                ]
            }}, 
            "http://smartplatforms.org/terms#LabResult": {{
                "methods": [
                    "GET"
                ]
            }}, 
            "http://smartplatforms.org/terms#Medication": {{
                "methods": [
                    "GET"
                ]
            }}, 
            "http://smartplatforms.org/terms#Ontology": {{
                "methods": [
                    "GET"
                ]
            }}, 
            "http://smartplatforms.org/terms#Problem": {{
                "methods": [
                    "GET"
                ]
            }},
            "http://smartplatforms.org/terms#Procedure": {{
                "methods": [
                    "GET"
                ]
            }}, 
            "http://smartplatforms.org/terms#SocialHistory": {{
                "methods": [
                    "GET"
                ]
            }},
            "http://smartplatforms.org/terms#VitalSignSet": {{
                "methods": [
                    "GET"
                ]
            }}
        }}
    }}'''
    
    processed_manifest = manifest.format(api_base=settings.SITE_URL_PREFIX,
                                         ui_base=settings.UI_SERVER_URL,
                                         site_description=settings.SITE_DESCRIPTION,
                                         admin=settings.EMAIL_SUPPORT_ADDRESS)
    
    return HttpResponse(processed_manifest, mimetype='application/json')
