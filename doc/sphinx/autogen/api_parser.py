"""
Pull relevant info from the indivo_server codebase to generate a framework for Indivo documentation
"""

# Add indivo_server to the sys path so that our script can find the codebase
# and Django can find settings.py
import sys, os
os.chdir('../..')
sys.path.append(os.getcwd())
sys.path.append("%s/.."%os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.conf import settings
from operator import attrgetter

from indivo.accesscontrol.access_rule import AccessRule
import indivo
import re

API_ROOTDIR = 'indivo_server'
API_FP = 'doc/sphinx/autogen/api-skeleton'
API_EXT = '.py'
API_REFERENCE_FP = 'doc/sphinx/source/api-reference'
API_REFERENCE_EXT = '.rst'
API_CALLS_DICT = 'CALLS'

class APIDict(object):
    ''' 
    A dictionary for holding Indivo API calls. If specified,
    auto-loads the calls from a python file. 
    '''

    api_rootdir = API_ROOTDIR
    api_fp = API_FP
    api_ext = API_EXT
    api_ref_fp = API_REFERENCE_FP
    api_ref_ext = API_REFERENCE_EXT
    calls_dict = API_CALLS_DICT

    def __init__(self, read_file=True):
        self.apicache = {}
        self.dirty = False
        if read_file:
            self._read_api()

    def is_empty(self):
        return not self.apicache

    def _read_api(self):
        '''
        Reads in the calls from the API file.
        '''
        calls = {}
        try:
            importstr = ("%s/%s"%(self.api_rootdir, self.api_fp)).replace('/', '.')
            api = __import__(importstr, fromlist=[self.calls_dict])
            calls = getattr(api, self.calls_dict)
        except ImportError: # file doesn't exist yet
            pass
        except AttributeError: # file doesn't have the calls_dict variable, must be bad formatting
            raise ValueError('module %s does not contain variable %s, and cannot be parsed as API calls'%
                             (importstr,self.calls_dict))

        for call in calls:
            c_obj = Call(**call)
            self.apicache[c_obj.title] = c_obj # don't use our __setitem__: userfile shouldn't dirty the cache

    def _write_to_file(self, pre_call_text, call_separator, post_call_text, 
                       call_render_func, output_path):
        calls = call_separator.join([getattr(c, call_render_func)() 
                                     for c in sorted(self.values(), key=attrgetter('path', 'method'))])

        out = '%s%s%s'%(pre_call_text, calls, post_call_text)
        f = open(output_path, 'w')
        f.write(out)
        f.close()
       
    def _write_api(self):
        '''
        Write the current state of the API to the API file
        '''
        full_fp = '%s/%s%s'%(settings.APP_HOME,self.api_fp, self.api_ext)
        separator = ',\n'
        render_func = 'to_python'
        imports = ''
        pre = '%s\n\nCALLS=['%(imports)
        post = ']'

        self._write_to_file(pre, separator, post, render_func, full_fp)

    def write_ReST_reference(self):
        '''
        Write the current state of the API to a ReST document
        '''
        header = '''
API Reference
=============

This page contains a full list of valid Indivo API calls, generated from the code.
For a more detailed walkthrough of individual calls, see :doc:`api`
'''
        full_fp = '%s/%s%s'%(settings.APP_HOME, self.api_ref_fp, self.api_ref_ext)
        render_func = 'to_ReST'
        separator = '\n\n--------\n\n'
        pre = '%s\n\n--------\n\n'%(header)
        post=''
        self._write_to_file(pre, separator, post, render_func, full_fp)

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __getitem__(self, key):
        return self.apicache[APIUtils.normalize_title(key)]

    def __setitem__(self, _key, val):
        key = APIUtils.normalize_title(_key)
        oldval = self.get(key, None)
        self.apicache[key] = val
        self.dirty = oldval != val

    def __delitem__(self, key):
        del self.apicache[key]
        self.dirty = True

    def save(self):
        if self.dirty:
            self._write_api()

    def update(self, call_dict):
        for k, v in call_dict.iteritems():
            self[k] = v

    def keys(self):
        return self.apicache.keys()
    
    def values(self):
        return self.apicache.values()

    def __repr__(self):
        dictrepr = dict.__repr__(self.apicache)
        return '%s(%s)' % (type(self).__name__, dictrepr)

class CallResolver(object):
    '''
    Takes a user-entered API call and an auto-generated API call
    and resolves their differing properties. Used in generating
    merged API calls.
    '''
    def __init__(self, cp_call, user_call, user_preferred=True):
        self.cp_call = cp_call
        self.user_call = user_call
        self.user_preferred = user_preferred

    def prefer_user(self):
        self.user_preferred = True

    def prefer_cp(self):
        self.user_preferred = False
    
    def resolve(self, field, defaults=None):
        '''
        Given an API call field, returns the value of that field
        that a merged call should use.
        '''
        if isinstance(getattr(self.cp_call, field, None), dict):
            return self._resolve_dictfield(field, defaults)
        else:
            return self._resolve_textfield(field, defaults)

    def _resolve_dictfield(self, field, defaults=None):
        cp_dict = getattr(self.cp_call, field)
        user_dict = getattr(self.user_call, field)

        all_keys = set(cp_dict.keys()).union(set(user_dict.keys()))

        retdict = {}
        for key in all_keys:
            cp_val = cp_dict.get(key, None)
            user_val = user_dict.get(key, None)
            retdict[key] = self._resolve(cp_val, user_val, key, defaults)

        return retdict

    def _resolve_textfield(self, field, defaults=None):
        cp_val = getattr(self.cp_call, field, None)
        user_val = getattr(self.user_call, field, None)
        return self._resolve(cp_val, user_val, field, defaults)
        
    def _resolve(self, cp_val, user_val, default_key=None, defaults=None):
        
        if (self.user_preferred and user_val) or not cp_val:
            retval = user_val
        else:
            retval = cp_val

        if not retval and defaults and defaults.has_key(default_key):
            retval = defaults[default_key]
        
        return retval

class Call(object):
    '''
    Representation of an Indivo API call, with rendering to ReST and Python.
    '''

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name == 'view_func_name':
            self.view_func = self._get_view_func()
        if name == 'view_func':
            self.access_rule = self._get_access_rule()
        if name == 'access_rule':
            self.access_doc = self._get_access_doc()

    def __init__(self, path=None, method=None, view_func_name='',
                 access_doc='', url_params={}, query_opts={}, data_fields={}, 
                 description='', return_desc='', return_ex='', deprecated=None,
                 added=None, changed=None):
        self.path = path
        self.method = method
        self.title = APIUtils.normalize_title('%s %s'%(method, path))
        self.view_func_name = view_func_name
        if access_doc:
            self.access_doc = access_doc
        self.url_params = url_params
        self.query_opts = query_opts
        self.data_fields = data_fields
        self.description = description
        self.return_desc = return_desc
        self.return_ex = return_ex
        self.deprecated = deprecated
        self.added = added
        self.changed = changed

    def _print_dict(self, d):
        lines = []
        for key, value in d.iteritems():
            lines.append("%s'%s':'%s',\n"%(self._indent(8), key, value))
        out = '{\n%s%s}'%(''.join(lines), self._indent(8))
        return out

    def _get_default(self, default_dict, key):
        ret = None
        if default_dict.has_key(key):
            if callable(default_dict[key]):
                try:
                    ret = default_dict[key](self)
                except:
                    pass
            else:
                ret = default_dict[key]
        return ret

    def set_defaults(self, default_maps):
        ''' Replace blank attributes of the Call with default values provided in `default_maps` '''
        for fieldname, default_map in default_maps.iteritems():
            if hasattr(self, fieldname):
                fieldval = getattr(self, fieldname, None)
            
                # The attribute is a dict, look for its keys in the map
                if isinstance(fieldval, dict):
                    for k in fieldval.keys():
                        if default_map.has_key(k) and not fieldval[k]:
                            fieldval[k] = self._get_default(default_map,k)

                # The attribute is a string, look for the attribute itself in the map
                else:
                    if default_map.has_key(fieldname) and not fieldval:
                        setattr(self, fieldname, self._get_default(default_map,fieldname))

    def _print_tuple(self, tuple, varname):
        key = '"%s": '%varname
        if tuple:
            value = str(tuple)
        else:
            value = 'None'

        return '%s%s,\n'%(key, value)
            
    def to_python(self):
        ''' 
        Render the Call to python code, for easy import.
        Output will look like:
        
        {
          'method': 'get',
          'path': '/records/{RECORD_ID}',
          'url_params': {
                          'RECORD_ID':'the Indivo record identifier',
                        },
          'view_func_name': 'record',
          'query_opts' : {
                          'offset': 'offset number. default is 0',
                         },
          'data_fields': {
                         },
          'description':'Get basic record information',
          'return_desc':'An XML snippet describing the Record',
          'return_ex':'
          <Record id="c002aa8e-1ff0-11de-b090-001b63948875" label="Jill Smith">
            <contact document_id="83nvb-038xcc-98xcv-234234325235" />
            <demographics document_id="646937a0-1ff1-11de-b090-001b63948875" />
          </Record>',
          'deprecated': ('0.9.3', 'Use :http:get:`/records/{RECORD_ID}/get`.'),
          'added':('0.9.3', ''),
          'changed':('1.0.0', 'Added *offset* to query params'),
        }
        '''
        method = '"method":"%s",\n'%self.method
        path = '"path":"%s",\n'%self.path
        view_func = '"view_func_name":"%s",\n'%self.view_func_name
        access_rule = '"access_doc":"%s",\n'%self.access_doc
        url_params = '"url_params":%s,\n'%self._print_dict(self.url_params)
        query_opts = '"query_opts":%s,\n'%self._print_dict(self.query_opts)
        data_fields = '"data_fields":%s,\n'%self._print_dict(self.data_fields)
        return_desc = '"return_desc":"%s",\n'%self.return_desc
        description = self._print_quoted_field('description', self.description)
        return_ex = self._print_quoted_field('return_ex', self.return_ex)
        deprecated = self._print_tuple(self.deprecated, 'deprecated')
        added = self._print_tuple(self.added, 'added')
        changed = self._print_tuple(self.changed, 'changed')
        indent = 4
        
        out = "{\n%s\n}"%( 
            self._indent(indent).join([
                    '', method, path, view_func, access_rule, 
                    url_params, query_opts, data_fields, description,
                    return_desc, return_ex, deprecated, added, changed]))
        return out

    def _print_quoted_field(self, key, val):
        ret = val if val else ''
        if not ret.startswith('\n'):
            ret = '\n'+ret
        if not ret.endswith('\n'):
            ret = ret+'\n'
        return '"%s":\'\'\'%s\'\'\',\n'%(key, ret)

    def to_ReST_directive(self):
        # Output will look lik
        #
        # .. http:get:: /records/{RECORD_ID}
        return ".. http:%s:: %s"%(self.method.lower(), self.path)

    def to_ReST(self):
        # Output will look like 
        #
        # .. http:get:: /records/{RECORD_ID}
        #
        #    Get basic record information.
        #
        #    :shortname: record
        #    :accesscontrol: The record owner, the admin app that created it, or an app with access to it
        #    :query order_by: one of ``label``, ``created-at``
        #    :query offset: offset number. default is 0
        #    :query limit: limit number. default is 30
        #    :param RECORD_ID: the Indivo record identifier
        #    :returns: XML describing the record
        #
        # ::
        #
        #    <Record id="c002aa8e-1ff0-11de-b090-001b63948875" label="Jill Smith">
        #      <contact document_id="83nvb-038xcc-98xcv-234234325235" />
        #      <demographics document_id="646937a0-1ff1-11de-b090-001b63948875" />
        #    </Record>
        #
        # .. versionadded:: 0.9.3
        #    
        # .. versionchanged:: 1.0.0
        #    Added *offset* to query parameters
        #
        # .. deprecated:: 0.9.3
        #    Use :http:get:`/records/{RECORD_ID}/get` instead.
        # 

        directive = self.to_ReST_directive()
        short_name = ":shortname: %s"%self.view_func_name
        access_doc = ":accesscontrol: %s"%self.access_doc
        url_params = [":parameter %s: %s"%(p, self.url_params[p]) for p in self.url_params.keys()]
        query_opts = [":queryparameter %s: %s"%(q, self.query_opts[q]) for q in self.query_opts.keys()]
        data_fields = [":formparameter %s: %s"%(d, self.data_fields[d]) for d in self.data_fields.keys()]
        returns = ":returns: %s"%self.return_desc
        indent = 3
        
        out = '%s\n%s\n%s%s%s%s%s%s'%(
            self._list_to_ReST([directive], 0),
            self._list_to_ReST(self.description.strip().split('\n'), indent),
            self._list_to_ReST([short_name], indent), 
            self._list_to_ReST([access_doc], indent),
            self._list_to_ReST(url_params, indent),
            self._list_to_ReST(query_opts, indent),
            self._list_to_ReST(data_fields, indent),
            self._list_to_ReST([returns], indent),
            )

        if self.return_ex.strip():
            ret_ex = self.return_ex
            out += '\nExample Return Value::\n'
            if not ret_ex.startswith('\n'):
                ret_ex = '\n' + ret_ex
            for line in ret_ex.split('\n'):
                out += self._indent(indent) + line + '\n'

        if self.added:
            out += self._change_directive('versionadded', self.added[0],
                                          self.added[1])
        if self.changed:
            out += self._change_directive('versionchanged', self.changed[0],
                                          self.changed[1])
        if self.deprecated:
            out += self._change_directive('deprecated', self.deprecated[0],
                                          self.deprecated[1])
        return out

    def _change_directive(self, directive_name, version, explanation):
        exp_str = '%s%s\n'%(self._indent(3), explanation) if explanation else ''
        return '\n.. %s:: %s\n%s'%(directive_name, version, exp_str)

    def _indent(self, indent):
        return " "*indent

    def _list_to_ReST(self, l, indent):
        out = ''
        for item in l:
            out += '%s%s\n'%(self._indent(indent), item)
        return out

    def _get_access_rule(self):
        return AccessRule.lookup(self.view_func) if self.view_func else None

    def _get_access_doc(self):
        if self.access_rule and self.access_rule.rule.__doc__:
            return self.access_rule.rule.__doc__
        return ''

    def _get_view_func(self):
        view_func = None
        if self.view_func_name:
            vfn = self.view_func_name
            try:
                # Is it an Indivo view?
                view_func = getattr(__import__('indivo.views', 
                                               fromlist=[vfn]), 
                                    vfn)
            except AttributeError:
                try:
                    # Is it a codingsystems view?
                    view_func = getattr(__import__('codingsystems.views', 
                                                   fromlist=[vfn]), 
                                        vfn)
                except AttributeError:
                    try:
                        # Is it a Django static view?
                        view_func = getattr(__import__('django.views.static', 
                                                       fromlist=[vfn]), 
                                            vfn)
                    except AttributeError:
                        pass
        return view_func
    
class CallParser(object):
    def __init__(self, urls):
        self.urllist = urls
        self.api = APIDict(read_file=False)
        self.parse(self.urllist, parent_path='/')

    def register(self, call):
        self.api[call.title] = call

    def lookup(self, call):
        return self.api.get(call.title, None)

    def parse(self, urllist, parent_path=''):
        for entry in urllist:
                
            # not a leaf node, recurse
            if hasattr(entry, 'url_patterns'):
                cur_path = entry.regex.pattern[1:]
                self.parse(entry.url_patterns, parent_path+cur_path)
                    
            # leaf node
            else:
                path, url_params = APIUtils.parse_url_params(parent_path + entry.regex.pattern[1:-1])

                # build up url_params for the Call constructor
                params = {}
                for param in url_params:
                    params[param[1]] = ''

                if isinstance(entry.callback, indivo.lib.utils.MethodDispatcher):
                    for method, view_func in entry.callback.methods.iteritems():
                        call = Call(path, method, view_func_name=view_func.__name__, url_params=params)
                        self.register(call)
                else:
                    method = 'GET'
                    call = Call(path, method, entry.callback.__name__, url_params=params)
                    self.register(call)

class APIUtils(object):

    @classmethod
    def _find_params(cls, url):
        params = []

        # API documentation format:
        # try matching things in {}
        for pattern in re.finditer('{(.*?)}', url):
            match = pattern.group(0)
            param = pattern.group(1).upper()
            params.append((match, param))

        # Django urlconf format:
        # match things inside <> that are in the context of (?P< your match >..) 
        for pattern in re.finditer( '\(\?P<(.*?)>.*?\)', url):
            match = pattern.group(0)
            param = pattern.group(1).upper()
            params.append((match, param))

        return params

    @classmethod
    def normalize_title(cls, title):
        method, url = title.split(' ')
        return '%s %s'%(cls.normalize_method(method),
                        cls.normalize_url(url))

    @classmethod
    def normalize_method(cls, method):
        return method.upper()
                      
    @classmethod
    def normalize_url(cls, url):
        params = cls._find_params(url)
        for i, param in enumerate(params):
            url = url.replace(param[0], '{%d}'%i)
        return url

    @classmethod
    def parse_url_params(cls, url):
        params = cls._find_params(url)
        for param in params:
            url = url.replace(param[0], '{%s}'%param[1])
        return url, params
