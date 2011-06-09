import time
from django import template
from django.http import HttpResponse
from django.template import Context, loader
from django.template.defaultfilters import stringfilter
from indivo.models import Document
from indivo.lib import iso8601
from indivo.views.documents.document import _set_doc_latest, _get_doc_relations

register = template.Library()

# this used to be a string filter, but that forces us to check silly things like the STRING "None",
# so instead this is just a normal filter, and it returns the empty string if it's null
@register.filter
def check_empty(value):
  if value == None:
    return ''
  else:
    return value
check_empty.is_safe = True


@register.filter
@stringfilter
def get_doc_obj(doc_id):
  try:
    doc = Document.objects.get(id=doc_id)
    
    # append the doc metadata
    _set_doc_latest(doc)
    doc.relates_to, doc.is_related_from = _get_doc_relations(doc)

    return loader.get_template('document.xml').render(Context({'doc': doc, 'record': doc.record}))
  except:
    return ""
get_doc_obj.is_safe = True

# this is definitely not a string filter, it should be a real timestamp
@register.filter
def format_iso8601_datetime(timestamp):
  if timestamp:
    return iso8601.format_utc_date(timestamp)
  else:
    return ""
format_iso8601_datetime.is_safe = True

@register.filter
def format_iso8601_date(timestamp):
  if timestamp:
    return iso8601.format_utc_date(timestamp, date_only = True)
  else:
    return ""
format_iso8601_date.is_safe = True
