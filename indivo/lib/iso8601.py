"""ISO 8601 date time string parsing

2010-09-01 slightly refactored to use the built-in time module rather than custom regexps
"""

from datetime import datetime, time
import isodate

from django.utils import timezone

# the iso8601 date formats we accept and produce, and nothing else for now
ISO8601_UTC_DATETIME_FORMAT_MICRO = "%Y-%m-%dT%H:%M:%S.%fZ"
ISO8601_UTC_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
ISO8601_UTC_DATE_FORMAT = "%Y-%m-%d"
ISO8601_UTC_TIME_FORMAT = "%H:%M:%SZ"


def format_utc_date(date, date_only=False):
    """Format a datetime, date, or time to ISO 8601 UTC

    :param date: datetime/date/time to format
    :param date_only: force output of only date component
    :return: ISO 8601 UTC string representation

    """
    try:
        if isinstance(date, time):
            return isodate.strftime(date, ISO8601_UTC_TIME_FORMAT)
        elif date_only:
            return isodate.strftime(date, ISO8601_UTC_DATE_FORMAT)
        else:
            if date.microsecond:
                return isodate.strftime(date, ISO8601_UTC_DATETIME_FORMAT_MICRO)
            else:
                return isodate.strftime(date, ISO8601_UTC_DATETIME_FORMAT)
    except ValueError:
        return "BAD DATE"  # TODO: poor behaviour


def parse_iso8601_date(string):
    """Parse an ISO 8601 string into a date

    :param string: ISO 8601 string to parse
    """
    return isodate.parse_date(string)


def parse_iso8601_datetime(string):
    """Parse an ISO 8601 string into a datetime

      * forces datetime into UTC if TZ not specified

      * sets time component to time.min if not specified

    :param string: ISO 8601 string to parse
    """
    result = None

    try:
        result = isodate.parse_datetime(string)
    except ValueError:
        result = isodate.parse_date(string)
        result = datetime.combine(result, time.min)

    if result and timezone.is_naive(result):
        result = timezone.make_aware(result, timezone.utc)

    return result