"""
Utils for the Admin interface.

"""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import *
from django.shortcuts import render_to_response
from indivo.lib.modelutils import _record_create, _account_create
from indivo.models import *
import csv, StringIO, os
from zipfile import ZipFile

RECORD_HEADERS = ['id', 'first name', 'last name', 'email address', 
                  'street address', 'state', 'zipcode', 'country', 'phone number']
ACCOUNT_HEADERS = ['id', 'full name', 'email address',]
SHARE_HEADERS = ['record id', 'account id', 'rel type']

class ManagedCSVIO(object):
    def __init__(self, file_path=None, is_writer=True, use_dict=True, headers=None):
        self.file_path = file_path # will use StringIO if None
        self.is_writer = is_writer
        self.use_dict = use_dict
        self.headers = headers

        self.file_stream = None
    
    def __enter__(self):
        if self.file_path:
            mode = 'ab' if self.is_writer else 'rb'
            self.file_stream = open(self.file_path, mode)
        elif not self.file_stream:
            self.file_stream = StringIO.StringIO()
        else:
            self.file_stream.seek(0, os.SEEK_END)

        if self.is_writer and self.use_dict:
            interface = csv.DictWriter(self.file_stream, self.headers)
        elif self.is_writer:
            interface = csv.writer(self.file_stream)
        elif self.use_dict:
            interface = csv.DictReader(self.file_stream)
        else:
            interface = csv.reader(self.file_stream)
            
        return interface

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.file_path and self.file_stream:
            self.file_stream.close()
    
    def get_stream(self):
        if self.file_path:
            return open(self.file_path, 'r') # just open it for reading

        if not self.file_stream:
            self.file_stream = StringIO.StringIO()
        else:
            self.file_stream.seek(0) # point to the start of the file
        return self.file_stream

    def reset(self):
        # Close any in-memory buffer
        if self.file_stream:
            self.file_stream.close()

        # Truncate any file saved to disk
        if self.file_path:
            fd = open(self.file_path, 'w')
            fd.truncate()
            fd.close()

class CSVStreamManager(object):
    def __init__(self, headers):
        self.headers = headers
        self.io_obj = ManagedCSVIO(headers=self.headers)
        self.write_headers()

    def write_headers(self):
        self.io_obj.is_writer = True
        self.io_obj.use_dict = False
        with self.io_obj as writer:
            writer.writerow(self.headers)

    def read(self):
        data = []
        self.io_obj.is_writer = False
        self.io_obj.use_dict = True
        with self.io_obj as reader:
            data = [line for line in reader]

        return data

    def write(self, rows):
        if not isinstance(rows, list):
            rows = [rows]

        self.io_obj.is_writer = True
        self.io_obj.use_dict = True
        with self.io_obj as writer:
            writer.writerows(rows)
            
    def get_stream(self):
        return self.io_obj.get_stream()

def in_mem_zipfile(file_dict):
    buf = StringIO.StringIO()
    zipped = ZipFile(buf, 'a')
    for name, file_obj in file_dict.iteritems():
        file_obj.seek(0)
        zipped.writestr(name, file_obj.read())
    zipped.close()
    buf.flush()
    data = buf.getvalue()
    buf.close()
    return data

def dump_db():
    """ Get a list of all records, accounts, and their relationships as csv data.

    Returns a tuple of (recordstream, accountstream, relationshipstream),
    where each stream is a file-like object containing csv data.

    """

    record_manager = CSVStreamManager(RECORD_HEADERS)
    account_manager = CSVStreamManager(ACCOUNT_HEADERS)
    share_manager = CSVStreamManager(SHARE_HEADERS)

    for record in Record.objects.all().iterator():
        
        # Write all the records
        data = {'id':record.id}
        if record.contact:
            contact = Contacts.from_xml(record.contact.content)
            phone_number = contact.phone_numbers[0] if contact.phone_numbers else ''
            contact_data = {
                'first name': contact.given_name,
                'last name': contact.family_name,
                'email address': contact.email,
                'street address': contact.street_address,
                'state': contact.region,
                'zipcode': contact.postal_code,
                'country': contact.country,
                'phone number': phone_number,
                }
        else:
            contact_data = {
                'first name': '',
                'last name': '',
                'email address': '',
                'street address': '',
                'state': '',
                'zipcode': '',
                'country': '',
                'phone number': '',
                }

        data.update(contact_data)
        record_manager.write(data)

        # Write all the owners
        if record.owner:
            data = {'record id': record.id,
                    'account id': record.owner.email,
                    'rel type': 'Owner',
                    }
            share_manager.write(data)

    # Write all the accounts
    for account in Account.objects.all().iterator():
        data = {'id':account.email,
                'full name': account.full_name,
                'email address': account.contact_email,
                }
        account_manager.write(data)
            
    # Write all the full shares
    for share in AccountFullShare.objects.all().iterator():
        data = {'record id': share.record.id,
                'account id': share.with_account.email,
                'rel type': 'Guardian',
                }
        share_manager.write(data)

    # Return the streams
    return (record_manager.get_stream(), account_manager.get_stream(), share_manager.get_stream(),)

def admin_create_record(contact_xml, creator):
    """" 
    Create a record, then log that to the admin logs.
    """
    record = _record_create(creator, contact_xml)
    return record

def admin_create_account(creator, account_id, full_name='', contact_email=None):
    account = _account_create(creator, account_id=account_id, full_name=full_name,
                              contact_email=contact_email, secondary_secret_p="1")
    return account

def admin_create_fullshare(record, account):
    RecordNotificationRoute.objects.get_or_create(record=record, account=account)
    share, created_p = AccountFullShare.objects.get_or_create(record=record, with_account=account, 
                                                              role_label='Guardian')
    return share

def admin_remove_fullshare(record, account):
    try:
        AccountFullShare.objects.get(record=record, with_account=account).delete()
    except AccountFullShare.DoesNotExist:
        return False

    return True

def admin_set_owner(record, account):
    record.owner = account
    record.save()

    return account

def admin_retire_account(account):
    account.set_state('retired')
    return account

def admin_create_user(creator, username, password, is_superuser = False, first_name=None, last_name=None, email=None):
    if not creator.is_superuser:
        raise PermissionDenied('only superusers may create other users.')
    
    # Look for other users with the same username first, to avoid the evil IntegrityError
    if User.objects.filter(username=username).exists():
        raise ValueError('a user with that username already exists.')

    user = User.objects.create_user(username, email=email, password=password)
    user.is_superuser = is_superuser
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return user

def render_admin_response(request, template_path, context={}):
    # add in the User and recent Records to all admin Contexts
    recents = request.session.get('recent_records', set([]))
    admin_context = {'recents':recents,
                     'user':request.user}
    admin_context.update(context)
    return render_to_response(template_path, admin_context) 
