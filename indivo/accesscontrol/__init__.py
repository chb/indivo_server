"""
Access Rule Initialization
"""
import sys
from accessfunc import *
from access_rule import AccessRule
from indivo.views import *
from django.contrib.auth.views import login, logout

def load_access_rules():
  """
  Initializes the accesscontrol system by loading the access rules for the views
  """  
  # These are run after the paramloader middleware, which means kw_args have been
  # converted to Django models.
  # Thus, access_funcs should take 'record', 'carenet', 'account', etc. instead of
  # view_args, view_kwargs.
  #
  # The syntax for defining an access rule is:
  #
  # def access_type_name(principal, record, account, **unused_args):
  #   ...func here...
  # views = [view_func_1, view_func_2, ...]
  # AccessRule('Access Type Name', access_type_name, views)
  #
  # For consistency, name AccessRules after the name of the access function.
  # Note the unused_args parameter to the access function. This allows different
  # views with different kw_args to share access functions without throwing exceptions:
  # make sure to include it in every access function.
  #
  # Also, each access function should have a doc string that describes what principals
  # it will accept. Doc strings should complete the sentence, 'The views protected by this
  # access function may be accessed by...'


  # These view functions will always throw 403, as they are either not used in the API or unimplemented:
  # inactive_views = [documents_delete,
  #                   carenet_app_permissions] 
  
  # Top-level views
  def basic_access(principal, **unused_args):
    """Any principal in Indivo."""
    return principal.basicPrincipalRole()
  # WARNING: This gives request tokens and 'no-users' access to these. Is this a problem?
  views = [get_version, # no-users should have access. Should reqtokens?
           all_phas,
           pha, # should either have access?
           login,
           logout,] 
  AccessRule('Basic Access', basic_access, views)

  def admin_access(principal, **unused_args):
    """Any user authenticated in the admin."""
    return principal.adminRole()
  views = [admin_show,
           admin_record_create,
           admin_record_show,
           admin_record_form,
           admin_record_owner_form,
           admin_record_owner,
           admin_record_account_owner_set,
           admin_record_search,
           admin_record_share_form,
           admin_record_share_add,
           admin_record_account_share_add,
           admin_record_account_share_delete,
           admin_account_show,
           admin_account_retire,
           admin_dump_state,]
  AccessRule('Admin Access', admin_access, views)

  # Account-related views
  def account_management_owner(principal, account, **unused_args):
    """Any admin app, or the Account owner."""
    return principal.isType('MachineApp') or principal.isSame(account)
  views = [account_info,
           account_info_set,
           account_username_set]
  AccessRule('Account Management Owner', account_management_owner, views)

  def account_management_by_record(principal, record, **unused_args):
    """Any admin app, or a principal in full control of the record."""
    return full_control(principal, record) \
        or principal.isType('MachineApp')
  views = [pha_record_delete,
           record_pha_enable]
  AccessRule('Account Management By Record', account_management_by_record, views)

  def account_management_no_admin_app(principal, account, **unused_args):
    """The Account owner."""
    return principal.isSame(account)
  views = [account_password_change,
           record_list,
           account_inbox,
           account_inbox_message,
           account_inbox_message_attachment_accept,
           account_message_archive,
           account_notifications,
           account_permissions]
  AccessRule('Account Management No Admin App', 
             account_management_no_admin_app, views)           

  def account_management_admin_app_only(principal, **unused_args):
    """Any admin app."""
    return principal.isType('MachineApp')
  views = [account_create, 
           account_search,
           account_forgot_password, 
           account_authsystem_add,
           account_check_secrets,
           account_resend_secret,
           account_reset,
           account_set_state,
           account_password_set,
           account_primary_secret,
           record_create,
           record_set_owner,
           record_pha_setup,
           account_secret,
           account_send_message]
  AccessRule('Account Management Admin App Only', 
             account_management_admin_app_only, views)

  def account_management_by_ext_id(principal, principal_email, **unused_args):
    """An admin app with an id matching the principal_email in the URL."""
    return principal.isType('MachineApp') \
        and principal.email == principal_email # No scoping ext_ids to different principals
  views = [record_create_ext]
  AccessRule('Account Management By Ext Id', 
             account_management_by_ext_id, views)

  def chrome_app_priveleges(principal, **unused_args):
    """Any Indivo UI app."""
    return principal.isType('chrome')
  views = [session_create,
           account_initialize]
  AccessRule('Chrome App Priveleges', chrome_app_priveleges, views)

  # PHA-related views
  def app_specific_priveleges(principal, pha, **unused_args):
    """The user app itself."""
    return pha_app_access(principal, pha)
  views = [pha_delete]
  AccessRule('App Specific Priveleges', app_specific_priveleges, views)

  # Oauth-related views
  def account_for_oauth(principal, **unused_args):
    """Any Account."""
    return principal.isType('Account')
  views = [request_token_claim, 
           request_token_info,
           surl_verify]
  AccessRule('Account For Oauth', account_for_oauth, views)

  def app_for_oauth(principal, **unused_args):
    """Any user app."""
    return principal.isType('PHA')
  views = [request_token]
  AccessRule('App For Oauth', app_for_oauth, views)

  def reqtoken_for_oauth(principal, **unused_args):
    """A request signed by a RequestToken."""
    return principal.isType('ReqToken')
  views = [exchange_token]
  AccessRule('Reqtoken For Oauth', reqtoken_for_oauth, views)

  def token_approval_admin(principal, reqtoken, **unused_args):
    """A principal in the carenet to which the request token is restricted (if the token is restricted), or a principal with full control over the record (if the token is not restricted)."""
    carenet_reqtoken = False
    carenet = reqtoken.carenet
    if carenet and reqtoken:
      carenet_reqtoken = principal.isInCarenet(carenet) and reqtoken.pha.isInCarenet(carenet)
    token_admin = full_control(principal, reqtoken.record)
    return carenet_reqtoken or token_admin
  views = [request_token_approve]
  AccessRule('Token Approval Admin', token_approval_admin, views)

  # Carenet-related views
  def carenet_read_access(principal, carenet, **unused_args):
    """A principal in the carenet, in full control of the carenet's record, or any admin app."""
    return full_control(principal, carenet.record) \
        or principal.isInCarenet(carenet) \
        or principal.isType('MachineApp')
  views = [carenet_account_list, # WHY CAN'T A PHA DO THESE? (they should)
           carenet_apps_list]
  AccessRule('Carenet Read Access', carenet_read_access, views)

  # Should admins do these? Why can't record-level PHAs do these? define more clearly
  def carenet_control(principal, carenet, **unused_args):
    """A principal in full control of the carenet's record."""
    return full_control(principal, carenet.record)
  views = [carenet_delete,
           carenet_rename,
           carenet_account_create,
           carenet_account_delete,
           carenet_apps_create,
           carenet_apps_delete,
           carenet_document_placement,
           carenet_document_delete]
  AccessRule('Carenet Control', carenet_control, views)

  def carenet_read_all_access(principal, carenet, account, **unused_args):
    """A user app with access to the carenet and proxying the account, a principal in full control of the carenet's record, or any admin app."""
    return (pha_carenet_access(principal, carenet) and principal.effective_principal.isSame(account)) \
        or full_control(principal, carenet.record) \
        or (principal.isInCarenet(carenet) and principal.isSame(account)) \
        or principal.isType('MachineApp')
  views = [carenet_account_permissions]
  AccessRule('Carenet Read All Access', carenet_read_all_access, views)

  # Record-related views
  def record_limited_access(principal, record, **unused_args):
    """A principal in full control of the record, or any admin app."""
    return full_control(principal, record) \
        or principal.isType('MachineApp')
  views = [record_phas,
           record_pha,
           record_get_owner,
           carenet_list,
           carenet_create]
  AccessRule('Record Limited Access', record_limited_access, views)

  def record_access(principal, record, **unused_args):
    """A principal in full control of the record, the admin app that created the record, or a user app with access to the record."""
    return pha_record_access(principal, record) \
        or full_control(principal, record) \
        or principal.createdRecord(record) # Admins can only view records they created
  views = [record]
  AccessRule('Record Access', record_access, views)

  def record_full_admin(principal, record, **unused_args):
    """The owner of the record, or any admin app."""
    return principal.ownsRecord(record) \
        or principal.isType('MachineApp')
  # Decision: PHAs shouldn't be allowed to manipulate sharing, at least not yet.
  views = [record_shares,
           record_share_add,
           record_share_delete]
  AccessRule('Record Full Admin', record_full_admin, views)

  # WHY CAN'T ACCOUNTS DO THIS?
  def record_message_access(principal, record, **unused_args):
    """Any admin app, or a user app with access to the record."""
    return pha_record_access(principal, record) \
        or principal.isType('MachineApp')
  views = [record_notify,
           record_send_message,
           record_message_attach]
  AccessRule('Record Message Access', record_message_access, views)

  # Document-related views
  def carenet_doc_access(principal, carenet, **unused_args):
    """A user app with access to the carenet or the entire carenet's record, or an account in the carenet or in control of the record."""
    return pha_carenet_access(principal, carenet) \
        or principal.isInCarenet(carenet) \
        or pha_record_access(principal, carenet.record) \
        or full_control(principal, carenet.record)
  views = [carenet_measurement_list,
           carenet_immunization_list,
           carenet_allergy_list,
           carenet_medication_list,
           carenet_procedure_list,
           carenet_problem_list,
           carenet_equipment_list,
           carenet_vitals_list,
           carenet_simple_clinical_notes_list,
           carenet_lab_list,
           carenet_document_list,
           carenet_document,
           carenet_document_meta]
  AccessRule('Carenet Doc Access', carenet_doc_access, views)

  def carenet_special_doc_access(principal, carenet, **unused_args):
    """A user app with access to the carenet or the entire carenet's record, an account in the carenet or in control of the record, or the admin app that created the carenet's record."""
    return carenet_doc_access(principal, carenet) \
        or principal.createdRecord(carenet.record)
  views = [read_special_document_carenet]
  AccessRule('Carenet Special Doc Access', carenet_special_doc_access, views)

  def record_doc_access(principal, record, **unused_args):
    """A user app with access to the record, or a principal in full control of the record"""
    return pha_record_access(principal, record) \
        or full_control(principal, record)
  views = [measurement_list,
           immunization_list,
           allergy_list,
           medication_list,
           procedure_list,
           problem_list,
           equipment_list,
           vitals_list,
           lab_list,
           simple_clinical_notes_list,
           report_ccr,
           record_document_list,
           record_document_meta,
           record_specific_document,
           record_document_label,
           document_versions,
           document_create_by_rel,
           get_documents_by_rel,
           document_set_status,
           document_status_history,
           document_rels,
           document_carenets]
  AccessRule('Record Doc Access', record_doc_access, views)
  
  def record_doc_access_ext(principal, record, pha, **unused_args):
    """A user app with access to the record, with an id matching the app email in the URL."""
    return pha_record_access(principal, record) \
        and (principal.isSame(pha) or principal.proxied_by.isSame(pha))# Can't scope ext_ids to phas that aren't you
  views = [document_create_by_ext_id,
           document_create_by_rel_with_ext_id,
           document_version_by_ext_id,
           record_document_label_ext,
           record_document_meta_ext,
           ]
  AccessRule('Record Doc Access Ext', record_doc_access_ext, views)

  def record_admin_doc_access(principal, record, **unused_args):
    """A user app with access to the record, a principal in full control of the record, or the admin app that created the record."""
    return record_doc_access(principal, record) \
        or principal.createdRecord(record)  #special case: Admin Apps need to create docs
  views = [document_create,
           document_version]
  AccessRule('Record Admin Doc Access', record_admin_doc_access, views)
  
  def record_special_doc_access(principal, record, **unused_args):
    """A user app with access to the record, a principal in full control of the record, or the admin app that created the record."""
    return record_doc_access(principal, record) \
        or principal.createdRecord(record)
  views = [read_special_document, # should PHAs be able to do this?
           save_special_document]
  AccessRule('Record Special Doc Access', record_special_doc_access, views)

  def record_doc_sharing_access(principal, record, **unused_args):
    """A principal in full control of the record."""
    return full_control(principal, record)
  views = [document_set_nevershare,
           document_remove_nevershare]
  AccessRule('Record Doc Sharing Access', record_doc_sharing_access, views)

  def record_app_doc_access(principal, record, pha, **unused_args):
    """A user app with access to the record, with an id matching the app email in the URL."""
    return pha_record_app_access(principal, record, pha)
  views = [record_app_document_meta,
           record_app_document_meta_ext,
           record_app_document_list,
           record_app_specific_document,
           record_app_document_create,
           record_app_document_create_or_update_ext,
           record_app_document_label,
           record_app_document_delete]
  AccessRule('Record App Doc Access', record_app_doc_access, views)
  

  # NOTE: old system checked that there was no record passed in. We don't have to
  # do this because all of the views are known to be app-specific
  def app_doc_access(principal, pha, **unused_args):
    """A user app with an id matching the app email in the URL."""
    return pha_app_access(principal, pha)
  views = [app_document_meta,
           app_document_meta_ext,
           app_document_list,
           app_specific_document,
           app_document_create,
           app_document_create_or_update,
           app_document_create_or_update_ext,
           app_document_label,
           app_document_delete]
  AccessRule('App Doc Access', app_doc_access, views)

  # Audit-related views
  def audit_access(principal, record, **unused_args):
    """A principal in full control of the record, or a user app with access to the record."""
    return full_control(principal, record) \
        or pha_record_access(principal, record)
  views = [audit_record_view,
           audit_document_view,
           audit_function_view,
           audit_query]
  AccessRule('Audit Access', audit_access, views)

  # Autoshare-related views: should phas or admins be able to do this?
  def autoshare_permissions(principal, record, **unused_args):
    """A principal in full control of the record."""
    return full_control(principal, record)
  views = [autoshare_list,
           autoshare_list_bytype_all,
           autoshare_create,
           autoshare_delete,
           autoshare_revert] # IN OLD SYSTEM, unpermissioned
  AccessRule('Autoshare Permissions', autoshare_permissions, views)

load_access_rules()
