"""
Utils for the Admin interface.

"""

from django.conf import settings
from indivo.views.record import _record_create
from indivo.views.account import _account_create
from indivo.lib import iso8601
from lxml import etree
from indivo.models import *
import os, csv, datetime, lockfile

RECORD_HEADERS = ['id', 'first name', 'last name', 'email address', 
                  'street address', 'zipcode', 'country', 'phone number']
ACCOUNT_HEADERS = ['id', 'first_name', 'last_name', 'email address',]
SHARE_HEADERS = ['record_id', 'account_id', 'rel_type']
ADMINLOG_HEADERS = ['user email', 'view_func', 'datetime']


class CSVManager(object):
    def __init__(self, filepath, headers):
        self.fp = filepath
        self.lock = FileLock(self.fp)
        self.data = []
        self.headers = headers

    def add(self, row_or_rows, write=False):
        if not isinstance(row_or_rows, dict):
            self.data += row_or_rows
        else:
            self.data.append(row_or_rows)
        
        if write:
            self.write()

    def read(self):
        buf = open(self.fp, 'rb')
        reader = csv.DictReader(buf) # uses the first line as headers
        for line in enumerate(self.reader):
            self.data.append(line)
        buf.close()

    def write(self):
        buf = open(self.fp, 'wb')
        fieldnames = self.headers
        writer = csv.DictWriter(buf, fieldnames)
        writer.writerow(self.headers)
        writer.writerows(self.data)
        buf.close()
            
class IndivoCSVManager(CSVManager):
    def __init__(self, filename, headers):
        csvdir = settings.ADMIN_LOG_PATH
        if not os.path.exists(csvdir):
            os.makedirs(csvdir)

        filepath = os.path.join(csvdir, filename)
        super(IndivoCSVManager, self).__init__(filepath, headers)

class RecordCSVManager(IndivoCSVManager):

    def __init__(self):
        filename = 'records.csv'
        headers = RECORD_HEADERS
        super(RecordCSVManager, self).__init__(filename, headers)

class AccountCSVManager(IndivoCSVManager):

    def __init__(self):
        filename = 'accounts.csv'
        headers = ACCOUNT_HEADERS
        super(AccountCSVManager, self).__init__(filename, headers)


class ShareCSVManager(IndivoCSVManager):

    def __init__(self):
        filename = 'shares.csv'
        headers = SHARE_HEADERS
        super(ShareCSVManager, self).__init__(filename, headers)

class AdminLogCSVManager(IndivoCSVManager):

    def __init__(self):
        filename = 'adminlogs.csv'
        headers = ADMINLOG_HEADERS
        super(AdminLogCSVManager, self).__init__(filename, headers)

def admin_log(func):
    """ View decorator which will log information about the user making an admin request. """
    @wraps(func)
    def _inner(request, *args, **kwargs):
        data = {'user email': request.user.email,
                'view_func' : func.__name__,
                'datetime' : iso8601.format_utc_date(datetime.datetime.now()),
                }
        manager = AdminLogCSVManager()
        with manager.lock:
            manager.read()
            manager.add(data, write=True)

        return func(request, *args, **kwargs)

    return _inner


def admin_create_record(contact_xml, creator):
    """" 
    Create a record, then log that to the admin logs.
    """
    record = _record_create(creator, contact_xml)
    contact = Contacts.from_xml(record.contact.content)
    phone_number = contact.phone_numbers[0] if contact.phone_numbers else ''
    data = {'id': record.id,
            'first name': contact.given_name,
            'last name': contact.family_name,
            'email address': contact.email,
            'street address': contact.street_address,
            'state': contact.region,
            'zipcode': contact.postal_code,
            'country': contact.country,
            'phone number': phone_number,
            }
    
    manager = RecordCSVManager()
    with manager.lock:
        manager.read()
        manager.add(data, write=True)
    return record

def admin_create_account(creator, account_id, full_name='', contact_email=None):
    account = _account_create(creator, account_id=account_id, full_name=full_name,
                              contact_email=contact_email, secondary_secret_p="1")
    namebits = account.full_name.split(' ')
    data = {'id':account.email,
            'first name': namebits[0],
            'last name': namebits[1],
            'email address': account.contact_email,
            }

    manager = AccountCSVManager()
    with manager.lock:
        manager.read()
        manager.add(data, write=True)
    return account

def admin_create_fullshare(record, account):
    RecordNotificationRoute.objects.get_or_create(record=record, account=account)
    share, created_p = AccountFullShare.objects.get_or_create(record=record, with_account=account, 
                                                              role_label='Guardian')
    if created_p:
        data = {'record_id': record.id,
                'account_id': account.email,
                'rel_type': 'Guardian',
                }
        manager = ShareCSVManager()
        with manager.lock:
            manager.read()
            manager.add(data, write=True)

    return share

def admin_set_owner(record, account):
    record.owner = account
    record.save()

    data = {'record_id': record.id,
            'account_id': account.email,
            'rel_type': 'Owner',
            }
    manager = ShareCSVManager()
    with manager.lock:
        manager.read()
        manager.add(data, write=True)

    return account
