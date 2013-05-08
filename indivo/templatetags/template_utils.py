from django import template
from indivo.lib import iso8601

register = template.Library()

# this used to be a string filter, but that forces us to check silly things like the STRING "None",
# so instead this is just a normal filter, and it returns the empty string if it's null
@register.filter(is_safe=True)
def check_empty(value):
  if value == None:
    return ''
  else:
    return value

# this is definitely not a string filter, it should be a real timestamp
@register.filter(is_safe=True)
def format_iso8601_datetime(timestamp):
  if timestamp:
    return iso8601.format_utc_date(timestamp)
  else:
    return ""

@register.filter(is_safe=True)
def format_iso8601_date(timestamp):
  if timestamp:
    return iso8601.format_utc_date(timestamp, date_only = True)
  else:
    return ""