"""
Indivo Views -- Indivo Admin
"""
from base import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.shortcuts import redirect 
from django.template import Context
from django.template.loader import get_template
from indivo.forms import *
from indivo.lib import admin
import pdb

@login_required()
def admin_show(request):
    return render_to_response('admin/home.html') 

@login_required()    
def admin_record_show(request, record):
    # read in recently viewed records
    recents = request.session.get('recent_records', set([]))
    recents.add(record.id)
    request.session['recent_records'] = recents
    # populate form from contact document  TODO: currently only handles single phone number
    contact = Contacts.from_xml(record.contact.content)
    recordForm = RecordForm(initial={'full_name':contact.full_name,
                                     'email':contact.email,
                                     'street_address':contact.street_address,
                                     'postal_code':contact.postal_code,
                                     'country':contact.country,
                                     'phone_number':contact.phone_numbers[0]})
    return render_to_response('admin/record_show.html', {
        'record_form': recordForm,
        'account_form': AccountForm(),
        'record': record,
        'recents': recents
    }) 

@login_required()    
def admin_record_form(request):
    recordForm = RecordForm()
    return render_to_response('admin/record_show.html', {
        'record_form': recordForm
    }) 

@login_required()
def admin_record_create(request):
    form = RecordForm(request.POST) 
    if form.is_valid(): 
        # Process the data in form.cleaned_data
        contact_dict = dict({'contact': form.cleaned_data})
        contact_dict['contact']['phone_numbers'] = [contact_dict['contact']['phone_number']]
        contactXML = get_template("contacts.xml").render(Context(contact_dict))
        try:
            account_args = settings.DEFAULT_ADMIN_OWNER
            email = account_args['email']
            if not account_args['contact_email']:
                account_args['contact_email'] = email
            del account_args['email']
            default_owner = Account.objects.get_or_create(email=email, 
                                          defaults=account_args)[0]
            record = admin.admin_create_record(contactXML, default_owner)
        except Exception as e:
            # TODO
            raise
        return redirect('/admin/record/' + record.id + '/')
    else:
        return render_to_response('admin/record_show.html', {
            'record_form': form
        })  

@login_required()    
def admin_record_search(request):
    search_string = request.GET['search_string']
    try:
        records = Record.objects.filter(label__icontains=search_string)
    except Exception as e:
        #TODO
        raise
    if (len(records) == 1):
        return redirect('/admin/record/' + records[0].id + '/')
    else:
        return render_to_response('admin/record_list.html',{
            'records': records
        })

@login_required()
def admin_record_share_form(request, record):
    return render_to_response('admin/share_add.html', {
        'account_form': AccountForm,
        'account_search_form': AccountForm,
        'record': record
    })
    
@login_required()
def admin_record_share_add(request, record):
    if request.POST['existing'] == 'False':
        # Create new Account and add Share
        form = AccountForm(request.POST)
        if form.is_valid(): 
            # TODO: generate account id
            try:
                account = admin.admin_create_account(request.principal, form.cleaned_data['email'], full_name=form.cleaned_data['full_name'], contact_email=form.cleaned_data['email'])
                share = admin.admin_create_fullshare(record, account)
            except Exception as e:
                # TODO
                raise
            return redirect('/admin/record/' + record.id +'/')
        else:
            return render_to_response('admin/share_add.html', {
                'account_form': form,
                'account_search_form': AccountForm(),
                'record': record
            })
    else:
        # Add share to existing Account
        account = []
        try:
            accounts = Account.objects.filter(full_name__icontains=request.POST['full_name'], email__icontains=request.POST['email'])
        except Exception as e:
            #TODO
            raise e
        
        return render_to_response('admin/share_add.html', {
                'record': record,
                'accounts': accounts,
                'account_search_form': AccountForm(),
            })
    
@login_required()
def admin_record_account_share_add(request, record, account):
    try:
        share = admin.admin_create_fullshare(record, account)
    except Exception as e:
        # TODO
        raise
    return redirect('/admin/record/' + record.id +'/')

@login_required()
def admin_record_owner_form(request, record):
    return render_to_response('admin/owner_set.html', {
        'account_form': AccountForm,
        'account_search_form': AccountForm,
        'record': record
    })

@login_required()
def admin_record_owner(request, record):
    if request.POST['existing'] == 'False':
        # Create new Account and set as Owner
        form = AccountForm(request.POST)
        if form.is_valid(): 
            # TODO: generate account id
            pdb.set_trace()
            try:
                account = admin.admin_create_account(request.principal, form.cleaned_data['email'], full_name=form.cleaned_data['full_name'], contact_email=form.cleaned_data['email'])
                account = admin.admin_set_owner(record, account)
            except Exception as e:
                # TODO
                x =2
            return redirect('/admin/record/' + record.id +'/')
        else:
            return render_to_response('admin/share_add.html', {
                'account_form': form,
                'account_search_form': AccountForm(),
                'record': record
            })
    else:
        # TODO
        return redirect('/admin/record/' + record.id +'/')