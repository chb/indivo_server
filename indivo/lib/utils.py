"""
Utilities for Indivo
"""

from django.http import HttpResponse
from django.template import Context, loader
from django.conf import settings
from django import http
from django.utils import simplejson
import django

try:
    from django.forms.fields import email_re
except ImportError:
    from django.core.validators import email_re

import django.core.mail as mail
import logging
import string, random
import functools

logger = logging.getLogger(__name__)

# taken from pointy-stick.com with some modifications
class MethodDispatcher(object):
    def __init__(self, method_map):
        self.methods= method_map
    
    def resolve(self, request):
        view_func = self.methods.get(request.method, None)
        return view_func
    
    @property
    def resolution_error_response(self):
        return http.HttpResponseNotAllowed(self.methods.keys())
    
    def __call__(self, request, *args, **kwargs):
        view_func = self.resolve(request)
        if view_func:
            return view_func(request, *args, **kwargs)
        return self.resolution_error_response

def is_valid_email(email):
    return True if email_re.match(email) else False

def random_string(length, choices=[string.letters]):
    # FIXME: seed!
    return "".join([random.choice(''.join(choices)) for i in xrange(length)])

def send_mail(subject, body, sender, recipient_list):
    # if send mail?
    if settings.SEND_MAIL:
        try:
            mail.send_mail(subject, body, sender, recipient_list)
        except Exception, e:
            logger.error("Exception raised when trying to send the following email: %s" % e)
            logger.error("-----\nFrom: %s\nTo: %s\nSubject: %s\n\n%s\n-----" % (sender, ', '.join(recipient_list), subject, body))
            raise e
    else:
        logger.debug("send_mail to set to false, would have sent email to %s\n\n%s" % (', '.join(recipient_list), body))

def render_template_raw(template_name, vars, type='xml'):
    t_obj = loader.get_template('%s.%s' % (template_name, type))
    c_obj = Context(vars)
    return t_obj.render(c_obj)

def render_template(template_name, vars, type='xml'):
    content = render_template_raw(template_name, vars, type)
    
    mimetype = 'text/plain'
    if type == 'xml':
        mimetype = "application/xml"
    elif type == "json":
        mimetype = 'text/json'
    return HttpResponse(content, mimetype=mimetype)


def get_element_value(dom, el):
    try:
        return dom.getElementsByTagName(el)[0].firstChild.nodeValue
    except:
        return ""

def url_interpolate(url_template, vars):
    """
    Interpolate a URL template
    TODO: security review this
    """
    
    result_url = url_template
    
    # go through the vars and replace
    for var_name in vars.keys():
        result_url = result_url.replace("{%s}" % var_name, vars[var_name])
    
    return result_url

def is_browser(request):
    """
    Determine if the request accepts text/html, in which case it's a user at a browser.
    """
    accept_header = request.META.get('HTTP_ACCEPT', False) or request.META.get('ACCEPT', False)
    if accept_header and isinstance(accept_header, str):
        return "text/html" in accept_header.split(',')
    return False

def get_content_type(request):
    content_type = None
    if request.META.has_key('CONTENT_TYPE'):
        content_type = request.META['CONTENT_TYPE']
    if not content_type and request.META.has_key('HTTP_CONTENT_TYPE'):
        content_type = request.META['HTTP_CONTENT_TYPE']
    return content_type

# some decorators to make life easier
def django_json(func):
    def func_with_json_conversion(*args, **kwargs):
        return_value = func(*args, **kwargs)
        return HttpResponse(simplejson.dumps(return_value), mimetype='application/json')
    functools.update_wrapper(func_with_json_conversion, func)
    return func_with_json_conversion

# Taken from http://code.activestate.com/
# A decorator for properties whose value should only be calculated once.
# Sample use:
# class SomeClass(object):
#
#     @LazyProperty
#     def someprop(self):
#         print 'Actually calculating value'
#         return 13
#
# To force recalculation (inadvisable):
# o = SomeClass()
# o.someprop # runs the calculation
# o.someprop # doesn't recalculate
# del o.someprop
# o.someprop # re-runs the calculation
#
# Note: DO NOT USE THIS ON PROPERTIES WHICH DEPEND ON THE VALUE OF SETTINGS!!
# If the settings change, the computed value might be incorrect.
 
class LazyProperty(object):
    def __init__(self, calculate_function):
        self._calculate = calculate_function

    def __get__(self, obj, _=None):
        if obj is None:
            return self
        value = self._calculate(obj)
        setattr(obj, self._calculate.func_name, value)
        return value

class DjangoVersionDependentExecutor(object):
    """ class which will execute different code based on Django's version.

    Syntax for a version requirement is ``{major}.{minor}.{revision}[+|-]``, 
    where the optional ``+`` and ``-`` indicate whether to include versions 
    after or before the given release, respectively.

    """

    def __init__(self, version_map, default_return_val=None):
        """ create the object.

        version_map is a dictionary of ``version_requirement:callable`` pairs.
        When called, the object will execute all callables in the 
        dictionary that corresponds to a version_requirement satisfied by the
        current Django version.

        If no such callables exist, calling the object will return
        ``default_return_val``. Otherwise, the call will return the value
        returned by the last callable to be executed. Note that, since there
        is no specified ordering on the callables, this could be the result
        of any passed callable. For this reason, it is a good idea to pass
        callables that all return values of equivalent types.
        
        """
        self.django_v = django.VERSION[0:3]
        self.ret = default_return_val
        self.funcs = []

        for version_string, func in version_map.iteritems():
            if version_string[-1] in ('+', '-'):
                direction = version_string[-1]
                version_string = version_string[:-1]

            req_v = tuple(map(int, version_string.split('.'))[0:3])

            if (req_v < self.django_v and direction == '+') \
                    or (req_v > self.django_v and direction == '-') \
                    or (req_v == self.django_v):
                self.funcs.append(func)

    def __call__(self, *args, **kwargs):
        ret_val = self.ret
        for func in self.funcs:
            ret_val = func(*args, **kwargs)
        return ret_val
