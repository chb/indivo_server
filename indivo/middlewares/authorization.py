"""
Middleware (filters) for Indivo

inspired by django.contrib.auth middleware, but doing it differently
for tighter integration into email-centric users in Indivo.
"""

import re
import indivo
import logging

from time import strftime
from django.http import *
from django.core.exceptions import PermissionDenied
from django.conf import settings
from indivo.accesscontrol.access_rule import AccessRule

class Authorization(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        """ The process_view() hook allows us to examine the request before view_func is called"""
        # Special override flag
        if self.OVERRIDE:
            return None
        
        # Url exception(s)
        exc_pattern= settings.INDIVO_ACCESS_CONTROL_EXCEPTION
        if exc_pattern and re.match(exc_pattern, request.path):
            return None
        
        if hasattr(view_func, 'resolve'):
            resolved_func = view_func.resolve(request)
            if not resolved_func:
                return view_func.resolution_error_response
            else:
                view_func = resolved_func
        
        try:
            if view_func and hasattr(request, 'principal') and request.principal:
                access_rule = AccessRule.lookup(view_func)
                
                if access_rule and access_rule.check(request.principal, **view_kwargs): 
                    return None # Accept
        except:
            logging.debug('indivo.middlewares.Authorization: access_rule.check() was unsuccessful')
            raise PermissionDenied
        logging.debug('indivo.middlewares.Authorization: There is no principal')
        raise PermissionDenied
    
    @classmethod
    def override(cls):
        cls.OVERRIDE = True
    
    @classmethod
    def cancel_override(cls):
        cls.OVERRIDE = False

Authorization.OVERRIDE = False

# Mark that the authorization module has been loaded
# nothing gets served otherwise
indivo.AUTHORIZATION_MODULE_LOADED = True
