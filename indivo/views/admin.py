"""
Indivo Views -- Indivo Admin
"""
from base import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect 
from django.template import Context
from django.template.loader import get_template
from indivo.forms import *
from indivo.lib import admin
import copy

@login_required()
def admin_show(request):
    return admin.render_admin_response(request, 'admin/home.html') 

@login_required()    
def admin_record_show(request, record):
    # update recently viewed records
    recents = request.session.get('recent_records', set([]))
    recents.add(record) # TODO: check to see if this is a memory/performance issue
    request.session['recent_records'] = recents
    # populate form from contact document  TODO: currently only handles single phone number
    if record.contact:
        contact = Contacts.from_xml(record.contact.content)
        recordForm = RecordForm(initial={'full_name':contact.full_name,
                                         'email':contact.email,
                                         'street_address':contact.street_address,
                                         'postal_code':contact.postal_code,
                                         'country':contact.country,
                                         'phone_number':contact.phone_numbers[0]})
    else:
        recordForm = RecordForm(initial={'full_name':record.label})
        
    return admin.render_admin_response(request, 'admin/record_show.html', {
        'record_form': recordForm,
        'account_form': AccountForm(),
        'record': record
    }) 

@login_required()    
def admin_record_form(request):
    recordForm = RecordForm()
    return admin.render_admin_response(request, 'admin/record_show.html', {
        'record_form': recordForm,
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
        return admin.render_admin_response(request, 'admin/record_show.html', {
            'record_form': form,
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
        return admin.render_admin_response(request, 'admin/record_list.html',{
            'records': records,
        })

@login_required()
def admin_record_share_form(request, record):
    return admin.render_admin_response(request, 'admin/share_add.html', {
        'account_form': AccountForm(),
        'account_search_form': AccountForm(),
        'record': record,
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
            return admin.render_admin_response(request, 'admin/share_add.html', {
                'account_form': form,
                'account_search_form': AccountForm(),
                'record': record,
            })
    else:
        # Add share to existing Account
        account = []
        try:
            accounts = Account.objects.filter(full_name__icontains=request.POST['full_name'], email__icontains=request.POST['email'])
        except Exception as e:
            #TODO
            raise e
        return admin.render_admin_response(request, 'admin/share_add.html', {
                'record': record,
                'accounts': accounts,
                'account_search_form': AccountForm(initial={'full_name':request.POST['full_name'], 'email':request.POST['email']})
            })

@login_required()
def admin_record_account_share_delete(request, record, account):
    success = admin.admin_remove_fullshare(record, account)
    if not success:
        # TODO
        raise Exception("couldn't delete share!")
    
    return redirect('/admin/record/' + record.id + '/')

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
    return admin.render_admin_response(request, 'admin/owner_set.html', {
        'account_form': AccountForm(),
        'account_search_form': AccountForm(),
        'record': record,
    })

@login_required()
def admin_record_owner(request, record):
    if request.POST['existing'] == 'False':
        # Create new Account and set as Owner
        form = AccountForm(request.POST)
        if form.is_valid(): 
            # TODO: generate account id
            try:
                account = admin.admin_create_account(request.principal, form.cleaned_data['email'], full_name=form.cleaned_data['full_name'], contact_email=form.cleaned_data['email'])
                account = admin.admin_set_owner(record, account)
            except Exception as e:
                # TODO
                x =2
            return redirect('/admin/record/' + record.id +'/')
        else:
            return admin.render_admin_response(request, 'admin/owner_set.html', {
                'account_form': form,
                'account_search_form': AccountForm(),
                'record': record
            })
    else:
        # set existing Account as owner
        account = []
        try:
            accounts = Account.objects.filter(full_name__icontains=request.POST['full_name'], email__icontains=request.POST['email'])
        except Exception as e:
            #TODO
            raise e
        return admin.render_admin_response(request, 'admin/owner_set.html', {
                'record': record,
                'accounts': accounts,
                'account_search_form': AccountForm(initial={'full_name':request.POST['full_name'], 'email':request.POST['email']})
            })

@login_required()
def admin_record_account_owner_set(request, record, account):
    try:
        account = admin.admin_set_owner(record, account)
    except Exception as e:
        # TODO
        raise
    return redirect('/admin/record/' + record.id +'/')

@login_required()    
def admin_account_show(request, account):
    return admin.render_admin_response(request, 'admin/account.html', {
        'account': account
    }) 

@login_required()
def admin_account_retire(request, account):
    admin.admin_retire_account(account);
    return redirect('/admin/account/' + account.email + '/')

@login_required()
def admin_dump_state(request):
    try:
        records_file, accounts_file, shares_file = admin.dump_db()
    except Exception as e:
        # TODO
        raise

    try:
        zip_data = admin.in_mem_zipfile({'records.csv':records_file,
                                         'accounts.csv':accounts_file,
                                         'shares.csv':shares_file,})
    except Exception as e:
        # TODO
        raise
    
    response = HttpResponse(mimetype='application/zip')
    response['Content-Disposition'] = 'filename=indivodata.zip'
    response.write(zip_data)
    return response

@login_required()
@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')
def admin_users_show(request):
    return admin.render_admin_response(request, 
                                       'admin/user_list.html', 
                                       {'users':admin.admin_get_users_to_manage(request),
                                        'user_form':admin.FullUserForm(),})

@login_required()
@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')
def admin_user_create(request):
    form = admin.FullUserForm(request.POST) 
    try:
        form.save()
        return redirect('/admin/users/')
    except ValueError:
        return admin.render_admin_response(request, 
                                           'admin/user_list.html', 
                                           {'users':admin.admin_get_users_to_manage(request),
                                            'user_form':form,})
    except Exception as e:
        # TODO
        raise

@login_required()
@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')
def admin_user_edit(request, user_id):
    if request.method == "GET":
        try:
            user = User.objects.get(id=user_id)
            return admin.render_admin_response(request, 'admin/user_edit.html',
                                               {'u':user,
                                                'user_form':admin.FullUserChangeForm(instance=user),})
        except User.DoesNotExist:
            # TODO
            raise
        except Exception as e:
            # TODO
            raise
    else:
        try:
            user = User.objects.get(id=user_id)
            form = admin.FullUserChangeForm(request.POST, instance=user)
            form.save()
            return redirect('/admin/users/')
        except ValueError:
            return admin.render_admin_response(request, 'admin/user_edit.html',
                                               {'u':user,
                                                'user_form':form,})
        except User.DoesNotExist:
            # TODO
            raise
        except Exception as e:
            # TODO
            raise

@login_required()
@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')
def admin_user_deactivate(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
        return redirect('/admin/users/')
    except User.DoesNotExist:
        # TODO
        raise
    except Exception as e:
        # TODO
        raise

@login_required()
@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')
def admin_user_activate(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        return redirect('/admin/users/')
    except User.DoesNotExist:
        # TODO
        raise
    except Exception as e:
        # TODO
        raise

