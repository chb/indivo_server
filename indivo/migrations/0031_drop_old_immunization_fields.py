# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Immunization.anatomic_surface'
        db.delete_column('indivo_immunization', 'anatomic_surface')

        # Deleting field 'Immunization.sequence'
        db.delete_column('indivo_immunization', 'sequence')

        # Deleting field 'Immunization.vaccine_type_type'
        db.delete_column('indivo_immunization', 'vaccine_type_type')

        # Deleting field 'Immunization.anatomic_surface_type'
        db.delete_column('indivo_immunization', 'anatomic_surface_type')

        # Deleting field 'Immunization.adverse_event'
        db.delete_column('indivo_immunization', 'adverse_event')

        # Deleting field 'Immunization.vaccine_manufacturer'
        db.delete_column('indivo_immunization', 'vaccine_manufacturer')

        # Deleting field 'Immunization.vaccine_type_abbrev'
        db.delete_column('indivo_immunization', 'vaccine_type_abbrev')

        # Deleting field 'Immunization.anatomic_surface_value'
        db.delete_column('indivo_immunization', 'anatomic_surface_value')

        # Deleting field 'Immunization.administered_by'
        db.delete_column('indivo_immunization', 'administered_by')

        # Deleting field 'Immunization.vaccine_type'
        db.delete_column('indivo_immunization', 'vaccine_type')

        # Deleting field 'Immunization.vaccine_lot'
        db.delete_column('indivo_immunization', 'vaccine_lot')

        # Deleting field 'Immunization.date_administered'
        db.delete_column('indivo_immunization', 'date_administered')

        # Deleting field 'Immunization.vaccine_type_value'
        db.delete_column('indivo_immunization', 'vaccine_type_value')

        # Deleting field 'Immunization.anatomic_surface_abbrev'
        db.delete_column('indivo_immunization', 'anatomic_surface_abbrev')

        # Deleting field 'Immunization.vaccine_expiration'
        db.delete_column('indivo_immunization', 'vaccine_expiration')


    def backwards(self, orm):
        
        # Adding field 'Immunization.anatomic_surface'
        db.add_column('indivo_immunization', 'anatomic_surface', self.gf('django.db.models.fields.CharField')(max_length=40, null=True), keep_default=False)

        # Adding field 'Immunization.sequence'
        db.add_column('indivo_immunization', 'sequence', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)

        # Adding field 'Immunization.vaccine_type_type'
        db.add_column('indivo_immunization', 'vaccine_type_type', self.gf('django.db.models.fields.CharField')(max_length=80, null=True), keep_default=False)

        # Adding field 'Immunization.anatomic_surface_type'
        db.add_column('indivo_immunization', 'anatomic_surface_type', self.gf('django.db.models.fields.CharField')(max_length=80, null=True), keep_default=False)

        # Adding field 'Immunization.adverse_event'
        db.add_column('indivo_immunization', 'adverse_event', self.gf('django.db.models.fields.CharField')(max_length=100, null=True), keep_default=False)

        # Adding field 'Immunization.vaccine_manufacturer'
        db.add_column('indivo_immunization', 'vaccine_manufacturer', self.gf('django.db.models.fields.CharField')(max_length=40, null=True), keep_default=False)

        # Adding field 'Immunization.vaccine_type_abbrev'
        db.add_column('indivo_immunization', 'vaccine_type_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20, null=True), keep_default=False)

        # Adding field 'Immunization.anatomic_surface_value'
        db.add_column('indivo_immunization', 'anatomic_surface_value', self.gf('django.db.models.fields.CharField')(max_length=20, null=True), keep_default=False)

        # Adding field 'Immunization.administered_by'
        db.add_column('indivo_immunization', 'administered_by', self.gf('django.db.models.fields.CharField')(max_length=40, null=True), keep_default=False)

        # Adding field 'Immunization.vaccine_type'
        db.add_column('indivo_immunization', 'vaccine_type', self.gf('django.db.models.fields.CharField')(max_length=200, null=True), keep_default=False)

        # Adding field 'Immunization.vaccine_lot'
        db.add_column('indivo_immunization', 'vaccine_lot', self.gf('django.db.models.fields.CharField')(max_length=20, null=True), keep_default=False)

        # Adding field 'Immunization.date_administered'
        db.add_column('indivo_immunization', 'date_administered', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Immunization.vaccine_type_value'
        db.add_column('indivo_immunization', 'vaccine_type_value', self.gf('django.db.models.fields.CharField')(max_length=40, null=True), keep_default=False)

        # Adding field 'Immunization.anatomic_surface_abbrev'
        db.add_column('indivo_immunization', 'anatomic_surface_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20, null=True), keep_default=False)

        # Adding field 'Immunization.vaccine_expiration'
        db.add_column('indivo_immunization', 'vaccine_expiration', self.gf('django.db.models.fields.DateField')(null=True), keep_default=False)


    models = {
        'indivo.accesstoken': {
            'Meta': {'object_name': 'AccessToken', '_ormbases': ['indivo.Principal']},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Account']", 'null': 'True'}),
            'carenet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Carenet']", 'null': 'True'}),
            'connect_auth_p': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expires_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'principal_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Principal']", 'unique': 'True', 'primary_key': 'True'}),
            'share': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.PHAShare']"}),
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
            'Meta': {'unique_together': "(('auth_system', 'account'), ('auth_system', 'username'))", 'object_name': 'AccountAuthSystem'},
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
        'indivo.accountfullshare': {
            'Meta': {'unique_together': "(('record', 'with_account'),)", 'object_name': 'AccountFullShare'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accountfullshare_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fullshares'", 'to': "orm['indivo.Record']"}),
            'role_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'with_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fullshares_to'", 'to': "orm['indivo.Account']"})
        },
        'indivo.allergy': {
            'Meta': {'object_name': 'Allergy', '_ormbases': ['indivo.Fact']},
            'allergic_reaction_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'allergic_reaction_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'allergic_reaction_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'category_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'category_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'category_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'drug_allergen_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'drug_allergen_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'drug_allergen_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'drug_class_allergen_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'drug_class_allergen_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'drug_class_allergen_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'food_allergen_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'food_allergen_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'food_allergen_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'severity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'severity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'severity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'indivo.allergyexclusion': {
            'Meta': {'object_name': 'AllergyExclusion', '_ormbases': ['indivo.Fact']},
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'name_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'indivo.audit': {
            'Meta': {'object_name': 'Audit'},
            'carenet_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'document_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'effective_principal_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'pha_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'proxied_by_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'record_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'req_domain': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'req_headers': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'req_ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True'}),
            'req_method': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'req_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'request_successful': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'resp_code': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'resp_headers': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'view_func': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
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
            'fqn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'nevershare': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'original': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'document_thread'", 'null': 'True', 'to': "orm['indivo.Document']"}),
            'pha': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pha_document'", 'null': 'True', 'to': "orm['indivo.PHA']"}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'null': 'True', 'to': "orm['indivo.Record']"}),
            'replaced_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'document_replaced'", 'null': 'True', 'to': "orm['indivo.Document']"}),
            'replaces': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Document']", 'null': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['indivo.StatusName']"}),
            'suppressed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'suppressed_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Principal']", 'null': 'True'})
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
            'internal_p': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
        'indivo.encounter': {
            'Meta': {'object_name': 'Encounter', '_ormbases': ['indivo.Fact']},
            'encounterType_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'encounterType_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'encounterType_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'endDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'facility_adr_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'facility_adr_country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'facility_adr_postalcode': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'facility_adr_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'facility_adr_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'facility_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'provider_adr_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_adr_country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_adr_postalcode': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'provider_adr_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_adr_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_bday': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'provider_dea_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True'}),
            'provider_ethnicity': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_gender': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_name_family': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_name_given': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_name_prefix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_name_suffix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_npi_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_preferred_language': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_race': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_tel_1_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'provider_tel_1_preferred_p': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'provider_tel_1_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'provider_tel_2_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'provider_tel_2_preferred_p': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'provider_tel_2_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'startDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
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
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Document']", 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Record']", 'null': 'True'})
        },
        'indivo.fill': {
            'Meta': {'object_name': 'Fill', '_ormbases': ['indivo.Fact']},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'dispenseDaysSupply': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'medication': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fulfillments'", 'null': 'True', 'to': "orm['indivo.Medication']"}),
            'pbm': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'pharmacy_adr_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'pharmacy_adr_country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'pharmacy_adr_postalcode': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'pharmacy_adr_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'pharmacy_adr_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'pharmacy_ncpdpid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'pharmacy_org': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_adr_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_adr_country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_adr_postalcode': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'provider_adr_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_adr_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_bday': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'provider_dea_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True'}),
            'provider_ethnicity': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_gender': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_name_family': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_name_given': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_name_prefix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_name_suffix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_npi_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_preferred_language': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_race': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provider_tel_1_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'provider_tel_1_preferred_p': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'provider_tel_1_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'provider_tel_2_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'provider_tel_2_preferred_p': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'provider_tel_2_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'quantityDispensed_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'quantityDispensed_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'indivo.immunization': {
            'Meta': {'object_name': 'Immunization', '_ormbases': ['indivo.Fact']},
            'administration_status_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'administration_status_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'administration_status_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'product_class_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'product_class_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'product_class_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'product_name_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'product_name_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'product_name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'refusal_reason_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'refusal_reason_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'refusal_reason_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
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
            'lab_type': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'non_critical_range_maximum': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'non_critical_range_minimum': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'normal_range_maximum': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'normal_range_minimum': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'})
        },
        'indivo.machineapp': {
            'Meta': {'object_name': 'MachineApp'},
            'app_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'consumer_key': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'indivo_version': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'principal_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Principal']", 'unique': 'True', 'primary_key': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'})
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
            'drugName_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'drugName_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'drugName_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'endDate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'frequency_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'frequency_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'instructions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provenance_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provenance_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'quantity_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'quantity_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'startDate': ('django.db.models.fields.DateField', [], {'null': 'True'})
        },
        'indivo.message': {
            'Meta': {'unique_together': "(('account', 'external_identifier', 'sender'),)", 'object_name': 'Message'},
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
            'Meta': {'unique_together': "(('nonce', 'oauth_type'),)", 'object_name': 'Nonce'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nonce': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'oauth_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
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
        'indivo.nouser': {
            'Meta': {'object_name': 'NoUser', '_ormbases': ['indivo.Principal']},
            'principal_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Principal']", 'unique': 'True', 'primary_key': 'True'})
        },
        'indivo.pha': {
            'Meta': {'object_name': 'PHA'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'autonomous_reason': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'callback_url': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'consumer_key': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'}),
            'frameable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_ui': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'icon_url': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'indivo_version': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'is_autonomous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'principal_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Principal']", 'unique': 'True', 'primary_key': 'True'}),
            'requirements': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'start_url_template': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'})
        },
        'indivo.phashare': {
            'Meta': {'unique_together': "(('record', 'with_pha'),)", 'object_name': 'PHAShare'},
            'authorized_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'authorized_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shares_authorized_by'", 'null': 'True', 'to': "orm['indivo.Account']"}),
            'carenet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Carenet']", 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'phashare_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pha_shares'", 'to': "orm['indivo.Record']"}),
            'with_pha': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pha_shares_to'", 'to': "orm['indivo.PHA']"})
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
            'endDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'name_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'startDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
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
            'share': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.PHAShare']", 'null': 'True'}),
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
