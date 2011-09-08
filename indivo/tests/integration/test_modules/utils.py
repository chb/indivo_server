"""
Utils for testing
"""

import copy
from lxml import etree

def assert_403(resp, message=""):
    return assert_response_code(resp, 403, message)


def assert_200(resp, message=""):
    return assert_response_code(resp, 200, message)

def assert_400(resp, message=""):
    return assert_response_code(resp, 400, message)

def assert_404(resp, message=""):
    return assert_response_code(resp, 404, message)

def assert_response_code(resp, code, message):
    assert resp.response['response_status'] == code, '%s: status is %s instead of %s' % (message, resp.response['response_status'], code)

def combine_dicts(d1, d2):
    result_d = copy.copy(d1)
    result_d.update(d2)
    return result_d


def parse_xml(resp_or_raw_data):
    if hasattr(resp_or_raw_data, 'response'):
        if resp_or_raw_data.response['response_status'] != 200:
            raise ValueError("not a 200 response trying to parse XML")

        raw_data = resp_or_raw_data.response['response_data']
    else:
        raw_data = resp_or_raw_data

    return etree.XML(raw_data)

def xpath(xml, xpath_expr, namespaces=None):
    return xml.xpath(xpath_expr, namespaces=namespaces)
    
