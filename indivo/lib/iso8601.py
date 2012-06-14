"""ISO 8601 date time string parsing

2010-09-01 slightly refactored to use the built-in time module rather than custom regexps
"""

from datetime import datetime, time

# the iso8601 date formats we accept and produce, and nothing else for now
ISO8601_UTC_DATETIME_FORMAT_MICRO = "%Y-%m-%dT%H:%M:%S.%fZ"
ISO8601_UTC_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
ISO8601_UTC_DATE_FORMAT = "%Y-%m-%d"
ISO8601_UTC_TIME_FORMAT = "%H:%M:%SZ"

def parse_utc_date(datestring):
    """
    parse a date expected to be in UTC format, either a datetime or a date only
    """
    try:
        return datetime.strptime(datestring, ISO8601_UTC_DATE_FORMAT)
    except ValueError:
        try:
            return datetime.strptime(datestring, ISO8601_UTC_DATETIME_FORMAT_MICRO)
        except ValueError:
            # another valueerror here and we surface it to the proc calling parse
            return datetime.strptime(datestring, ISO8601_UTC_DATETIME_FORMAT)

def format_utc_date(date, date_only=False):
    try:
        if isinstance(date, time):
            return date.strftime(ISO8601_UTC_TIME_FORMAT)
        elif date_only:
            return date.strftime(ISO8601_UTC_DATE_FORMAT)
        else:
            if date.microsecond:
                return date.strftime(ISO8601_UTC_DATETIME_FORMAT_MICRO)
            else:
                return date.strftime(ISO8601_UTC_DATETIME_FORMAT)
    except ValueError:
        return "BAD DATE"
