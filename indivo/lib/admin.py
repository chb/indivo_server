"""
Utils for the Admin interface.

"""

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import *
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
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

class FullUserForm(UserCreationForm):
    first_name = forms.RegexField(label=_("First Name"), max_length=30, regex=r'^[\w.-]+\s*$',
                                  help_text= _("User's first name."),
                                  error_messages = {'invalid': _("This value may contain only letters, numbers and ./- characters.")})
    last_name = forms.RegexField(label=_("Last Name"), max_length=30, regex=r'^[\w.-]+\s*$',
                                  help_text= _("User's last name."),
                                  error_messages={'invalid': _("This value may contain only letters, numbers and ./- characters.")})
    email = forms.EmailField(label=_("Email Address"), help_text=_("User's email address."),
                             error_messages={'invalid':_("This value must be a valid email address")})
    is_superuser = forms.BooleanField(label=_("Super User"))

    def save(self, commit=True):
        user = super(FullUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"].strip()
        user.last_name = self.cleaned_data["last_name"].strip()
        user.email = self.cleaned_data["email"]
        user.is_superuser = self.cleaned_data["is_superuser"]
        if commit:
            user.save()
        return user

class FullUserChangeForm(UserChangeForm):
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput, 
                                required=False)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."), required=False)

    first_name = forms.RegexField(label=_("First Name"), max_length=30, regex=r'^[\w.-]+\s*$',
                                  help_text= _("User's first name."),
                                  error_messages = {'invalid': _("This value may contain only letters, numbers and ./- characters.")})
    last_name = forms.RegexField(label=_("Last Name"), max_length=30, regex=r'^[\w.-]+\s*$',
                                  help_text= _("User's last name."),
                                  error_messages={'invalid': _("This value may contain only letters, numbers and ./- characters.")})
    email = forms.EmailField(label=_("Email Address"), help_text=_("User's email address."),
                             error_messages={'invalid':_("This value must be a valid email address")})
    is_superuser = forms.BooleanField(label=_("Super User"))

    def save(self, commit=True):
        user = super(FullUserChangeForm, self).save(commit=False)
        new_pw = self.cleaned_data['password1']
        if new_pw.strip():
            user.set_password(new_pw)
        user.first_name = self.cleaned_data['first_name'].strip()
        user.last_name = self.cleaned_data['last_name'].strip()
        user.email = self.cleaned_data['email']
        user.is_superuser = self.cleaned_data['is_superuser']
        if commit:
            user.save()
        return user
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "is_superuser",)

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
    account.save()
    return account

def admin_get_users_to_manage(request):
    users = User.objects.all().order_by('username')
    return users

def render_admin_response(request, template_path, context={}):
    # add in the User and recent Records to all admin Contexts
    recents = request.session.get('recent_records', set([]))
    admin_context = {'recents':recents,
                     'user':request.user}
    admin_context.update(context)
    return render_to_response(template_path, admin_context,
                              context_instance=RequestContext(request))
