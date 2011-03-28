# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Principal'
        db.create_table('indivo_principal', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='principal_created_by', null=True, to=orm['indivo.Principal'])),
            ('email', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('indivo', ['Principal'])

        # Adding model 'Account'
        db.create_table('indivo_account', (
            ('account', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['indivo.Principal'], unique=True, primary_key=True)),
            ('primary_secret', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('secondary_secret', self.gf('django.db.models.fields.CharField')(max_length=8, null=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('contact_email', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('last_login_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('last_failed_login_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('total_login_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('failed_login_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('state', self.gf('django.db.models.fields.CharField')(default='uninitialized', max_length=50)),
            ('last_state_change', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('indivo', ['Account'])

        # Adding model 'AuthSystem'
        db.create_table('indivo_authsystem', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='authsystem_created_by', null=True, to=orm['indivo.Principal'])),
            ('short_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('internal_p', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('indivo', ['AuthSystem'])

        # Adding model 'AccountAuthSystem'
        db.create_table('indivo_accountauthsystem', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='accountauthsystem_created_by', null=True, to=orm['indivo.Principal'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='auth_systems', to=orm['indivo.Account'])),
            ('auth_system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.AuthSystem'])),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('auth_parameters', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True)),
            ('user_attributes', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True)),
        ))
        db.send_create_signal('indivo', ['AccountAuthSystem'])

        # Adding unique constraint on 'AccountAuthSystem', fields ['auth_system', 'username']
        db.create_unique('indivo_accountauthsystem', ['auth_system_id', 'username'])

        # Adding model 'Carenet'
        db.create_table('indivo_carenet', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='carenet_created_by', null=True, to=orm['indivo.Principal'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Record'])),
        ))
        db.send_create_signal('indivo', ['Carenet'])

        # Adding unique constraint on 'Carenet', fields ['name', 'record']
        db.create_unique('indivo_carenet', ['name', 'record_id'])

        # Adding model 'CarenetDocument'
        db.create_table('indivo_carenetdocument', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='carenetdocument_created_by', null=True, to=orm['indivo.Principal'])),
            ('carenet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Carenet'])),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Document'])),
            ('share_p', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('indivo', ['CarenetDocument'])

        # Adding unique constraint on 'CarenetDocument', fields ['carenet', 'document']
        db.create_unique('indivo_carenetdocument', ['carenet_id', 'document_id'])

        # Adding model 'CarenetPHA'
        db.create_table('indivo_carenetpha', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='carenetpha_created_by', null=True, to=orm['indivo.Principal'])),
            ('carenet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Carenet'])),
            ('pha', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.PHA'])),
        ))
        db.send_create_signal('indivo', ['CarenetPHA'])

        # Adding unique constraint on 'CarenetPHA', fields ['carenet', 'pha']
        db.create_unique('indivo_carenetpha', ['carenet_id', 'pha_id'])

        # Adding model 'CarenetAccount'
        db.create_table('indivo_carenetaccount', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='carenetaccount_created_by', null=True, to=orm['indivo.Principal'])),
            ('carenet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Carenet'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Account'])),
            ('can_write', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('indivo', ['CarenetAccount'])

        # Adding unique constraint on 'CarenetAccount', fields ['carenet', 'account']
        db.create_unique('indivo_carenetaccount', ['carenet_id', 'account_id'])

        # Adding model 'CarenetAutoshare'
        db.create_table('indivo_carenetautoshare', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='carenetautoshare_created_by', null=True, to=orm['indivo.Principal'])),
            ('carenet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Carenet'])),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Record'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.DocumentSchema'], null=True)),
        ))
        db.send_create_signal('indivo', ['CarenetAutoshare'])

        # Adding unique constraint on 'CarenetAutoshare', fields ['carenet', 'record', 'type']
        db.create_unique('indivo_carenetautoshare', ['carenet_id', 'record_id', 'type_id'])

        # Adding model 'Share'
        db.create_table('indivo_share', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='share_created_by', null=True, to=orm['indivo.Principal'])),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shares', to=orm['indivo.Record'])),
            ('with_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shares_to', null=True, to=orm['indivo.Account'])),
            ('with_pha', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shares_to', null=True, to=orm['indivo.PHA'])),
            ('authorized_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('authorized_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shares_authorized_by', null=True, to=orm['indivo.Account'])),
            ('carenet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Carenet'], null=True)),
            ('role_label', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal('indivo', ['Share'])

        # Adding unique constraint on 'Share', fields ['record', 'with_account']
        db.create_unique('indivo_share', ['record_id', 'with_account_id'])

        # Adding unique constraint on 'Share', fields ['record', 'with_pha']
        db.create_unique('indivo_share', ['record_id', 'with_pha_id'])

        # Adding model 'AccessToken'
        db.create_table('indivo_accesstoken', (
            ('principal_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['indivo.Principal'], unique=True, primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('token_secret', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('share', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Share'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Account'], null=True)),
            ('carenet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Carenet'], null=True)),
            ('expires_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('indivo', ['AccessToken'])

        # Adding model 'ReqToken'
        db.create_table('indivo_reqtoken', (
            ('principal_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['indivo.Principal'], unique=True, primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('token_secret', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('verifier', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('oauth_callback', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('pha', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.PHA'])),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Record'], null=True)),
            ('carenet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Carenet'], null=True)),
            ('authorized_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('authorized_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Account'], null=True)),
            ('share', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Share'], null=True)),
        ))
        db.send_create_signal('indivo', ['ReqToken'])

        # Adding model 'Message'
        db.create_table('indivo_message', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='message_created_by', null=True, to=orm['indivo.Principal'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Account'])),
            ('about_record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Record'], null=True)),
            ('external_identifier', self.gf('django.db.models.fields.CharField')(max_length=250, null=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='message_as_sender', to=orm['indivo.Principal'])),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='message_as_recipient', to=orm['indivo.Principal'])),
            ('severity', self.gf('django.db.models.fields.CharField')(default='low', max_length=100)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('body_type', self.gf('django.db.models.fields.CharField')(default='plaintext', max_length=100)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('received_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('read_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('archived_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('response_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='message_responses', null=True, to=orm['indivo.Message'])),
            ('num_attachments', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('indivo', ['Message'])

        # Adding model 'MessageAttachment'
        db.create_table('indivo_messageattachment', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='messageattachment_created_by', null=True, to=orm['indivo.Principal'])),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Message'])),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('saved_to_document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Document'], null=True)),
            ('attachment_num', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('indivo', ['MessageAttachment'])

        # Adding unique constraint on 'MessageAttachment', fields ['message', 'attachment_num']
        db.create_unique('indivo_messageattachment', ['message_id', 'attachment_num'])

        # Adding model 'Notification'
        db.create_table('indivo_notification', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notification_created_by', null=True, to=orm['indivo.Principal'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Account'])),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Record'], null=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications_sent_by', to=orm['indivo.Principal'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Document'], null=True)),
            ('app_url', self.gf('django.db.models.fields.CharField')(max_length=300, null=True)),
        ))
        db.send_create_signal('indivo', ['Notification'])

        # Adding model 'RecordNotificationRoute'
        db.create_table('indivo_recordnotificationroute', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recordnotificationroute_created_by', null=True, to=orm['indivo.Principal'])),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notification_routes', to=orm['indivo.Record'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Account'])),
        ))
        db.send_create_signal('indivo', ['RecordNotificationRoute'])

        # Adding unique constraint on 'RecordNotificationRoute', fields ['account', 'record']
        db.create_unique('indivo_recordnotificationroute', ['account_id', 'record_id'])

        # Adding model 'StatusName'
        db.create_table('indivo_statusname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=24)),
        ))
        db.send_create_signal('indivo', ['StatusName'])

        # Adding model 'DocumentStatusHistory'
        db.create_table('indivo_documentstatushistory', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='documentstatushistory_created_by', null=True, to=orm['indivo.Principal'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.StatusName'])),
            ('reason', self.gf('django.db.models.fields.TextField')()),
            ('document', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('record', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('proxied_by_principal', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('effective_principal', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal('indivo', ['DocumentStatusHistory'])

        # Adding model 'Record'
        db.create_table('indivo_record', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='record_created_by', null=True, to=orm['indivo.Principal'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='records_owned_by', null=True, to=orm['indivo.Principal'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=60, null=True)),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='the_record_for_contact', null=True, to=orm['indivo.Document'])),
            ('demographics', self.gf('django.db.models.fields.related.ForeignKey')(related_name='the_record_for_demographics', null=True, to=orm['indivo.Document'])),
        ))
        db.send_create_signal('indivo', ['Record'])

        # Adding model 'DocumentSchema'
        db.create_table('indivo_documentschema', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='documentschema_created_by', null=True, to=orm['indivo.Principal'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('stylesheet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stylesheet', null=True, to=orm['indivo.Document'])),
        ))
        db.send_create_signal('indivo', ['DocumentSchema'])

        # Adding model 'Document'
        db.create_table('indivo_document', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='document_created_by', null=True, to=orm['indivo.Principal'])),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='documents', null=True, to=orm['indivo.Record'])),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=250, null=True)),
            ('nevershare', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.DocumentSchema'], null=True)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True)),
            ('content_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('pha', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pha_document', null=True, to=orm['indivo.PHA'])),
            ('suppressed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('suppressed_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Principal'], null=True)),
            ('original', self.gf('django.db.models.fields.related.ForeignKey')(related_name='document_thread', null=True, to=orm['indivo.Document'])),
            ('replaced_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='document_replaced', null=True, to=orm['indivo.Document'])),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('digest', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['indivo.StatusName'])),
        ))
        db.send_create_signal('indivo', ['Document'])

        # Adding unique constraint on 'Document', fields ['record', 'external_id']
        db.create_unique('indivo_document', ['record_id', 'external_id'])

        # Adding model 'Nonce'
        db.create_table('indivo_nonce', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nonce', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('indivo', ['Nonce'])

        # Adding model 'PHA'
        db.create_table('indivo_pha', (
            ('principal_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['indivo.Principal'], unique=True, primary_key=True)),
            ('consumer_key', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('start_url_template', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('callback_url', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('is_autonomous', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('autonomous_reason', self.gf('django.db.models.fields.TextField')(null=True)),
            ('has_ui', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('frameable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('schema', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.DocumentSchema'], null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True)),
            ('privacy_tou', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('indivo', ['PHA'])

        # Adding model 'MachineApp'
        db.create_table('indivo_machineapp', (
            ('principal_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['indivo.Principal'], unique=True, primary_key=True)),
            ('consumer_key', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('app_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('indivo', ['MachineApp'])

        # Adding model 'SessionRequestToken'
        db.create_table('indivo_sessionrequesttoken', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sessionrequesttoken_created_by', null=True, to=orm['indivo.Principal'])),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Account'], null=True)),
            ('approved_p', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('indivo', ['SessionRequestToken'])

        # Adding model 'SessionToken'
        db.create_table('indivo_sessiontoken', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sessiontoken_created_by', null=True, to=orm['indivo.Principal'])),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.Account'], null=True)),
            ('expires_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('indivo', ['SessionToken'])

        # Adding model 'DocumentRels'
        db.create_table('indivo_documentrels', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_0', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rels_as_doc_0', to=orm['indivo.Document'])),
            ('document_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rels_as_doc_1', to=orm['indivo.Document'])),
            ('relationship', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['indivo.DocumentSchema'])),
        ))
        db.send_create_signal('indivo', ['DocumentRels'])

        # Adding model 'DocumentProcessing'
        db.create_table('indivo_documentprocessing', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='documentprocessing_created_by', null=True, to=orm['indivo.Principal'])),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(related_name='processed_doc', null=True, to=orm['indivo.Document'])),
        ))
        db.send_create_signal('indivo', ['DocumentProcessing'])

        # Adding model 'Audit'
        db.create_table('indivo_audit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('req_view_func', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('req_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('req_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('req_ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('req_domain', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('req_headers', self.gf('django.db.models.fields.TextField')()),
            ('req_method', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('record', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('document', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('resp_code', self.gf('django.db.models.fields.IntegerField')()),
            ('resp_error_msg', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('resp_server', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('resp_headers', self.gf('django.db.models.fields.TextField')()),
            ('req_effective_principal_email', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('req_proxied_by_principal_email', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal('indivo', ['Audit'])

        # Adding model 'Fact'
        db.create_table('indivo_fact', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(related_name='allergy', null=True, to=orm['indivo.Document'])),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='allergy', null=True, to=orm['indivo.Record'])),
        ))
        db.send_create_signal('indivo', ['Fact'])

        # Adding model 'Allergy'
        db.create_table('indivo_allergy', (
            ('fact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['indivo.Fact'], unique=True, primary_key=True)),
            ('date_diagnosed', self.gf('django.db.models.fields.DateField')(null=True)),
            ('diagnosed_by', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('allergen_type', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('allergen_type_type', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('allergen_type_value', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('allergen_type_abbrev', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('allergen_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('allergen_name_type', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('allergen_name_value', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('allergen_name_abbrev', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('reaction', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('specifics', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('indivo', ['Allergy'])

        # Adding model 'SimpleClinicalNote'
        db.create_table('indivo_simpleclinicalnote', (
            ('fact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['indivo.Fact'], unique=True, primary_key=True)),
            ('date_of_visit', self.gf('django.db.models.fields.DateTimeField')()),
            ('finalized_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('visit_type', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('visit_type_type', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('visit_type_value', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('visit_type_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('visit_location', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('specialty', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('specialty_type', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('specialty_value', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('specialty_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('signed_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('provider_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('provider_institution', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('chief_complaint', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('indivo', ['SimpleClinicalNote'])

        # Adding model 'Equipment'
        db.create_table('indivo_equipment', (
            ('fact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['indivo.Fact'], unique=True, primary_key=True)),
            ('date_started', self.gf('django.db.models.fields.DateField')(null=True)),
            ('date_stopped', self.gf('django.db.models.fields.DateField')(null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('vendor', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('indivo', ['Equipment'])

        # Adding model 'Measurement'
        db.create_table('indivo_measurement', (
            ('fact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['indivo.Fact'], unique=True, primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('indivo', ['Measurement'])

        # Adding model 'Immunization'
        db.create_table('indivo_immunization', (
            ('fact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['indivo.Fact'], unique=True, primary_key=True)),
            ('date_administered', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('administered_by', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('vaccine_type', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('vaccine_type_type', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('vaccine_type_value', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('vaccine_type_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('vaccine_manufacturer', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('vaccine_lot', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('vaccine_expiration', self.gf('django.db.models.fields.DateField')(null=True)),
            ('sequence', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('anatomic_surface', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('anatomic_surface_type', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('anatomic_surface_value', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('anatomic_surface_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('adverse_event', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal('indivo', ['Immunization'])

        # Adding model 'Lab'
        db.create_table('indivo_lab', (
            ('fact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['indivo.Fact'], unique=True, primary_key=True)),
            ('date_measured', self.gf('django.db.models.fields.DateTimeField')()),
            ('lab_name', self.gf('django.db.models.fields.CharField')(max_length=250, null=True)),
            ('lab_address', self.gf('django.db.models.fields.CharField')(max_length=250, null=True)),
            ('lab_type', self.gf('django.db.models.fields.CharField')(max_length=250, null=True)),
            ('lab_comments', self.gf('django.db.models.fields.TextField')(null=True)),
            ('first_panel_name', self.gf('django.db.models.fields.CharField')(max_length=250, null=True)),
            ('first_lab_test_name', self.gf('django.db.models.fields.CharField')(max_length=250, null=True)),
            ('first_lab_test_value', self.gf('django.db.models.fields.CharField')(max_length=250, null=True)),
        ))
        db.send_create_signal('indivo', ['Lab'])

        # Adding model 'Medication'
        db.create_table('indivo_medication', (
            ('fact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['indivo.Fact'], unique=True, primary_key=True)),
            ('date_started', self.gf('django.db.models.fields.DateField')(null=True)),
            ('date_stopped', self.gf('django.db.models.fields.DateField')(null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name_type', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('name_value', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('name_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('brand_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('brand_name_type', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('brand_name_value', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('brand_name_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('dose_textvalue', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('dose_value', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('dose_unit', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('dose_unit_type', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('dose_unit_value', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('dose_unit_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('route', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('route_type', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('route_value', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('route_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('strength_textvalue', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('strength_value', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('strength_unit', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('strength_unit_type', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('strength_unit_value', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('strength_unit_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('frequency_type', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('frequency_value', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('frequency_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('prescribed_by_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('prescribed_by_institution', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('prescribed_on', self.gf('django.db.models.fields.DateField')(null=True)),
            ('prescribed_stop_on', self.gf('django.db.models.fields.DateField')(null=True)),
            ('dispense_as_written', self.gf('django.db.models.fields.NullBooleanField')(null=True)),
            ('prescription_duration', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('prescription_refill_info', self.gf('django.db.models.fields.TextField')(null=True)),
            ('prescription_instructions', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('indivo', ['Medication'])

        # Adding model 'Problem'
        db.create_table('indivo_problem', (
            ('fact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['indivo.Fact'], unique=True, primary_key=True)),
            ('date_onset', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('date_resolution', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('name_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('name_value', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('name_abbrev', self.gf('django.db.models.fields.CharField')(max_length=24, null=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True)),
            ('diagnosed_by', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
        ))
        db.send_create_signal('indivo', ['Problem'])

        # Adding model 'Procedure'
        db.create_table('indivo_procedure', (
            ('fact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['indivo.Fact'], unique=True, primary_key=True)),
            ('date_performed', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_type', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('name_value', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('name_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('provider_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('provider_institution', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('indivo', ['Procedure'])

        # Adding model 'Vitals'
        db.create_table('indivo_vitals', (
            ('fact_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['indivo.Fact'], unique=True, primary_key=True)),
            ('date_measured', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_type', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('name_value', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('name_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('unit_type', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('unit_value', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('unit_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('site', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('indivo', ['Vitals'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Document', fields ['record', 'external_id']
        db.delete_unique('indivo_document', ['record_id', 'external_id'])

        # Removing unique constraint on 'RecordNotificationRoute', fields ['account', 'record']
        db.delete_unique('indivo_recordnotificationroute', ['account_id', 'record_id'])

        # Removing unique constraint on 'MessageAttachment', fields ['message', 'attachment_num']
        db.delete_unique('indivo_messageattachment', ['message_id', 'attachment_num'])

        # Removing unique constraint on 'Share', fields ['record', 'with_pha']
        db.delete_unique('indivo_share', ['record_id', 'with_pha_id'])

        # Removing unique constraint on 'Share', fields ['record', 'with_account']
        db.delete_unique('indivo_share', ['record_id', 'with_account_id'])

        # Removing unique constraint on 'CarenetAutoshare', fields ['carenet', 'record', 'type']
        db.delete_unique('indivo_carenetautoshare', ['carenet_id', 'record_id', 'type_id'])

        # Removing unique constraint on 'CarenetAccount', fields ['carenet', 'account']
        db.delete_unique('indivo_carenetaccount', ['carenet_id', 'account_id'])

        # Removing unique constraint on 'CarenetPHA', fields ['carenet', 'pha']
        db.delete_unique('indivo_carenetpha', ['carenet_id', 'pha_id'])

        # Removing unique constraint on 'CarenetDocument', fields ['carenet', 'document']
        db.delete_unique('indivo_carenetdocument', ['carenet_id', 'document_id'])

        # Removing unique constraint on 'Carenet', fields ['name', 'record']
        db.delete_unique('indivo_carenet', ['name', 'record_id'])

        # Removing unique constraint on 'AccountAuthSystem', fields ['auth_system', 'username']
        db.delete_unique('indivo_accountauthsystem', ['auth_system_id', 'username'])

        # Deleting model 'Principal'
        db.delete_table('indivo_principal')

        # Deleting model 'Account'
        db.delete_table('indivo_account')

        # Deleting model 'AuthSystem'
        db.delete_table('indivo_authsystem')

        # Deleting model 'AccountAuthSystem'
        db.delete_table('indivo_accountauthsystem')

        # Deleting model 'Carenet'
        db.delete_table('indivo_carenet')

        # Deleting model 'CarenetDocument'
        db.delete_table('indivo_carenetdocument')

        # Deleting model 'CarenetPHA'
        db.delete_table('indivo_carenetpha')

        # Deleting model 'CarenetAccount'
        db.delete_table('indivo_carenetaccount')

        # Deleting model 'CarenetAutoshare'
        db.delete_table('indivo_carenetautoshare')

        # Deleting model 'Share'
        db.delete_table('indivo_share')

        # Deleting model 'AccessToken'
        db.delete_table('indivo_accesstoken')

        # Deleting model 'ReqToken'
        db.delete_table('indivo_reqtoken')

        # Deleting model 'Message'
        db.delete_table('indivo_message')

        # Deleting model 'MessageAttachment'
        db.delete_table('indivo_messageattachment')

        # Deleting model 'Notification'
        db.delete_table('indivo_notification')

        # Deleting model 'RecordNotificationRoute'
        db.delete_table('indivo_recordnotificationroute')

        # Deleting model 'StatusName'
        db.delete_table('indivo_statusname')

        # Deleting model 'DocumentStatusHistory'
        db.delete_table('indivo_documentstatushistory')

        # Deleting model 'Record'
        db.delete_table('indivo_record')

        # Deleting model 'DocumentSchema'
        db.delete_table('indivo_documentschema')

        # Deleting model 'Document'
        db.delete_table('indivo_document')

        # Deleting model 'Nonce'
        db.delete_table('indivo_nonce')

        # Deleting model 'PHA'
        db.delete_table('indivo_pha')

        # Deleting model 'MachineApp'
        db.delete_table('indivo_machineapp')

        # Deleting model 'SessionRequestToken'
        db.delete_table('indivo_sessionrequesttoken')

        # Deleting model 'SessionToken'
        db.delete_table('indivo_sessiontoken')

        # Deleting model 'DocumentRels'
        db.delete_table('indivo_documentrels')

        # Deleting model 'DocumentProcessing'
        db.delete_table('indivo_documentprocessing')

        # Deleting model 'Audit'
        db.delete_table('indivo_audit')

        # Deleting model 'Fact'
        db.delete_table('indivo_fact')

        # Deleting model 'Allergy'
        db.delete_table('indivo_allergy')

        # Deleting model 'SimpleClinicalNote'
        db.delete_table('indivo_simpleclinicalnote')

        # Deleting model 'Equipment'
        db.delete_table('indivo_equipment')

        # Deleting model 'Measurement'
        db.delete_table('indivo_measurement')

        # Deleting model 'Immunization'
        db.delete_table('indivo_immunization')

        # Deleting model 'Lab'
        db.delete_table('indivo_lab')

        # Deleting model 'Medication'
        db.delete_table('indivo_medication')

        # Deleting model 'Problem'
        db.delete_table('indivo_problem')

        # Deleting model 'Procedure'
        db.delete_table('indivo_procedure')

        # Deleting model 'Vitals'
        db.delete_table('indivo_vitals')


    models = {
        'indivo.accesstoken': {
            'Meta': {'object_name': 'AccessToken', '_ormbases': ['indivo.Principal']},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Account']", 'null': 'True'}),
            'carenet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Carenet']", 'null': 'True'}),
            'expires_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'principal_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Principal']", 'unique': 'True', 'primary_key': 'True'}),
            'share': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Share']"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'token_secret': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'indivo.account': {
            'Meta': {'object_name': 'Account', '_ormbases': ['indivo.Principal']},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Principal']", 'unique': 'True', 'primary_key': 'True'}),
            'contact_email': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'failed_login_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'last_failed_login_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_login_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_state_change': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'primary_secret': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'secondary_secret': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'uninitialized'", 'max_length': '50'}),
            'total_login_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'indivo.accountauthsystem': {
            'Meta': {'unique_together': "(('auth_system', 'username'),)", 'object_name': 'AccountAuthSystem'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'auth_systems'", 'to': "orm['indivo.Account']"}),
            'auth_parameters': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'auth_system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.AuthSystem']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accountauthsystem_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user_attributes': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'indivo.allergy': {
            'Meta': {'object_name': 'Allergy', '_ormbases': ['indivo.Fact']},
            'allergen_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'allergen_name_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'allergen_name_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'allergen_name_value': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'allergen_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'allergen_type_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'allergen_type_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'allergen_type_value': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'date_diagnosed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'diagnosed_by': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'reaction': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'specifics': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'indivo.audit': {
            'Meta': {'object_name': 'Audit'},
            'document': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'record': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'req_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'req_domain': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'req_effective_principal_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'req_headers': ('django.db.models.fields.TextField', [], {}),
            'req_ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'req_method': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'req_proxied_by_principal_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'req_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'req_view_func': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'resp_code': ('django.db.models.fields.IntegerField', [], {}),
            'resp_error_msg': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'resp_headers': ('django.db.models.fields.TextField', [], {}),
            'resp_server': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'indivo.authsystem': {
            'Meta': {'object_name': 'AuthSystem'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'authsystem_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'internal_p': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'indivo.carenet': {
            'Meta': {'unique_together': "(('name', 'record'),)", 'object_name': 'Carenet'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'carenet_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Record']"})
        },
        'indivo.carenetaccount': {
            'Meta': {'unique_together': "(('carenet', 'account'),)", 'object_name': 'CarenetAccount'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Account']"}),
            'can_write': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'carenet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Carenet']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'carenetaccount_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        'indivo.carenetautoshare': {
            'Meta': {'unique_together': "(('carenet', 'record', 'type'),)", 'object_name': 'CarenetAutoshare'},
            'carenet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Carenet']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'carenetautoshare_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Record']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.DocumentSchema']", 'null': 'True'})
        },
        'indivo.carenetdocument': {
            'Meta': {'unique_together': "(('carenet', 'document'),)", 'object_name': 'CarenetDocument'},
            'carenet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Carenet']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'carenetdocument_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Document']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'share_p': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'indivo.carenetpha': {
            'Meta': {'unique_together': "(('carenet', 'pha'),)", 'object_name': 'CarenetPHA'},
            'carenet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Carenet']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'carenetpha_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'pha': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.PHA']"})
        },
        'indivo.document': {
            'Meta': {'unique_together': "(('record', 'external_id'),)", 'object_name': 'Document'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'content_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'document_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'nevershare': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'original': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'document_thread'", 'null': 'True', 'to': "orm['indivo.Document']"}),
            'pha': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pha_document'", 'null': 'True', 'to': "orm['indivo.PHA']"}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'null': 'True', 'to': "orm['indivo.Record']"}),
            'replaced_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'document_replaced'", 'null': 'True', 'to': "orm['indivo.Document']"}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['indivo.StatusName']"}),
            'suppressed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'suppressed_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Principal']", 'null': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.DocumentSchema']", 'null': 'True'})
        },
        'indivo.documentprocessing': {
            'Meta': {'object_name': 'DocumentProcessing'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documentprocessing_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'processed_doc'", 'null': 'True', 'to': "orm['indivo.Document']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        'indivo.documentrels': {
            'Meta': {'object_name': 'DocumentRels'},
            'document_0': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rels_as_doc_0'", 'to': "orm['indivo.Document']"}),
            'document_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rels_as_doc_1'", 'to': "orm['indivo.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.DocumentSchema']"})
        },
        'indivo.documentschema': {
            'Meta': {'object_name': 'DocumentSchema'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documentschema_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'stylesheet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stylesheet'", 'null': 'True', 'to': "orm['indivo.Document']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'indivo.documentstatushistory': {
            'Meta': {'object_name': 'DocumentStatusHistory'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documentstatushistory_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'document': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'effective_principal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'proxied_by_principal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {}),
            'record': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.StatusName']"})
        },
        'indivo.equipment': {
            'Meta': {'object_name': 'Equipment', '_ormbases': ['indivo.Fact']},
            'date_started': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'date_stopped': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'})
        },
        'indivo.fact': {
            'Meta': {'object_name': 'Fact'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'allergy'", 'null': 'True', 'to': "orm['indivo.Document']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'allergy'", 'null': 'True', 'to': "orm['indivo.Record']"})
        },
        'indivo.immunization': {
            'Meta': {'object_name': 'Immunization', '_ormbases': ['indivo.Fact']},
            'administered_by': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'adverse_event': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'anatomic_surface': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'anatomic_surface_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'anatomic_surface_type': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'anatomic_surface_value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'date_administered': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'vaccine_expiration': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'vaccine_lot': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'vaccine_manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'vaccine_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'vaccine_type_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'vaccine_type_type': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'vaccine_type_value': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'})
        },
        'indivo.lab': {
            'Meta': {'object_name': 'Lab', '_ormbases': ['indivo.Fact']},
            'date_measured': ('django.db.models.fields.DateTimeField', [], {}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'first_lab_test_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'first_lab_test_value': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'first_panel_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'lab_address': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'lab_comments': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'lab_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'lab_type': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'})
        },
        'indivo.machineapp': {
            'Meta': {'object_name': 'MachineApp'},
            'app_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'consumer_key': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'principal_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Principal']", 'unique': 'True', 'primary_key': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'indivo.measurement': {
            'Meta': {'object_name': 'Measurement', '_ormbases': ['indivo.Fact']},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'indivo.medication': {
            'Meta': {'object_name': 'Medication', '_ormbases': ['indivo.Fact']},
            'brand_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'brand_name_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'brand_name_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'brand_name_value': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'date_started': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'date_stopped': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'dispense_as_written': ('django.db.models.fields.NullBooleanField', [], {'null': 'True'}),
            'dose_textvalue': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'dose_unit': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'dose_unit_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'dose_unit_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'dose_unit_value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'dose_value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'frequency_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'frequency_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'frequency_value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'name_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'name_value': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'prescribed_by_institution': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'prescribed_by_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'prescribed_on': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'prescribed_stop_on': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'prescription_duration': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'prescription_instructions': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'prescription_refill_info': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'route': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'route_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'route_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'route_value': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'strength_textvalue': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'strength_unit': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'strength_unit_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'strength_unit_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'strength_unit_value': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'strength_value': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        'indivo.message': {
            'Meta': {'object_name': 'Message'},
            'about_record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Record']", 'null': 'True'}),
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Account']"}),
            'archived_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'body_type': ('django.db.models.fields.CharField', [], {'default': "'plaintext'", 'max_length': '100'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'message_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'external_identifier': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'num_attachments': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'read_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'received_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'message_as_recipient'", 'to': "orm['indivo.Principal']"}),
            'response_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'message_responses'", 'null': 'True', 'to': "orm['indivo.Message']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'message_as_sender'", 'to': "orm['indivo.Principal']"}),
            'severity': ('django.db.models.fields.CharField', [], {'default': "'low'", 'max_length': '100'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'indivo.messageattachment': {
            'Meta': {'unique_together': "(('message', 'attachment_num'),)", 'object_name': 'MessageAttachment'},
            'attachment_num': ('django.db.models.fields.IntegerField', [], {}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'messageattachment_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Message']"}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'saved_to_document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Document']", 'null': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'indivo.nonce': {
            'Meta': {'object_name': 'Nonce'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nonce': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'indivo.notification': {
            'Meta': {'object_name': 'Notification'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Account']"}),
            'app_url': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Document']", 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Record']", 'null': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications_sent_by'", 'to': "orm['indivo.Principal']"})
        },
        'indivo.pha': {
            'Meta': {'object_name': 'PHA'},
            'autonomous_reason': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'callback_url': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'consumer_key': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'frameable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_ui': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_autonomous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'principal_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Principal']", 'unique': 'True', 'primary_key': True}),
            'privacy_tou': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'schema': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.DocumentSchema']", 'null': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'start_url_template': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'indivo.principal': {
            'Meta': {'object_name': 'Principal'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'principal_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'indivo.problem': {
            'Meta': {'object_name': 'Problem', '_ormbases': ['indivo.Fact']},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'date_onset': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_resolution': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'diagnosed_by': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True'}),
            'name_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name_value': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'})
        },
        'indivo.procedure': {
            'Meta': {'object_name': 'Procedure', '_ormbases': ['indivo.Fact']},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'date_performed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'name_type': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'name_value': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'provider_institution': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'provider_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        'indivo.record': {
            'Meta': {'object_name': 'Record'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'the_record_for_contact'", 'null': 'True', 'to': "orm['indivo.Document']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'record_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'demographics': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'the_record_for_demographics'", 'null': 'True', 'to': "orm['indivo.Document']"}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'records_owned_by'", 'null': 'True', 'to': "orm['indivo.Principal']"})
        },
        'indivo.recordnotificationroute': {
            'Meta': {'unique_together': "(('account', 'record'),)", 'object_name': 'RecordNotificationRoute'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Account']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recordnotificationroute_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification_routes'", 'to': "orm['indivo.Record']"})
        },
        'indivo.reqtoken': {
            'Meta': {'object_name': 'ReqToken', '_ormbases': ['indivo.Principal']},
            'authorized_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'authorized_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Account']", 'null': 'True'}),
            'carenet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Carenet']", 'null': 'True'}),
            'oauth_callback': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'pha': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.PHA']"}),
            'principal_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Principal']", 'unique': 'True', 'primary_key': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Record']", 'null': 'True'}),
            'share': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Share']", 'null': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'token_secret': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'verifier': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'indivo.sessionrequesttoken': {
            'Meta': {'object_name': 'SessionRequestToken'},
            'approved_p': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessionrequesttoken_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Account']", 'null': 'True'})
        },
        'indivo.sessiontoken': {
            'Meta': {'object_name': 'SessionToken'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessiontoken_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'expires_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Account']", 'null': 'True'})
        },
        'indivo.share': {
            'Meta': {'unique_together': "(('record', 'with_account'), ('record', 'with_pha'))", 'object_name': 'Share'},
            'authorized_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'authorized_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shares_authorized_by'", 'null': 'True', 'to': "orm['indivo.Account']"}),
            'carenet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Carenet']", 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'share_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shares'", 'to': "orm['indivo.Record']"}),
            'role_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'with_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shares_to'", 'null': 'True', 'to': "orm['indivo.Account']"}),
            'with_pha': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shares_to'", 'null': 'True', 'to': "orm['indivo.PHA']"})
        },
        'indivo.simpleclinicalnote': {
            'Meta': {'object_name': 'SimpleClinicalNote', '_ormbases': ['indivo.Fact']},
            'chief_complaint': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'date_of_visit': ('django.db.models.fields.DateTimeField', [], {}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'finalized_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'provider_institution': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'provider_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'signed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'specialty': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'specialty_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'specialty_type': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'specialty_value': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'visit_location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'visit_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'visit_type_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'visit_type_type': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'visit_type_value': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'})
        },
        'indivo.statusname': {
            'Meta': {'object_name': 'StatusName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '24'})
        },
        'indivo.vitals': {
            'Meta': {'object_name': 'Vitals', '_ormbases': ['indivo.Fact']},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'date_measured': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'name_type': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'name_value': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unit_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'unit_type': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'unit_value': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['indivo']
