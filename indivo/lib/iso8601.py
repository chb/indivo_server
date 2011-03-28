"""ISO 8601 date time string parsing

Basic usage:
>>> import iso8601
>>> iso8601.parse_date("2007-01-25T12:00:00Z")
datetime.datetime(2007, 1, 25, 12, 0, tzinfo=<iso8601.iso8601.Utc ...>)
>>>

2010-09-01 slightly refactored to use the built-in time module rather than custom regexps
"""

from datetime import datetime, timedelta, tzinfo, date
import time
import re

__all__ = ["parse_date", "ParseError"]

# Adapted from http://delete.me.uk/2005/03/iso8601.html
ISO8601_REGEX = re.compile(r"(?P<year>[0-9]{4})(-(?P<month>[0-9]{1,2})(-(?P<day>[0-9]{1,2})"
    r"((?P<separator>.)(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2})(:(?P<second>[0-9]{2})(\.(?P<fraction>[0-9]+))?)?"
    r"(?P<timezone>Z|(([-+])([0-9]{2}):([0-9]{2})))?)?)?)?"
)
TIMEZONE_REGEX = re.compile("(?P<prefix>[+-])(?P<hours>[0-9]{2}).(?P<minutes>[0-9]{2})")

# the iso8601 date formats we accept and produce, and nothing else for now
ISO8601_UTC_DATETIME_FORMAT_MICRO = "%Y-%m-%dT%H:%M:%S.%fZ"
ISO8601_UTC_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
ISO8601_UTC_DATE_FORMAT = "%Y-%m-%d"

class ParseError(Exception):
    """Raised when there is a problem parsing a date string"""

# Yoinked from python docs
ZERO = timedelta(0)
class Utc(tzinfo):
    """UTC
    
    """
    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO
UTC = Utc()

class FixedOffset(tzinfo):
    """Fixed offset in hours and minutes from UTC
    
    """
    def __init__(self, offset_hours, offset_minutes, name):
        self.__offset = timedelta(hours=offset_hours, minutes=offset_minutes)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return ZERO
    
    def __repr__(self):
        return "<FixedOffset %r>" % self.__name

def parse_timezone(tzstring, default_timezone=UTC):
    """Parses ISO 8601 time zone specs into tzinfo offsets
    
    """
    if tzstring == "Z":
        return default_timezone
    # This isn't strictly correct, but it's common to encounter dates without
    # timezones so I'll assume the default (which defaults to UTC).
    # Addresses issue 4.
    if tzstring is None:
        return default_timezone
    m = TIMEZONE_REGEX.match(tzstring)
    prefix, hours, minutes = m.groups()
    hours, minutes = int(hours), int(minutes)
    if prefix == "-":
        hours = -hours
        minutes = -minutes
    return FixedOffset(hours, minutes, tzstring)

def parse_date(datestring, default_timezone=UTC):
    """Parses ISO 8601 dates into datetime objects
    
    The timezone is parsed from the date string. However it is quite common to
    have dates without a timezone (not strictly correct). In this case the
    default timezone specified in default_timezone is used. This is UTC by
    default.
    """
    if not isinstance(datestring, basestring):
        raise ParseError("Expecting a string %r" % datestring)
    m = ISO8601_REGEX.match(datestring)
    if not m:
        raise ParseError("Unable to parse date string %r" % datestring)
    groups = m.groupdict()
    if groups["hour"] != None:
        tz = parse_timezone(groups["timezone"], default_timezone=default_timezone)
        if groups["fraction"] is None:
            groups["fraction"] = 0
        else:
            groups["fraction"] = int(float("0.%s" % groups["fraction"]) * 1e6)
        return datetime(int(groups["year"]), int(groups["month"]), int(groups["day"]),
                        int(groups["hour"]), int(groups["minute"]), int(groups["second"]),
                        int(groups["fraction"]), tz)
    else:
        return date(int(groups["year"]), int(groups["month"]), int(groups["day"]))

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
        if date_only:
            return date.strftime(ISO8601_UTC_DATE_FORMAT)
        else:
            return date.strftime(ISO8601_UTC_DATETIME_FORMAT)
    except ValueError:
        return "BAD DATE"
