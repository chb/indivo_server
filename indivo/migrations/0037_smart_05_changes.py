# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        
        # Adding field 'Encounter.type_provenance_source_code'
        db.add_column('indivo_encounter', 'type_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='type_prov_sc', blank=True), keep_default=False)

        # Adding field 'Encounter.type_provenance_translation_fidelity_identifier'
        db.add_column('indivo_encounter', 'type_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='type_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Encounter.type_provenance_translation_fidelity_system'
        db.add_column('indivo_encounter', 'type_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='type_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Encounter.type_provenance_translation_fidelity_title'
        db.add_column('indivo_encounter', 'type_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='type_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Encounter.type_provenance_title'
        db.add_column('indivo_encounter', 'type_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='type_prov_title', blank=True), keep_default=False)


        db.rename_column('indivo_encounter', 'encounterType_identifier', 'type_code_id')
        db.rename_column('indivo_encounter', 'encounterType_system', 'type_code_sys')
        db.rename_column('indivo_encounter', 'encounterType_title', 'type_code_title')
        # Adding field 'Encounter.type_title'
        db.add_column('indivo_encounter', 'type_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='type_title', blank=True), keep_default=False)

        
        
        # Deleting field 'Immunization.administration_status_system'
        db.rename_column('indivo_immunization', 'administration_status_system', 'administration_status_code_sys')
        db.rename_column('indivo_immunization', 'administration_status_identifier', 'administration_status_code_id')
        db.rename_column('indivo_immunization', 'administration_status_title', 'administration_status_code_title')
        db.add_column('indivo_immunization', 'administration_status_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        

        # Deleting field 'Immunization.product_class_identifier'
        db.rename_column('indivo_immunization', 'product_class_identifier', 'product_class_code_id')
        db.rename_column('indivo_immunization', 'product_class_system', 'product_class_code_sys')
        db.rename_column('indivo_immunization', 'product_class_title', 'product_class_code_title')
        db.add_column('indivo_immunization', 'product_class_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Deleting field 'Immunization.product_class_2_system'
        db.rename_column('indivo_immunization', 'product_class_2_system', 'product_class_2_code_sys')
        db.rename_column('indivo_immunization', 'product_class_2_identifier', 'product_class_2_code_id')
        db.rename_column('indivo_immunization', 'product_class_2_title', 'product_class_2_code_title')
        db.add_column('indivo_immunization', 'product_class_2_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Deleting field 'Immunization.product_name_identifier'
        db.rename_column('indivo_immunization', 'product_name_identifier', 'product_name_code_id')
        db.rename_column('indivo_immunization', 'product_name_system', 'product_name_code_sys')
        db.rename_column('indivo_immunization', 'product_name_title', 'product_name_code_title')
        db.add_column('indivo_immunization', 'product_name_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Deleting field 'Immunization.refusal_reason_system'
        db.rename_column('indivo_immunization', 'refusal_reason_system', 'refusal_reason_code_sys')
        db.rename_column('indivo_immunization', 'refusal_reason_identifier', 'refusal_reason_code_id')
        db.rename_column('indivo_immunization', 'refusal_reason_title', 'refusal_reason_code_title')
        db.add_column('indivo_immunization', 'refusal_reason_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        
        # Adding field 'Immunization.product_class_provenance_source_code'
        db.add_column('indivo_immunization', 'product_class_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='product_class_prov_sc', blank=True), keep_default=False)

        # Adding field 'Immunization.product_class_provenance_translation_fidelity_identifier'
        db.add_column('indivo_immunization', 'product_class_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='product_class_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Immunization.product_class_provenance_translation_fidelity_system'
        db.add_column('indivo_immunization', 'product_class_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='product_class_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Immunization.product_class_provenance_translation_fidelity_title'
        db.add_column('indivo_immunization', 'product_class_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='product_class_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Immunization.product_class_provenance_title'
        db.add_column('indivo_immunization', 'product_class_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='product_class_prov_title', blank=True), keep_default=False)

        
        
        
        # Adding field 'Immunization.product_class_2_provenance_source_code'
        db.add_column('indivo_immunization', 'product_class_2_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='product_class_2_prov_sc', blank=True), keep_default=False)

        # Adding field 'Immunization.product_class_2_provenance_translation_fidelity_identifier'
        db.add_column('indivo_immunization', 'product_class_2_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='product_class_2_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Immunization.product_class_2_provenance_translation_fidelity_system'
        db.add_column('indivo_immunization', 'product_class_2_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='product_class_2_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Immunization.product_class_2_provenance_translation_fidelity_title'
        db.add_column('indivo_immunization', 'product_class_2_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='product_class_2_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Immunization.product_class_2_provenance_title'
        db.add_column('indivo_immunization', 'product_class_2_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='product_class_2_prov_title', blank=True), keep_default=False)

        
       

        # Adding field 'Immunization.refusal_reason_provenance_source_code'
        db.add_column('indivo_immunization', 'refusal_reason_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='refusal_reason_prov_sc', blank=True), keep_default=False)

        # Adding field 'Immunization.refusal_reason_provenance_translation_fidelity_identifier'
        db.add_column('indivo_immunization', 'refusal_reason_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='refusal_reason_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Immunization.refusal_reason_provenance_translation_fidelity_system'
        db.add_column('indivo_immunization', 'refusal_reason_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='refusal_reason_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Immunization.refusal_reason_provenance_translation_fidelity_title'
        db.add_column('indivo_immunization', 'refusal_reason_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='refusal_reason_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Immunization.refusal_reason_provenance_title'
        db.add_column('indivo_immunization', 'refusal_reason_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='refusal_reason_prov_title', blank=True), keep_default=False)

       
        
      
        # Adding field 'Immunization.administration_status_provenance_source_code'
        db.add_column('indivo_immunization', 'administration_status_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='administration_status_prov_sc', blank=True), keep_default=False)

        # Adding field 'Immunization.administration_status_provenance_translation_fidelity_identifier'
        db.add_column('indivo_immunization', 'administration_status_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='administration_status_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Immunization.administration_status_provenance_translation_fidelity_system'
        db.add_column('indivo_immunization', 'administration_status_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='administration_status_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Immunization.administration_status_provenance_translation_fidelity_title'
        db.add_column('indivo_immunization', 'administration_status_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='administration_status_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Immunization.administration_status_provenance_title'
        db.add_column('indivo_immunization', 'administration_status_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='administration_status_prov_title', blank=True), keep_default=False)

       

        
        # Adding field 'Immunization.product_name_provenance_source_code'
        db.add_column('indivo_immunization', 'product_name_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='product_name_prov_sc', blank=True), keep_default=False)

        # Adding field 'Immunization.product_name_provenance_translation_fidelity_identifier'
        db.add_column('indivo_immunization', 'product_name_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='product_name_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Immunization.product_name_provenance_translation_fidelity_system'
        db.add_column('indivo_immunization', 'product_name_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='product_name_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Immunization.product_name_provenance_translation_fidelity_title'
        db.add_column('indivo_immunization', 'product_name_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='product_name_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Immunization.product_name_provenance_title'
        db.add_column('indivo_immunization', 'product_name_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='product_name_prov_title', blank=True), keep_default=False)

       

        
        
        db.rename_column('indivo_problem', 'name_identifier', 'name_code_id')
        db.rename_column('indivo_problem', 'name_system', 'name_code_sys')
        db.rename_column('indivo_problem', 'name_title', 'name_code_title')
        db.add_column('indivo_problem', 'name_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        

        # Adding field 'Problem.name_provenance_source_code'
        db.add_column('indivo_problem', 'name_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_sc', blank=True), keep_default=False)

        # Adding field 'Problem.name_provenance_translation_fidelity_identifier'
        db.add_column('indivo_problem', 'name_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Problem.name_provenance_translation_fidelity_system'
        db.add_column('indivo_problem', 'name_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Problem.name_provenance_translation_fidelity_title'
        db.add_column('indivo_problem', 'name_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Problem.name_provenance_title'
        db.add_column('indivo_problem', 'name_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_title', blank=True), keep_default=False)

        

        # Deleting field 'VitalSigns.heart_rate_name_system'
        db.rename_column('indivo_vitalsigns', 'heart_rate_name_identifier', 'heart_rate_name_code_id')
        db.rename_column('indivo_vitalsigns', 'heart_rate_name_system', 'heart_rate_name_code_sys')
        db.rename_column('indivo_vitalsigns', 'heart_rate_name_title', 'heart_rate_name_code_title')
        db.add_column('indivo_vitalsigns', 'heart_rate_name_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Deleting field 'VitalSigns.oxygen_saturation_name_system'
        db.rename_column('indivo_vitalsigns', 'oxygen_saturation_name_identifier', 'oxygen_saturation_name_code_id')
        db.rename_column('indivo_vitalsigns', 'oxygen_saturation_name_system', 'oxygen_saturation_name_code_sys')
        db.rename_column('indivo_vitalsigns', 'oxygen_saturation_name_title', 'oxygen_saturation_name_code_title')
        db.add_column('indivo_vitalsigns', 'oxygen_saturation_name_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Deleting field 'VitalSigns.temperature_name_system'
        db.rename_column('indivo_vitalsigns', 'temperature_name_identifier', 'temperature_name_code_id')
        db.rename_column('indivo_vitalsigns', 'temperature_name_system', 'temperature_name_code_sys')
        db.rename_column('indivo_vitalsigns', 'temperature_name_title', 'temperature_name_code_title')
        db.add_column('indivo_vitalsigns', 'temperature_name_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Deleting field 'VitalSigns.bp_systolic_name_system'
        db.rename_column('indivo_vitalsigns', 'bp_systolic_name_identifier', 'bp_systolic_name_code_id')
        db.rename_column('indivo_vitalsigns', 'bp_systolic_name_system', 'bp_systolic_name_code_sys')
        db.rename_column('indivo_vitalsigns', 'bp_systolic_name_title', 'bp_systolic_name_code_title')
        db.add_column('indivo_vitalsigns', 'bp_systolic_name_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Deleting field 'VitalSigns.bp_diastolic_name_identifier'
        db.rename_column('indivo_vitalsigns', 'bp_diastolic_name_identifier', 'bp_diastolic_name_code_id')
        db.rename_column('indivo_vitalsigns', 'bp_diastolic_name_system', 'bp_diastolic_name_code_sys')
        db.rename_column('indivo_vitalsigns', 'bp_diastolic_name_title', 'bp_diastolic_name_code_title')
        db.add_column('indivo_vitalsigns', 'bp_diastolic_name_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Deleting field 'VitalSigns.height_name_system'
        db.rename_column('indivo_vitalsigns', 'height_name_identifier', 'height_name_code_id')
        db.rename_column('indivo_vitalsigns', 'height_name_system', 'height_name_code_sys')
        db.rename_column('indivo_vitalsigns', 'height_name_title', 'height_name_code_title')
        db.add_column('indivo_vitalsigns', 'height_name_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Deleting field 'VitalSigns.bmi_name_system'
        db.rename_column('indivo_vitalsigns', 'bmi_name_identifier', 'bmi_name_code_id')
        db.rename_column('indivo_vitalsigns', 'bmi_name_system', 'bmi_name_code_sys')
        db.rename_column('indivo_vitalsigns', 'bmi_name_title', 'bmi_name_code_title')
        db.add_column('indivo_vitalsigns', 'bmi_name_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

       
        # Deleting field 'VitalSigns.respiratory_rate_name_identifier'
        db.rename_column('indivo_vitalsigns', 'respiratory_rate_name_identifier', 'respiratory_rate_name_code_id')
        db.rename_column('indivo_vitalsigns', 'respiratory_rate_name_system', 'respiratory_rate_name_code_sys')
        db.rename_column('indivo_vitalsigns', 'respiratory_rate_name_title', 'respiratory_rate_name_code_title')
        db.add_column('indivo_vitalsigns', 'respiratory_rate_name_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Deleting field 'VitalSigns.bp_position_identifier'
        db.rename_column('indivo_vitalsigns', 'bp_position_identifier', 'bp_position_code_id')
        db.rename_column('indivo_vitalsigns', 'bp_position_system', 'bp_position_code_sys')
        db.rename_column('indivo_vitalsigns', 'bp_position_title', 'bp_position_code_title')
        db.add_column('indivo_vitalsigns', 'bp_position_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
                
        # Deleting field 'VitalSigns.bp_method_identifier'
        db.rename_column('indivo_vitalsigns', 'bp_method_identifier', 'bp_method_code_id')
        db.rename_column('indivo_vitalsigns', 'bp_method_system', 'bp_method_code_sys')
        db.rename_column('indivo_vitalsigns', 'bp_method_title', 'bp_method_code_title')
        db.add_column('indivo_vitalsigns', 'bp_method_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        
        db.rename_column('indivo_vitalsigns', 'bp_site_identifier', 'bp_site_code_id')
        db.rename_column('indivo_vitalsigns', 'bp_site_system', 'bp_site_code_sys')
        db.rename_column('indivo_vitalsigns', 'bp_site_title', 'bp_site_code_title')
        db.add_column('indivo_vitalsigns', 'bp_site_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Deleting field 'VitalSigns.weight_name_system'
        db.rename_column('indivo_vitalsigns', 'weight_name_identifier', 'weight_name_code_id')
        db.rename_column('indivo_vitalsigns', 'weight_name_system', 'weight_name_code_sys')
        db.rename_column('indivo_vitalsigns', 'weight_name_title', 'weight_name_code_title')
        db.add_column('indivo_vitalsigns', 'weight_name_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)


        # Adding field 'VitalSigns.temperature_name_provenance_source_code'
        db.add_column('indivo_vitalsigns', 'temperature_name_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='temperature_name_prov_sc', blank=True), keep_default=False)

        # Adding field 'VitalSigns.temperature_name_provenance_translation_fidelity_identifier'
        db.add_column('indivo_vitalsigns', 'temperature_name_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='temperature_name_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'VitalSigns.temperature_name_provenance_translation_fidelity_system'
        db.add_column('indivo_vitalsigns', 'temperature_name_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='temperature_name_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'VitalSigns.temperature_name_provenance_translation_fidelity_title'
        db.add_column('indivo_vitalsigns', 'temperature_name_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='temperature_name_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'VitalSigns.temperature_name_provenance_title'
        db.add_column('indivo_vitalsigns', 'temperature_name_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='temperature_name_prov_title', blank=True), keep_default=False)

       
        # Adding field 'VitalSigns.weight_name_provenance_source_code'
        db.add_column('indivo_vitalsigns', 'weight_name_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='weight_name_prov_sc', blank=True), keep_default=False)

        # Adding field 'VitalSigns.weight_name_provenance_translation_fidelity_identifier'
        db.add_column('indivo_vitalsigns', 'weight_name_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='weight_name_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'VitalSigns.weight_name_provenance_translation_fidelity_system'
        db.add_column('indivo_vitalsigns', 'weight_name_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='weight_name_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'VitalSigns.weight_name_provenance_translation_fidelity_title'
        db.add_column('indivo_vitalsigns', 'weight_name_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='weight_name_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'VitalSigns.weight_name_provenance_title'
        db.add_column('indivo_vitalsigns', 'weight_name_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='weight_name_prov_title', blank=True), keep_default=False)

        
        # Adding field 'VitalSigns.oxygen_saturation_name_provenance_source_code'
        db.add_column('indivo_vitalsigns', 'oxygen_saturation_name_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='oxygen_saturation_name_prov_sc', blank=True), keep_default=False)

        # Adding field 'VitalSigns.oxygen_saturation_name_provenance_translation_fidelity_identifier'
        db.add_column('indivo_vitalsigns', 'oxygen_saturation_name_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='oxygen_saturation_name_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'VitalSigns.oxygen_saturation_name_provenance_translation_fidelity_system'
        db.add_column('indivo_vitalsigns', 'oxygen_saturation_name_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='oxygen_saturation_name_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'VitalSigns.oxygen_saturation_name_provenance_translation_fidelity_title'
        db.add_column('indivo_vitalsigns', 'oxygen_saturation_name_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='oxygen_saturation_name_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'VitalSigns.oxygen_saturation_name_provenance_title'
        db.add_column('indivo_vitalsigns', 'oxygen_saturation_name_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='oxygen_saturation_name_prov_title', blank=True), keep_default=False)

        
        # Adding field 'VitalSigns.bmi_name_provenance_source_code'
        db.add_column('indivo_vitalsigns', 'bmi_name_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bmi_name_prov_sc', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bmi_name_provenance_translation_fidelity_identifier'
        db.add_column('indivo_vitalsigns', 'bmi_name_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bmi_name_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bmi_name_provenance_translation_fidelity_system'
        db.add_column('indivo_vitalsigns', 'bmi_name_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bmi_name_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bmi_name_provenance_translation_fidelity_title'
        db.add_column('indivo_vitalsigns', 'bmi_name_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bmi_name_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bmi_name_provenance_title'
        db.add_column('indivo_vitalsigns', 'bmi_name_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bmi_name_prov_title', blank=True), keep_default=False)

        
        # Adding field 'VitalSigns.respiratory_rate_name_provenance_source_code'
        db.add_column('indivo_vitalsigns', 'respiratory_rate_name_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='respiratory_rate_name_prov_sc', blank=True), keep_default=False)

        # Adding field 'VitalSigns.respiratory_rate_name_provenance_translation_fidelity_identifier'
        db.add_column('indivo_vitalsigns', 'respiratory_rate_name_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='respiratory_rate_name_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'VitalSigns.respiratory_rate_name_provenance_translation_fidelity_system'
        db.add_column('indivo_vitalsigns', 'respiratory_rate_name_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='respiratory_rate_name_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'VitalSigns.respiratory_rate_name_provenance_translation_fidelity_title'
        db.add_column('indivo_vitalsigns', 'respiratory_rate_name_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='respiratory_rate_name_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'VitalSigns.respiratory_rate_name_provenance_title'
        db.add_column('indivo_vitalsigns', 'respiratory_rate_name_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='respiratory_rate_name_prov_title', blank=True), keep_default=False)

        
        # Adding field 'VitalSigns.height_name_provenance_source_code'
        db.add_column('indivo_vitalsigns', 'height_name_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='height_name_prov_sc', blank=True), keep_default=False)

        # Adding field 'VitalSigns.height_name_provenance_translation_fidelity_identifier'
        db.add_column('indivo_vitalsigns', 'height_name_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='height_name_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'VitalSigns.height_name_provenance_translation_fidelity_system'
        db.add_column('indivo_vitalsigns', 'height_name_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='height_name_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'VitalSigns.height_name_provenance_translation_fidelity_title'
        db.add_column('indivo_vitalsigns', 'height_name_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='height_name_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'VitalSigns.height_name_provenance_title'
        db.add_column('indivo_vitalsigns', 'height_name_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='height_name_prov_title', blank=True), keep_default=False)

        
        # Adding field 'VitalSigns.heart_rate_name_provenance_source_code'
        db.add_column('indivo_vitalsigns', 'heart_rate_name_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='heart_rate_name_prov_sc', blank=True), keep_default=False)

        # Adding field 'VitalSigns.heart_rate_name_provenance_translation_fidelity_identifier'
        db.add_column('indivo_vitalsigns', 'heart_rate_name_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='heart_rate_name_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'VitalSigns.heart_rate_name_provenance_translation_fidelity_system'
        db.add_column('indivo_vitalsigns', 'heart_rate_name_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='heart_rate_name_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'VitalSigns.heart_rate_name_provenance_translation_fidelity_title'
        db.add_column('indivo_vitalsigns', 'heart_rate_name_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='heart_rate_name_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'VitalSigns.heart_rate_name_provenance_title'
        db.add_column('indivo_vitalsigns', 'heart_rate_name_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='heart_rate_name_prov_title', blank=True), keep_default=False)

       
        # Adding field 'VitalSigns.bp_position_provenance_source_code'
        db.add_column('indivo_vitalsigns', 'bp_position_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_position_prov_sc', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_position_provenance_translation_fidelity_identifier'
        db.add_column('indivo_vitalsigns', 'bp_position_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_position_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_position_provenance_translation_fidelity_system'
        db.add_column('indivo_vitalsigns', 'bp_position_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_position_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_position_provenance_translation_fidelity_title'
        db.add_column('indivo_vitalsigns', 'bp_position_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_position_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_position_provenance_title'
        db.add_column('indivo_vitalsigns', 'bp_position_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_position_prov_title', blank=True), keep_default=False)

        
        # Adding field 'VitalSigns.bp_diastolic_name_provenance_source_code'
        db.add_column('indivo_vitalsigns', 'bp_diastolic_name_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_diastolic_name_prov_sc', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_diastolic_name_provenance_translation_fidelity_identifier'
        db.add_column('indivo_vitalsigns', 'bp_diastolic_name_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_diastolic_name_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_diastolic_name_provenance_translation_fidelity_system'
        db.add_column('indivo_vitalsigns', 'bp_diastolic_name_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_diastolic_name_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_diastolic_name_provenance_translation_fidelity_title'
        db.add_column('indivo_vitalsigns', 'bp_diastolic_name_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_diastolic_name_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_diastolic_name_provenance_title'
        db.add_column('indivo_vitalsigns', 'bp_diastolic_name_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_diastolic_name_prov_title', blank=True), keep_default=False)

        
        # Adding field 'VitalSigns.bp_systolic_name_provenance_source_code'
        db.add_column('indivo_vitalsigns', 'bp_systolic_name_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_systolic_name_prov_sc', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_systolic_name_provenance_translation_fidelity_identifier'
        db.add_column('indivo_vitalsigns', 'bp_systolic_name_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_systolic_name_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_systolic_name_provenance_translation_fidelity_system'
        db.add_column('indivo_vitalsigns', 'bp_systolic_name_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_systolic_name_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_systolic_name_provenance_translation_fidelity_title'
        db.add_column('indivo_vitalsigns', 'bp_systolic_name_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_systolic_name_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_systolic_name_provenance_title'
        db.add_column('indivo_vitalsigns', 'bp_systolic_name_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_systolic_name_prov_title', blank=True), keep_default=False)

        
        # Adding field 'VitalSigns.bp_site_provenance_source_code'
        db.add_column('indivo_vitalsigns', 'bp_site_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_site_prov_sc', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_site_provenance_translation_fidelity_identifier'
        db.add_column('indivo_vitalsigns', 'bp_site_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_site_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_site_provenance_translation_fidelity_system'
        db.add_column('indivo_vitalsigns', 'bp_site_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_site_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_site_provenance_translation_fidelity_title'
        db.add_column('indivo_vitalsigns', 'bp_site_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_site_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_site_provenance_title'
        db.add_column('indivo_vitalsigns', 'bp_site_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_site_prov_title', blank=True), keep_default=False)

        
        # Adding field 'VitalSigns.bp_method_provenance_source_code'
        db.add_column('indivo_vitalsigns', 'bp_method_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_method_prov_sc', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_method_provenance_translation_fidelity_identifier'
        db.add_column('indivo_vitalsigns', 'bp_method_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_method_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_method_provenance_translation_fidelity_system'
        db.add_column('indivo_vitalsigns', 'bp_method_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_method_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_method_provenance_translation_fidelity_title'
        db.add_column('indivo_vitalsigns', 'bp_method_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_method_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'VitalSigns.bp_method_provenance_title'
        db.add_column('indivo_vitalsigns', 'bp_method_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='bp_method_prov_title', blank=True), keep_default=False)

        
        # Adding field 'VitalSigns.head_circ_value'
        db.add_column('indivo_vitalsigns', 'head_circ_value', self.gf('django.db.models.fields.FloatField')(null=True, db_column='head_circ_value', blank=True), keep_default=False)

        # Adding field 'VitalSigns.head_circ_unit'
        db.add_column('indivo_vitalsigns', 'head_circ_unit', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='head_circ_unit', blank=True), keep_default=False)

        # Adding field 'VitalSigns.head_circ_name_provenance_source_code'
        db.add_column('indivo_vitalsigns', 'head_circ_name_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='head_circ_name_prov_sc', blank=True), keep_default=False)

        # Adding field 'VitalSigns.head_circ_name_provenance_translation_fidelity_identifier'
        db.add_column('indivo_vitalsigns', 'head_circ_name_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='head_circ_name_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'VitalSigns.head_circ_name_provenance_translation_fidelity_system'
        db.add_column('indivo_vitalsigns', 'head_circ_name_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='head_circ_name_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'VitalSigns.head_circ_name_provenance_translation_fidelity_title'
        db.add_column('indivo_vitalsigns', 'head_circ_name_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='head_circ_name_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'VitalSigns.head_circ_name_provenance_title'
        db.add_column('indivo_vitalsigns', 'head_circ_name_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='head_circ_name_prov_title', blank=True), keep_default=False)

        # Adding field 'VitalSigns.head_circ_name_code_id'
        db.add_column('indivo_vitalsigns', 'head_circ_name_code_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='head_circ_name_code_id', blank=True), keep_default=False)

        # Adding field 'VitalSigns.head_circ_name_code_sys'
        db.add_column('indivo_vitalsigns', 'head_circ_name_code_sys', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='head_circ_name_code_sys', blank=True), keep_default=False)

        # Adding field 'VitalSigns.head_circ_name_code_title'
        db.add_column('indivo_vitalsigns', 'head_circ_name_code_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='head_circ_name_code_title', blank=True), keep_default=False)

        # Adding field 'VitalSigns.head_circ_name_title'
        db.add_column('indivo_vitalsigns', 'head_circ_name_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='head_circ_name_title', blank=True), keep_default=False)

        
        
        db.rename_column('indivo_allergy', 'drug_class_allergen_identifier', 'drug_class_allergen_code_id')
        db.rename_column('indivo_allergy', 'drug_class_allergen_system', 'drug_class_allergen_code_sys')
        db.rename_column('indivo_allergy', 'drug_class_allergen_title', 'drug_class_allergen_code_title')
        db.add_column('indivo_allergy', 'drug_class_allergen_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        
        
        db.rename_column('indivo_allergy', 'category_identifier', 'category_code_id')
        db.rename_column('indivo_allergy', 'category_system', 'category_code_sys')
        db.rename_column('indivo_allergy', 'category_title', 'category_code_title')
        db.add_column('indivo_allergy', 'category_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)


        db.rename_column('indivo_allergy', 'severity_identifier', 'severity_code_id')
        db.rename_column('indivo_allergy', 'severity_system', 'severity_code_sys')
        db.rename_column('indivo_allergy', 'severity_title', 'severity_code_title')
        db.add_column('indivo_allergy', 'severity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)


        
        db.rename_column('indivo_allergy', 'allergic_reaction_identifier', 'allergic_reaction_code_id')
        db.rename_column('indivo_allergy', 'allergic_reaction_system', 'allergic_reaction_code_sys')
        db.rename_column('indivo_allergy', 'allergic_reaction_title', 'allergic_reaction_code_title')
        db.add_column('indivo_allergy', 'allergic_reaction_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        
        
        db.rename_column('indivo_allergy', 'drug_allergen_identifier', 'drug_allergen_code_id')
        db.rename_column('indivo_allergy', 'drug_allergen_system', 'drug_allergen_code_sys')
        db.rename_column('indivo_allergy', 'drug_allergen_title', 'drug_allergen_code_title')
        db.add_column('indivo_allergy', 'drug_allergen_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        
       
        db.rename_column('indivo_allergy', 'food_allergen_identifier', 'other_allergen_code_id')
        db.rename_column('indivo_allergy', 'food_allergen_system', 'other_allergen_code_sys')
        db.rename_column('indivo_allergy', 'food_allergen_title', 'other_allergen_code_title')
        db.add_column('indivo_allergy', 'other_allergen_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        

        # Adding field 'Allergy.category_provenance_source_code'
        db.add_column('indivo_allergy', 'category_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='category_prov_sc', blank=True), keep_default=False)

        # Adding field 'Allergy.category_provenance_translation_fidelity_identifier'
        db.add_column('indivo_allergy', 'category_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='category_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Allergy.category_provenance_translation_fidelity_system'
        db.add_column('indivo_allergy', 'category_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='category_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Allergy.category_provenance_translation_fidelity_title'
        db.add_column('indivo_allergy', 'category_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='category_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Allergy.category_provenance_title'
        db.add_column('indivo_allergy', 'category_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='category_prov_title', blank=True), keep_default=False)

        # Adding field 'Allergy.severity_provenance_source_code'
        db.add_column('indivo_allergy', 'severity_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='severity_prov_sc', blank=True), keep_default=False)

        # Adding field 'Allergy.severity_provenance_translation_fidelity_identifier'
        db.add_column('indivo_allergy', 'severity_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='severity_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Allergy.severity_provenance_translation_fidelity_system'
        db.add_column('indivo_allergy', 'severity_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='severity_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Allergy.severity_provenance_translation_fidelity_title'
        db.add_column('indivo_allergy', 'severity_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='severity_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Allergy.severity_provenance_title'
        db.add_column('indivo_allergy', 'severity_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='severity_prov_title', blank=True), keep_default=False)

        # Adding field 'Allergy.drug_allergen_provenance_source_code'
        db.add_column('indivo_allergy', 'drug_allergen_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='drug_allergen_prov_sc', blank=True), keep_default=False)

        # Adding field 'Allergy.drug_allergen_provenance_translation_fidelity_identifier'
        db.add_column('indivo_allergy', 'drug_allergen_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='drug_allergen_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Allergy.drug_allergen_provenance_translation_fidelity_system'
        db.add_column('indivo_allergy', 'drug_allergen_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='drug_allergen_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Allergy.drug_allergen_provenance_translation_fidelity_title'
        db.add_column('indivo_allergy', 'drug_allergen_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='drug_allergen_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Allergy.drug_allergen_provenance_title'
        db.add_column('indivo_allergy', 'drug_allergen_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='drug_allergen_prov_title', blank=True), keep_default=False)

        
        # Adding field 'Allergy.drug_class_allergen_provenance_source_code'
        db.add_column('indivo_allergy', 'drug_class_allergen_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='drug_class_allergen_prov_sc', blank=True), keep_default=False)

        # Adding field 'Allergy.drug_class_allergen_provenance_translation_fidelity_identifier'
        db.add_column('indivo_allergy', 'drug_class_allergen_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='drug_class_allergen_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Allergy.drug_class_allergen_provenance_translation_fidelity_system'
        db.add_column('indivo_allergy', 'drug_class_allergen_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='drug_class_allergen_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Allergy.drug_class_allergen_provenance_translation_fidelity_title'
        db.add_column('indivo_allergy', 'drug_class_allergen_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='drug_class_allergen_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Allergy.drug_class_allergen_provenance_title'
        db.add_column('indivo_allergy', 'drug_class_allergen_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='drug_class_allergen_prov_title', blank=True), keep_default=False)

        

        # Adding field 'Allergy.other_allergen_provenance_source_code'
        db.add_column('indivo_allergy', 'other_allergen_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='other_allergen_prov_sc', blank=True), keep_default=False)

        # Adding field 'Allergy.other_allergen_provenance_translation_fidelity_identifier'
        db.add_column('indivo_allergy', 'other_allergen_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='other_allergen_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Allergy.other_allergen_provenance_translation_fidelity_system'
        db.add_column('indivo_allergy', 'other_allergen_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='other_allergen_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Allergy.other_allergen_provenance_translation_fidelity_title'
        db.add_column('indivo_allergy', 'other_allergen_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='other_allergen_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Allergy.other_allergen_provenance_title'
        db.add_column('indivo_allergy', 'other_allergen_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='other_allergen_prov_title', blank=True), keep_default=False)

        
        # Adding field 'Allergy.allergic_reaction_provenance_source_code'
        db.add_column('indivo_allergy', 'allergic_reaction_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='allergic_reaction_prov_sc', blank=True), keep_default=False)

        # Adding field 'Allergy.allergic_reaction_provenance_translation_fidelity_identifier'
        db.add_column('indivo_allergy', 'allergic_reaction_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='allergic_reaction_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Allergy.allergic_reaction_provenance_translation_fidelity_system'
        db.add_column('indivo_allergy', 'allergic_reaction_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='allergic_reaction_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Allergy.allergic_reaction_provenance_translation_fidelity_title'
        db.add_column('indivo_allergy', 'allergic_reaction_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='allergic_reaction_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Allergy.allergic_reaction_provenance_title'
        db.add_column('indivo_allergy', 'allergic_reaction_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='allergic_reaction_prov_title', blank=True), keep_default=False)

       
        
        # Deleting field 'Procedure.date_performed'
        db.delete_column('indivo_procedure', 'date_performed')

        # Deleting field 'Procedure.name_value'
        db.delete_column('indivo_procedure', 'name_value')

        # Deleting field 'Procedure.name_abbrev'
        db.delete_column('indivo_procedure', 'name_abbrev')

        # Deleting field 'Procedure.name'
        db.delete_column('indivo_procedure', 'name')

        # Deleting field 'Procedure.comments'
        db.delete_column('indivo_procedure', 'comments')

        # Deleting field 'Procedure.provider_institution'
        db.delete_column('indivo_procedure', 'provider_institution')

        # Deleting field 'Procedure.location'
        db.delete_column('indivo_procedure', 'location')

        # Deleting field 'Procedure.provider_name'
        db.delete_column('indivo_procedure', 'provider_name')

        # Deleting field 'Procedure.name_type'
        db.delete_column('indivo_procedure', 'name_type')

        # Adding field 'Procedure.date'
        db.add_column('indivo_procedure', 'date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'Procedure.notes'
        db.add_column('indivo_procedure', 'notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Procedure.status_provenance_source_code'
        db.add_column('indivo_procedure', 'status_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='status_prov_sc', blank=True), keep_default=False)

        # Adding field 'Procedure.status_provenance_translation_fidelity_identifier'
        db.add_column('indivo_procedure', 'status_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='status_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Procedure.status_provenance_translation_fidelity_system'
        db.add_column('indivo_procedure', 'status_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='status_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Procedure.status_provenance_translation_fidelity_title'
        db.add_column('indivo_procedure', 'status_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='status_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Procedure.status_provenance_title'
        db.add_column('indivo_procedure', 'status_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='status_prov_title', blank=True), keep_default=False)

        # Adding field 'Procedure.status_code_id'
        db.add_column('indivo_procedure', 'status_code_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='status_code_id', blank=True), keep_default=False)

        # Adding field 'Procedure.status_code_sys'
        db.add_column('indivo_procedure', 'status_code_sys', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='status_code_sys', blank=True), keep_default=False)

        # Adding field 'Procedure.status_code_title'
        db.add_column('indivo_procedure', 'status_code_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='status_code_title', blank=True), keep_default=False)

        # Adding field 'Procedure.status_title'
        db.add_column('indivo_procedure', 'status_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='status_title', blank=True), keep_default=False)

        # Adding field 'Procedure.name_provenance_source_code'
        db.add_column('indivo_procedure', 'name_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_sc', blank=True), keep_default=False)

        # Adding field 'Procedure.name_provenance_translation_fidelity_identifier'
        db.add_column('indivo_procedure', 'name_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Procedure.name_provenance_translation_fidelity_system'
        db.add_column('indivo_procedure', 'name_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Procedure.name_provenance_translation_fidelity_title'
        db.add_column('indivo_procedure', 'name_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Procedure.name_provenance_title'
        db.add_column('indivo_procedure', 'name_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_title', blank=True), keep_default=False)

        # Adding field 'Procedure.name_code_id'
        db.add_column('indivo_procedure', 'name_code_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_code_id', blank=True), keep_default=False)

        # Adding field 'Procedure.name_code_sys'
        db.add_column('indivo_procedure', 'name_code_sys', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_code_sys', blank=True), keep_default=False)

        # Adding field 'Procedure.name_code_title'
        db.add_column('indivo_procedure', 'name_code_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_code_title', blank=True), keep_default=False)

        # Adding field 'Procedure.name_title'
        db.add_column('indivo_procedure', 'name_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_title', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_bday'
        db.add_column('indivo_procedure', 'provider_bday', self.gf('django.db.models.fields.DateField')(null=True, db_column='provider_bday', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_dea_number'
        db.add_column('indivo_procedure', 'provider_dea_number', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provider_dea_number', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_ethnicity'
        db.add_column('indivo_procedure', 'provider_ethnicity', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provider_ethnicity', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_npi_number'
        db.add_column('indivo_procedure', 'provider_npi_number', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provider_npi_number', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_adr_postalcode'
        db.add_column('indivo_procedure', 'provider_adr_postalcode', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, db_column='provider_adr_postalcode', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_adr_country'
        db.add_column('indivo_procedure', 'provider_adr_country', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provider_adr_country', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_adr_region'
        db.add_column('indivo_procedure', 'provider_adr_region', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provider_adr_region', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_adr_street'
        db.add_column('indivo_procedure', 'provider_adr_street', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provider_adr_street', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_adr_city'
        db.add_column('indivo_procedure', 'provider_adr_city', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provider_adr_city', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_name_middle'
        db.add_column('indivo_procedure', 'provider_name_middle', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provider_name_middle', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_name_given'
        db.add_column('indivo_procedure', 'provider_name_given', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provider_name_given', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_name_prefix'
        db.add_column('indivo_procedure', 'provider_name_prefix', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provider_name_prefix', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_name_family'
        db.add_column('indivo_procedure', 'provider_name_family', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provider_name_family', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_name_suffix'
        db.add_column('indivo_procedure', 'provider_name_suffix', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provider_name_suffix', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_preferred_language'
        db.add_column('indivo_procedure', 'provider_preferred_language', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provider_preferred_language', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_tel_2_type'
        db.add_column('indivo_procedure', 'provider_tel_2_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, db_column='provider_tel_2_type', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_tel_2_number'
        db.add_column('indivo_procedure', 'provider_tel_2_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, db_column='provider_tel_2_number', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_tel_2_preferred_p'
        db.add_column('indivo_procedure', 'provider_tel_2_preferred_p', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='provider_tel_2_preferred_p'), keep_default=False)

        # Adding field 'Procedure.provider_tel_1_type'
        db.add_column('indivo_procedure', 'provider_tel_1_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, db_column='provider_tel_1_type', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_tel_1_number'
        db.add_column('indivo_procedure', 'provider_tel_1_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, db_column='provider_tel_1_number', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_tel_1_preferred_p'
        db.add_column('indivo_procedure', 'provider_tel_1_preferred_p', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='provider_tel_1_preferred_p'), keep_default=False)

        # Adding field 'Procedure.provider_race'
        db.add_column('indivo_procedure', 'provider_race', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provider_race', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_gender'
        db.add_column('indivo_procedure', 'provider_gender', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provider_gender', blank=True), keep_default=False)

        # Adding field 'Procedure.provider_email'
        db.add_column('indivo_procedure', 'provider_email', self.gf('django.db.models.fields.EmailField')(max_length=255, null=True, db_column='provider_email', blank=True), keep_default=False)


        db.rename_column('indivo_allergyexclusion', 'name_identifier', 'name_code_id')
        db.rename_column('indivo_allergyexclusion', 'name_system', 'name_code_sys')
        db.rename_column('indivo_allergyexclusion', 'name_title', 'name_code_title')
        db.add_column('indivo_allergyexclusion', 'name_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'AllergyExclusion.name_provenance_source_code'
        db.add_column('indivo_allergyexclusion', 'name_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_sc', blank=True), keep_default=False)

        # Adding field 'AllergyExclusion.name_provenance_translation_fidelity_identifier'
        db.add_column('indivo_allergyexclusion', 'name_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'AllergyExclusion.name_provenance_translation_fidelity_system'
        db.add_column('indivo_allergyexclusion', 'name_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'AllergyExclusion.name_provenance_translation_fidelity_title'
        db.add_column('indivo_allergyexclusion', 'name_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'AllergyExclusion.name_provenance_title'
        db.add_column('indivo_allergyexclusion', 'name_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_title', blank=True), keep_default=False)

       
        
        db.rename_column('indivo_medication', 'drugName_identifier', 'name_code_id')
        db.rename_column('indivo_medication', 'drugName_system', 'name_code_sys')
        db.rename_column('indivo_medication', 'drugName_title', 'name_code_title')
        db.add_column('indivo_medication', 'name_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        
        db.rename_column('indivo_medication', 'provenance_identifier', 'provenance_code_id')
        db.rename_column('indivo_medication', 'provenance_system', 'provenance_code_sys')
        db.rename_column('indivo_medication', 'provenance_title', 'provenance_code_title')
        db.add_column('indivo_medication', 'provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)


        # Adding field 'Medication.name_provenance_source_code'
        db.add_column('indivo_medication', 'name_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_sc', blank=True), keep_default=False)

        # Adding field 'Medication.name_provenance_translation_fidelity_identifier'
        db.add_column('indivo_medication', 'name_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Medication.name_provenance_translation_fidelity_system'
        db.add_column('indivo_medication', 'name_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Medication.name_provenance_translation_fidelity_title'
        db.add_column('indivo_medication', 'name_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Medication.name_provenance_title'
        db.add_column('indivo_medication', 'name_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_title', blank=True), keep_default=False)

        

        # Adding field 'Medication.provenance_provenance_source_code'
        db.add_column('indivo_medication', 'provenance_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provenance_prov_sc', blank=True), keep_default=False)

        # Adding field 'Medication.provenance_provenance_translation_fidelity_identifier'
        db.add_column('indivo_medication', 'provenance_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provenance_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'Medication.provenance_provenance_translation_fidelity_system'
        db.add_column('indivo_medication', 'provenance_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provenance_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'Medication.provenance_provenance_translation_fidelity_title'
        db.add_column('indivo_medication', 'provenance_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provenance_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'Medication.provenance_provenance_title'
        db.add_column('indivo_medication', 'provenance_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='provenance_prov_title', blank=True), keep_default=False)


        # Deleting field 'LabResult.collected_by_org_adr_country'
        db.delete_column('indivo_labresult', 'collected_by_org_adr_country')

        # Deleting field 'LabResult.collected_by_name_suffix'
        db.delete_column('indivo_labresult', 'collected_by_name_suffix')

        # Deleting field 'LabResult.collected_by_org_adr_city'
        db.delete_column('indivo_labresult', 'collected_by_org_adr_city')

        # Deleting field 'LabResult.collected_by_name_given'
        db.delete_column('indivo_labresult', 'collected_by_name_given')

        # Deleting field 'LabResult.collected_by_role'
        db.delete_column('indivo_labresult', 'collected_by_role')

        # Deleting field 'LabResult.collected_by_org_adr_region'
        db.delete_column('indivo_labresult', 'collected_by_org_adr_region')

        # Deleting field 'LabResult.collected_by_org_name'
        db.delete_column('indivo_labresult', 'collected_by_org_name')

        # Deleting field 'LabResult.collected_by_org_adr_postalcode'
        db.delete_column('indivo_labresult', 'collected_by_org_adr_postalcode')

        # Deleting field 'LabResult.collected_by_name_prefix'
        db.delete_column('indivo_labresult', 'collected_by_name_prefix')

        # Deleting field 'LabResult.collected_by_org_adr_street'
        db.delete_column('indivo_labresult', 'collected_by_org_adr_street')

        # Deleting field 'LabResult.collected_by_name_family'
        db.delete_column('indivo_labresult', 'collected_by_name_family')
        
        # Deleting field 'LabResult.collected_by_name_middle'
        db.delete_column('indivo_labresult', 'collected_by_name_middle')

        
        db.rename_column('indivo_labresult', 'test_name_identifier', 'name_code_id')
        db.rename_column('indivo_labresult', 'test_name_system', 'name_code_sys')
        db.rename_column('indivo_labresult', 'test_name_title', 'name_code_title')
        db.add_column('indivo_labresult', 'name_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        
        db.rename_column('indivo_labresult', 'abnormal_interpretation_identifier', 'abnormal_interpretation_code_id')
        db.rename_column('indivo_labresult', 'abnormal_interpretation_system', 'abnormal_interpretation_code_sys')
        db.rename_column('indivo_labresult', 'abnormal_interpretation_title', 'abnormal_interpretation_code_title')
        db.add_column('indivo_labresult', 'abnormal_interpretation_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        
        
        db.rename_column('indivo_labresult', 'status_identifier', 'status_code_id')
        db.rename_column('indivo_labresult', 'status_system', 'status_code_sys')
        db.rename_column('indivo_labresult', 'status_title', 'status_code_title')
        db.add_column('indivo_labresult', 'status_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

       
        db.rename_column('indivo_labresult', 'collected_at', 'date')
       
        # Adding field 'LabResult.status_provenance_source_code'
        db.add_column('indivo_labresult', 'status_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='status_prov_sc', blank=True), keep_default=False)

        # Adding field 'LabResult.status_provenance_translation_fidelity_identifier'
        db.add_column('indivo_labresult', 'status_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='status_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'LabResult.status_provenance_translation_fidelity_system'
        db.add_column('indivo_labresult', 'status_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='status_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'LabResult.status_provenance_translation_fidelity_title'
        db.add_column('indivo_labresult', 'status_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='status_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'LabResult.status_provenance_title'
        db.add_column('indivo_labresult', 'status_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='status_prov_title', blank=True), keep_default=False)

        
        # Adding field 'LabResult.name_provenance_source_code'
        db.add_column('indivo_labresult', 'name_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_sc', blank=True), keep_default=False)

        # Adding field 'LabResult.name_provenance_translation_fidelity_identifier'
        db.add_column('indivo_labresult', 'name_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'LabResult.name_provenance_translation_fidelity_system'
        db.add_column('indivo_labresult', 'name_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'LabResult.name_provenance_translation_fidelity_title'
        db.add_column('indivo_labresult', 'name_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'LabResult.name_provenance_title'
        db.add_column('indivo_labresult', 'name_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='name_prov_title', blank=True), keep_default=False)

        

        # Adding field 'LabResult.abnormal_interpretation_provenance_source_code'
        db.add_column('indivo_labresult', 'abnormal_interpretation_provenance_source_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='abnormal_interpretation_prov_sc', blank=True), keep_default=False)

        # Adding field 'LabResult.abnormal_interpretation_provenance_translation_fidelity_identifier'
        db.add_column('indivo_labresult', 'abnormal_interpretation_provenance_translation_fidelity_identifier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='abnormal_interpretation_prov_tf_id', blank=True), keep_default=False)

        # Adding field 'LabResult.abnormal_interpretation_provenance_translation_fidelity_system'
        db.add_column('indivo_labresult', 'abnormal_interpretation_provenance_translation_fidelity_system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='abnormal_interpretation_prov_tf_sys', blank=True), keep_default=False)

        # Adding field 'LabResult.abnormal_interpretation_provenance_translation_fidelity_title'
        db.add_column('indivo_labresult', 'abnormal_interpretation_provenance_translation_fidelity_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='abnormal_interpretation_prov_tf_title', blank=True), keep_default=False)

        # Adding field 'LabResult.abnormal_interpretation_provenance_title'
        db.add_column('indivo_labresult', 'abnormal_interpretation_provenance_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, db_column='abnormal_interpretation_prov_title', blank=True), keep_default=False)

       


    def backwards(self, orm):
        
        db.delete_column('indivo_encounter', 'type_prov_sc')
        db.delete_column('indivo_encounter', 'type_prov_tf_id')
        db.delete_column('indivo_encounter', 'type_prov_tf_sys')
        db.delete_column('indivo_encounter', 'type_prov_tf_title')
        db.delete_column('indivo_encounter', 'type_prov_title')
        db.rename_column('indivo_encounter', 'type_code_id', 'encounterType_identifier')
        db.rename_column('indivo_encounter', 'type_code_sys', 'encounterType_system')
        db.rename_column('indivo_encounter', 'type_code_title', 'encounterType_title')
        db.delete_column('indivo_encounter', 'type_title')

        db.delete_column('indivo_immunization', 'administration_status_title')
        db.rename_column('indivo_immunization', 'administration_status_code_sys', 'administration_status_system')
        db.rename_column('indivo_immunization', 'administration_status_code_id', 'administration_status_identifier')
        db.rename_column('indivo_immunization', 'administration_status_code_title', 'administration_status_title')
        
        db.delete_column('indivo_immunization', 'product_class_title')
        db.rename_column('indivo_immunization', 'product_class_code_id', 'product_class_identifier')
        db.rename_column('indivo_immunization', 'product_class_code_sys', 'product_class_system')
        db.rename_column('indivo_immunization', 'product_class_code_title', 'product_class_title')

        db.delete_column('indivo_immunization', 'product_class_2_title')
        db.rename_column('indivo_immunization', 'product_class_2_code_sys', 'product_class_2_system')
        db.rename_column('indivo_immunization', 'product_class_2_code_id', 'product_class_2_identifier')
        db.rename_column('indivo_immunization', 'product_class_2_code_title', 'product_class_2_title')

        db.delete_column('indivo_immunization', 'product_name_title')
        db.rename_column('indivo_immunization', 'product_name_code_id', 'product_name_identifier')
        db.rename_column('indivo_immunization', 'product_name_code_sys', 'product_name_system')
        db.rename_column('indivo_immunization', 'product_name_code_title', 'product_name_title')

        db.delete_column('indivo_immunization', 'refusal_reason_title')
        db.rename_column('indivo_immunization', 'refusal_reason_code_sys', 'refusal_reason_system')
        db.rename_column('indivo_immunization', 'refusal_reason_code_id', 'refusal_reason_identifier')
        db.rename_column('indivo_immunization', 'refusal_reason_code_title', 'refusal_reason_title')
        
        
        db.delete_column('indivo_immunization', 'product_class_prov_sc')
        db.delete_column('indivo_immunization', 'product_class_prov_tf_id')
        db.delete_column('indivo_immunization', 'product_class_prov_tf_sys')
        db.delete_column('indivo_immunization', 'product_class_prov_tf_title')
        db.delete_column('indivo_immunization', 'product_class_prov_title')
        db.delete_column('indivo_immunization', 'product_class_2_prov_sc')
        db.delete_column('indivo_immunization', 'product_class_2_prov_tf_id')
        db.delete_column('indivo_immunization', 'product_class_2_prov_tf_sys')
        db.delete_column('indivo_immunization', 'product_class_2_prov_tf_title')
        db.delete_column('indivo_immunization', 'product_class_2_prov_title')
        db.delete_column('indivo_immunization', 'refusal_reason_prov_sc')
        db.delete_column('indivo_immunization', 'refusal_reason_prov_tf_id')
        db.delete_column('indivo_immunization', 'refusal_reason_prov_tf_sys')
        db.delete_column('indivo_immunization', 'refusal_reason_prov_tf_title')
        db.delete_column('indivo_immunization', 'refusal_reason_prov_title')
        db.delete_column('indivo_immunization', 'administration_status_prov_sc')
        db.delete_column('indivo_immunization', 'administration_status_prov_tf_id')
        db.delete_column('indivo_immunization', 'administration_status_prov_tf_sys')
        db.delete_column('indivo_immunization', 'administration_status_prov_tf_title')
        db.delete_column('indivo_immunization', 'administration_status_prov_title')
        db.delete_column('indivo_immunization', 'product_name_prov_sc')
        db.delete_column('indivo_immunization', 'product_name_prov_tf_id')
        db.delete_column('indivo_immunization', 'product_name_prov_tf_sys')
        db.delete_column('indivo_immunization', 'product_name_prov_tf_title')
        db.delete_column('indivo_immunization', 'product_name_prov_title')

        db.delete_column('indivo_problem', 'name_title')
        db.rename_column('indivo_problem', 'name_code_id', 'name_identifier')
        db.rename_column('indivo_problem', 'name_code_sys', 'name_system')
        db.rename_column('indivo_problem', 'name_code_title', 'name_title')
        
        db.delete_column('indivo_problem', 'name_prov_sc')
        db.delete_column('indivo_problem', 'name_prov_tf_id')
        db.delete_column('indivo_problem', 'name_prov_tf_sys')
        db.delete_column('indivo_problem', 'name_prov_tf_title')
        db.delete_column('indivo_problem', 'name_prov_title')

        db.delete_column('indivo_vitalsigns', 'heart_rate_name_title')
        db.rename_column('indivo_vitalsigns', 'heart_rate_name_code_id', 'heart_rate_name_identifier')
        db.rename_column('indivo_vitalsigns', 'heart_rate_name_code_sys', 'heart_rate_name_system')
        db.rename_column('indivo_vitalsigns', 'heart_rate_name_code_title', 'heart_rate_name_title')

        db.delete_column('indivo_vitalsigns', 'oxygen_saturation_name_title')
        db.rename_column('indivo_vitalsigns', 'oxygen_saturation_name_code_id', 'oxygen_saturation_name_identifier')
        db.rename_column('indivo_vitalsigns', 'oxygen_saturation_name_code_sys', 'oxygen_saturation_name_system')
        db.rename_column('indivo_vitalsigns', 'oxygen_saturation_name_code_title', 'oxygen_saturation_name_title')

        db.delete_column('indivo_vitalsigns', 'temperature_name_title')
        db.rename_column('indivo_vitalsigns', 'temperature_name_code_id', 'temperature_name_identifier')
        db.rename_column('indivo_vitalsigns', 'temperature_name_code_sys', 'temperature_name_system')
        db.rename_column('indivo_vitalsigns', 'temperature_name_code_title', 'temperature_name_title')

        db.delete_column('indivo_vitalsigns', 'bp_systolic_name_title')
        db.rename_column('indivo_vitalsigns', 'bp_systolic_name_code_id', 'bp_systolic_name_identifier')
        db.rename_column('indivo_vitalsigns', 'bp_systolic_name_code_sys', 'bp_systolic_name_system')
        db.rename_column('indivo_vitalsigns', 'bp_systolic_name_code_title', 'bp_systolic_name_title')

        db.delete_column('indivo_vitalsigns', 'bp_diastolic_name_title')
        db.rename_column('indivo_vitalsigns', 'bp_diastolic_name_code_id', 'bp_diastolic_name_identifier')
        db.rename_column('indivo_vitalsigns', 'bp_diastolic_name_code_sys', 'bp_diastolic_name_system')
        db.rename_column('indivo_vitalsigns', 'bp_diastolic_name_code_title', 'bp_diastolic_name_title')

        db.delete_column('indivo_vitalsigns', 'height_name_title')
        db.rename_column('indivo_vitalsigns', 'height_name_code_id', 'height_name_identifier')
        db.rename_column('indivo_vitalsigns', 'height_name_code_sys', 'height_name_system')
        db.rename_column('indivo_vitalsigns', 'height_name_code_title', 'height_name_title')

        db.delete_column('indivo_vitalsigns', 'bmi_name_title')
        db.rename_column('indivo_vitalsigns', 'bmi_name_code_id', 'bmi_name_identifier')
        db.rename_column('indivo_vitalsigns', 'bmi_name_code_sys', 'bmi_name_system')
        db.rename_column('indivo_vitalsigns', 'bmi_name_code_title', 'bmi_name_title')

        db.delete_column('indivo_vitalsigns', 'respiratory_rate_name_title')
        db.rename_column('indivo_vitalsigns', 'respiratory_rate_name_code_id', 'respiratory_rate_name_identifier')
        db.rename_column('indivo_vitalsigns', 'respiratory_rate_name_code_sys', 'respiratory_rate_name_system')
        db.rename_column('indivo_vitalsigns', 'respiratory_rate_name_code_title', 'respiratory_rate_name_title')

        db.delete_column('indivo_vitalsigns', 'bp_position_title')
        db.rename_column('indivo_vitalsigns', 'bp_position_code_id', 'bp_position_identifier')
        db.rename_column('indivo_vitalsigns', 'bp_position_code_sys', 'bp_position_system')
        db.rename_column('indivo_vitalsigns', 'bp_position_code_title', 'bp_position_title')
                
        db.delete_column('indivo_vitalsigns', 'bp_method_title')
        db.rename_column('indivo_vitalsigns', 'bp_method_code_id', 'bp_method_identifier')
        db.rename_column('indivo_vitalsigns', 'bp_method_code_sys', 'bp_method_system')
        db.rename_column('indivo_vitalsigns', 'bp_method_code_title', 'bp_method_title')
        
        db.delete_column('indivo_vitalsigns', 'bp_site_title')
        db.rename_column('indivo_vitalsigns', 'bp_site_code_id', 'bp_site_identifier')
        db.rename_column('indivo_vitalsigns', 'bp_site_code_sys', 'bp_site_system')
        db.rename_column('indivo_vitalsigns', 'bp_site_code_title', 'bp_site_title')

        db.delete_column('indivo_vitalsigns', 'weight_name_title')
        db.rename_column('indivo_vitalsigns', 'weight_name_code_id', 'weight_name_identifier')
        db.rename_column('indivo_vitalsigns', 'weight_name_code_sys', 'weight_name_system')
        db.rename_column('indivo_vitalsigns', 'weight_name_code_title', 'weight_name_title')
        
        db.delete_column('indivo_vitalsigns', 'temperature_name_prov_sc')
        db.delete_column('indivo_vitalsigns', 'temperature_name_prov_tf_id')
        db.delete_column('indivo_vitalsigns', 'temperature_name_prov_tf_sys')
        db.delete_column('indivo_vitalsigns', 'temperature_name_prov_tf_title')
        db.delete_column('indivo_vitalsigns', 'temperature_name_prov_title')
        db.delete_column('indivo_vitalsigns', 'weight_name_prov_sc')
        db.delete_column('indivo_vitalsigns', 'weight_name_prov_tf_id')
        db.delete_column('indivo_vitalsigns', 'weight_name_prov_tf_sys')
        db.delete_column('indivo_vitalsigns', 'weight_name_prov_tf_title')
        db.delete_column('indivo_vitalsigns', 'weight_name_prov_title')
        db.delete_column('indivo_vitalsigns', 'oxygen_saturation_name_prov_sc')
        db.delete_column('indivo_vitalsigns', 'oxygen_saturation_name_prov_tf_id')
        db.delete_column('indivo_vitalsigns', 'oxygen_saturation_name_prov_tf_sys')
        db.delete_column('indivo_vitalsigns', 'oxygen_saturation_name_prov_tf_title')
        db.delete_column('indivo_vitalsigns', 'oxygen_saturation_name_prov_title')
        db.delete_column('indivo_vitalsigns', 'bmi_name_prov_sc')
        db.delete_column('indivo_vitalsigns', 'bmi_name_prov_tf_id')
        db.delete_column('indivo_vitalsigns', 'bmi_name_prov_tf_sys')
        db.delete_column('indivo_vitalsigns', 'bmi_name_prov_tf_title')
        db.delete_column('indivo_vitalsigns', 'bmi_name_prov_title')
        db.delete_column('indivo_vitalsigns', 'respiratory_rate_name_prov_sc')
        db.delete_column('indivo_vitalsigns', 'respiratory_rate_name_prov_tf_id')
        db.delete_column('indivo_vitalsigns', 'respiratory_rate_name_prov_tf_sys')
        db.delete_column('indivo_vitalsigns', 'respiratory_rate_name_prov_tf_title')
        db.delete_column('indivo_vitalsigns', 'respiratory_rate_name_prov_title')
        db.delete_column('indivo_vitalsigns', 'height_name_prov_sc')
        db.delete_column('indivo_vitalsigns', 'height_name_prov_tf_id')
        db.delete_column('indivo_vitalsigns', 'height_name_prov_tf_sys')
        db.delete_column('indivo_vitalsigns', 'height_name_prov_tf_title')
        db.delete_column('indivo_vitalsigns', 'height_name_prov_title')
        db.delete_column('indivo_vitalsigns', 'heart_rate_name_prov_sc')
        db.delete_column('indivo_vitalsigns', 'heart_rate_name_prov_tf_id')
        db.delete_column('indivo_vitalsigns', 'heart_rate_name_prov_tf_sys')
        db.delete_column('indivo_vitalsigns', 'heart_rate_name_prov_tf_title')
        db.delete_column('indivo_vitalsigns', 'heart_rate_name_prov_title')
        db.delete_column('indivo_vitalsigns', 'bp_position_prov_sc')
        db.delete_column('indivo_vitalsigns', 'bp_position_prov_tf_id')
        db.delete_column('indivo_vitalsigns', 'bp_position_prov_tf_sys')
        db.delete_column('indivo_vitalsigns', 'bp_position_prov_tf_title')
        db.delete_column('indivo_vitalsigns', 'bp_position_prov_title')
        db.delete_column('indivo_vitalsigns', 'bp_diastolic_name_prov_sc')
        db.delete_column('indivo_vitalsigns', 'bp_diastolic_name_prov_tf_id')
        db.delete_column('indivo_vitalsigns', 'bp_diastolic_name_prov_tf_sys')
        db.delete_column('indivo_vitalsigns', 'bp_diastolic_name_prov_tf_title')
        db.delete_column('indivo_vitalsigns', 'bp_diastolic_name_prov_title')
        db.delete_column('indivo_vitalsigns', 'bp_systolic_name_prov_sc')
        db.delete_column('indivo_vitalsigns', 'bp_systolic_name_prov_tf_id')
        db.delete_column('indivo_vitalsigns', 'bp_systolic_name_prov_tf_sys')
        db.delete_column('indivo_vitalsigns', 'bp_systolic_name_prov_tf_title')
        db.delete_column('indivo_vitalsigns', 'bp_systolic_name_prov_title')
        db.delete_column('indivo_vitalsigns', 'bp_site_prov_sc')
        db.delete_column('indivo_vitalsigns', 'bp_site_prov_tf_id')
        db.delete_column('indivo_vitalsigns', 'bp_site_prov_tf_sys')
        db.delete_column('indivo_vitalsigns', 'bp_site_prov_tf_title')
        db.delete_column('indivo_vitalsigns', 'bp_site_prov_title')
        db.delete_column('indivo_vitalsigns', 'bp_method_prov_sc')
        db.delete_column('indivo_vitalsigns', 'bp_method_prov_tf_id')
        db.delete_column('indivo_vitalsigns', 'bp_method_prov_tf_sys')
        db.delete_column('indivo_vitalsigns', 'bp_method_prov_tf_title')
        db.delete_column('indivo_vitalsigns', 'bp_method_prov_title')
        db.delete_column('indivo_vitalsigns', 'head_circ_value')
        db.delete_column('indivo_vitalsigns', 'head_circ_unit')
        db.delete_column('indivo_vitalsigns', 'head_circ_name_prov_sc')
        db.delete_column('indivo_vitalsigns', 'head_circ_name_prov_tf_id')
        db.delete_column('indivo_vitalsigns', 'head_circ_name_prov_tf_sys')
        db.delete_column('indivo_vitalsigns', 'head_circ_name_prov_tf_title')
        db.delete_column('indivo_vitalsigns', 'head_circ_name_prov_title')
        db.delete_column('indivo_vitalsigns', 'head_circ_name_code_id')
        db.delete_column('indivo_vitalsigns', 'head_circ_name_code_sys')
        db.delete_column('indivo_vitalsigns', 'head_circ_name_code_title')
        db.delete_column('indivo_vitalsigns', 'head_circ_name_title')


        db.delete_column('indivo_allergy', 'drug_class_allergen_title')
        db.rename_column('indivo_allergy', 'drug_class_allergen_code_id', 'drug_class_allergen_identifier')
        db.rename_column('indivo_allergy', 'drug_class_allergen_code_sys', 'drug_class_allergen_system')
        db.rename_column('indivo_allergy', 'drug_class_allergen_code_title', 'drug_class_allergen_title')
        
        db.delete_column('indivo_allergy', 'category_title')
        db.rename_column('indivo_allergy', 'category_code_id', 'category_identifier')
        db.rename_column('indivo_allergy', 'category_code_sys', 'category_system')
        db.rename_column('indivo_allergy', 'category_code_title', 'category_title')

        db.delete_column('indivo_allergy', 'severity_title')
        db.rename_column('indivo_allergy', 'severity_code_id', 'severity_identifier')
        db.rename_column('indivo_allergy', 'severity_code_sys', 'severity_system')
        db.rename_column('indivo_allergy', 'severity_code_title', 'severity_title')

        db.delete_column('indivo_allergy', 'allergic_reaction_title')
        db.rename_column('indivo_allergy', 'allergic_reaction_code_id', 'allergic_reaction_identifier')
        db.rename_column('indivo_allergy', 'allergic_reaction_code_sys', 'allergic_reaction_system')
        db.rename_column('indivo_allergy', 'allergic_reaction_code_title', 'allergic_reaction_title')

        db.delete_column('indivo_allergy', 'drug_allergen_title')
        db.rename_column('indivo_allergy', 'drug_allergen_code_id', 'drug_allergen_identifier')
        db.rename_column('indivo_allergy', 'drug_allergen_code_sys', 'drug_allergen_system')
        db.rename_column('indivo_allergy', 'drug_allergen_code_title', 'drug_allergen_title')

        db.delete_column('indivo_allergy', 'other_allergen_title')
        db.rename_column('indivo_allergy', 'other_allergen_code_id', 'food_allergen_identifier')
        db.rename_column('indivo_allergy', 'other_allergen_code_sys', 'food_allergen_system')
        db.rename_column('indivo_allergy', 'other_allergen_code_title', 'food_allergen_title')
        
        db.delete_column('indivo_allergy', 'category_prov_sc')
        db.delete_column('indivo_allergy', 'category_prov_tf_id')
        db.delete_column('indivo_allergy', 'category_prov_tf_sys')
        db.delete_column('indivo_allergy', 'category_prov_tf_title')
        db.delete_column('indivo_allergy', 'category_prov_title')
        db.delete_column('indivo_allergy', 'severity_prov_sc')
        db.delete_column('indivo_allergy', 'severity_prov_tf_id')
        db.delete_column('indivo_allergy', 'severity_prov_tf_sys')
        db.delete_column('indivo_allergy', 'severity_prov_tf_title')
        db.delete_column('indivo_allergy', 'severity_prov_title')
        db.delete_column('indivo_allergy', 'drug_allergen_prov_sc')
        db.delete_column('indivo_allergy', 'drug_allergen_prov_tf_id')
        db.delete_column('indivo_allergy', 'drug_allergen_prov_tf_sys')
        db.delete_column('indivo_allergy', 'drug_allergen_prov_tf_title')
        db.delete_column('indivo_allergy', 'drug_allergen_prov_title')
        db.delete_column('indivo_allergy', 'drug_class_allergen_prov_sc')
        db.delete_column('indivo_allergy', 'drug_class_allergen_prov_tf_id')
        db.delete_column('indivo_allergy', 'drug_class_allergen_prov_tf_sys')
        db.delete_column('indivo_allergy', 'drug_class_allergen_prov_tf_title')
        db.delete_column('indivo_allergy', 'drug_class_allergen_prov_title')
        db.delete_column('indivo_allergy', 'other_allergen_prov_sc')
        db.delete_column('indivo_allergy', 'other_allergen_prov_tf_id')
        db.delete_column('indivo_allergy', 'other_allergen_prov_tf_sys')
        db.delete_column('indivo_allergy', 'other_allergen_prov_tf_title')
        db.delete_column('indivo_allergy', 'other_allergen_prov_title')
        db.delete_column('indivo_allergy', 'allergic_reaction_prov_sc')
        db.delete_column('indivo_allergy', 'allergic_reaction_prov_tf_id')
        db.delete_column('indivo_allergy', 'allergic_reaction_prov_tf_sys')
        db.delete_column('indivo_allergy', 'allergic_reaction_prov_tf_title')
        db.delete_column('indivo_allergy', 'allergic_reaction_prov_title')
        
        
        db.add_column('indivo_procedure', 'date_performed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)
        db.add_column('indivo_procedure', 'name_value', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True), keep_default=False)
        db.add_column('indivo_procedure', 'name_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True), keep_default=False)
        db.add_column('indivo_procedure', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)
        db.add_column('indivo_procedure', 'comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)
        db.add_column('indivo_procedure', 'provider_institution', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True), keep_default=False)
        db.add_column('indivo_procedure', 'location', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True), keep_default=False)
        db.add_column('indivo_procedure', 'provider_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True), keep_default=False)
        db.add_column('indivo_procedure', 'name_type', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True), keep_default=False)
        
        db.delete_column('indivo_procedure', 'date')
        db.delete_column('indivo_procedure', 'notes')
        db.delete_column('indivo_procedure', 'status_prov_sc')
        db.delete_column('indivo_procedure', 'status_prov_tf_id')
        db.delete_column('indivo_procedure', 'status_prov_tf_sys')
        db.delete_column('indivo_procedure', 'status_prov_tf_title')
        db.delete_column('indivo_procedure', 'status_prov_title')
        db.delete_column('indivo_procedure', 'status_code_id')
        db.delete_column('indivo_procedure', 'status_code_sys')
        db.delete_column('indivo_procedure', 'status_code_title')
        db.delete_column('indivo_procedure', 'status_title')
        db.delete_column('indivo_procedure', 'name_prov_sc')
        db.delete_column('indivo_procedure', 'name_prov_tf_id')
        db.delete_column('indivo_procedure', 'name_prov_tf_sys')
        db.delete_column('indivo_procedure', 'name_prov_tf_title')
        db.delete_column('indivo_procedure', 'name_prov_title')
        db.delete_column('indivo_procedure', 'name_code_id')
        db.delete_column('indivo_procedure', 'name_code_sys')
        db.delete_column('indivo_procedure', 'name_code_title')
        db.delete_column('indivo_procedure', 'name_title')
        db.delete_column('indivo_procedure', 'provider_bday')
        db.delete_column('indivo_procedure', 'provider_dea_number')
        db.delete_column('indivo_procedure', 'provider_ethnicity')
        db.delete_column('indivo_procedure', 'provider_npi_number')
        db.delete_column('indivo_procedure', 'provider_adr_postalcode')
        db.delete_column('indivo_procedure', 'provider_adr_country')
        db.delete_column('indivo_procedure', 'provider_adr_region')
        db.delete_column('indivo_procedure', 'provider_adr_street')
        db.delete_column('indivo_procedure', 'provider_adr_city')
        db.delete_column('indivo_procedure', 'provider_name_middle')
        db.delete_column('indivo_procedure', 'provider_name_given')
        db.delete_column('indivo_procedure', 'provider_name_prefix')
        db.delete_column('indivo_procedure', 'provider_name_family')
        db.delete_column('indivo_procedure', 'provider_name_suffix')
        db.delete_column('indivo_procedure', 'provider_preferred_language')
        db.delete_column('indivo_procedure', 'provider_tel_2_type')
        db.delete_column('indivo_procedure', 'provider_tel_2_number')
        db.delete_column('indivo_procedure', 'provider_tel_2_preferred_p')
        db.delete_column('indivo_procedure', 'provider_tel_1_type')
        db.delete_column('indivo_procedure', 'provider_tel_1_number')
        db.delete_column('indivo_procedure', 'provider_tel_1_preferred_p')
        db.delete_column('indivo_procedure', 'provider_race')
        db.delete_column('indivo_procedure', 'provider_gender')
        db.delete_column('indivo_procedure', 'provider_email')

        db.delete_column('indivo_allergyexclusion', 'name_title')
        db.rename_column('indivo_allergyexclusion', 'name_code_id', 'name_identifier')
        db.rename_column('indivo_allergyexclusion', 'name_code_sys', 'name_system')
        db.rename_column('indivo_allergyexclusion', 'name_code_title', 'name_title')
        
        db.delete_column('indivo_allergyexclusion', 'name_prov_sc')
        db.delete_column('indivo_allergyexclusion', 'name_prov_tf_id')
        db.delete_column('indivo_allergyexclusion', 'name_prov_tf_sys')
        db.delete_column('indivo_allergyexclusion', 'name_prov_tf_title')
        db.delete_column('indivo_allergyexclusion', 'name_prov_title')
       
        db.delete_column('indivo_medication', 'name_title')
        db.rename_column('indivo_medication', 'name_code_id', 'drugName_identifier')
        db.rename_column('indivo_medication', 'name_code_sys', 'drugName_system')
        db.rename_column('indivo_medication', 'name_code_title', 'drugName_title')

        db.delete_column('indivo_medication', 'provenance_title')
        db.rename_column('indivo_medication', 'provenance_code_id', 'provenance_identifier')
        db.rename_column('indivo_medication', 'provenance_code_sys', 'provenance_system')
        db.rename_column('indivo_medication', 'provenance_code_title', 'provenance_title')
        
        db.delete_column('indivo_medication', 'name_prov_sc')
        db.delete_column('indivo_medication', 'name_prov_tf_id')
        db.delete_column('indivo_medication', 'name_prov_tf_sys')
        db.delete_column('indivo_medication', 'name_prov_tf_title')
        db.delete_column('indivo_medication', 'name_prov_title')
        db.delete_column('indivo_medication', 'provenance_prov_sc')
        db.delete_column('indivo_medication', 'provenance_prov_tf_id')
        db.delete_column('indivo_medication', 'provenance_prov_tf_sys')
        db.delete_column('indivo_medication', 'provenance_prov_tf_title')
        db.delete_column('indivo_medication', 'provenance_prov_title')
        
        
        db.add_column('indivo_labresult', 'collected_by_org_adr_country', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('indivo_labresult', 'collected_by_name_suffix', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('indivo_labresult', 'collected_by_org_adr_city', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('indivo_labresult', 'collected_by_name_given', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('indivo_labresult', 'collected_by_role', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('indivo_labresult', 'collected_by_org_adr_region', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('indivo_labresult', 'collected_by_org_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('indivo_labresult', 'collected_by_org_adr_postalcode', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True), keep_default=False)
        db.add_column('indivo_labresult', 'collected_by_name_prefix', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('indivo_labresult', 'collected_by_org_adr_street', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('indivo_labresult', 'collected_by_name_family', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)
        db.add_column('indivo_labresult', 'collected_by_name_middle', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        db.delete_column('indivo_labresult', 'name_title')
        db.rename_column('indivo_labresult', 'name_code_id', 'test_name_identifier')
        db.rename_column('indivo_labresult', 'name_code_sys', 'test_name_system')
        db.rename_column('indivo_labresult', 'name_code_title', 'test_name_title')
        
        db.delete_column('indivo_labresult', 'abnormal_interpretation_title')
        db.rename_column('indivo_labresult', 'abnormal_interpretation_code_id', 'abnormal_interpretation_identifier')
        db.rename_column('indivo_labresult', 'abnormal_interpretation_code_sys', 'abnormal_interpretation_system')
        db.rename_column('indivo_labresult', 'abnormal_interpretation_code_title', 'abnormal_interpretation_title')
        
        db.delete_column('indivo_labresult', 'status_title')
        db.rename_column('indivo_labresult', 'status_code_id', 'status_identifier')
        db.rename_column('indivo_labresult', 'status_code_sys', 'status_system')
        db.rename_column('indivo_labresult', 'status_code_title', 'status_title')
       
        db.rename_column('indivo_labresult', 'date', 'collected_at')
        db.delete_column('indivo_labresult', 'status_prov_sc')
        db.delete_column('indivo_labresult', 'status_prov_tf_id')
        db.delete_column('indivo_labresult', 'status_prov_tf_sys')
        db.delete_column('indivo_labresult', 'status_prov_tf_title')
        db.delete_column('indivo_labresult', 'status_prov_title')
        db.delete_column('indivo_labresult', 'name_prov_sc')
        db.delete_column('indivo_labresult', 'name_prov_tf_id')
        db.delete_column('indivo_labresult', 'name_prov_tf_sys')
        db.delete_column('indivo_labresult', 'name_prov_tf_title')
        db.delete_column('indivo_labresult', 'name_prov_title')
        db.delete_column('indivo_labresult', 'abnormal_interpretation_prov_sc')
        db.delete_column('indivo_labresult', 'abnormal_interpretation_prov_tf_id')
        db.delete_column('indivo_labresult', 'abnormal_interpretation_prov_tf_sys')
        db.delete_column('indivo_labresult', 'abnormal_interpretation_prov_tf_title')
        db.delete_column('indivo_labresult', 'abnormal_interpretation_prov_title')

        


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
            'allergic_reaction_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'allergic_reaction_code_id'"}),
            'allergic_reaction_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'allergic_reaction_code_sys'", 'blank': 'True'}),
            'allergic_reaction_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'allergic_reaction_code_title'"}),
            'allergic_reaction_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'allergic_reaction_prov_sc'", 'blank': 'True'}),
            'allergic_reaction_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'allergic_reaction_prov_title'", 'blank': 'True'}),
            'allergic_reaction_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'allergic_reaction_prov_tf_id'", 'blank': 'True'}),
            'allergic_reaction_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'allergic_reaction_prov_tf_sys'", 'blank': 'True'}),
            'allergic_reaction_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'allergic_reaction_prov_tf_title'", 'blank': 'True'}),
            'allergic_reaction_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'allergic_reaction_title'", 'blank': 'True'}),
            'category_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'category_code_id'", 'blank': 'True'}),
            'category_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'category_code_sys'", 'blank': 'True'}),
            'category_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'category_code_title'"}),
            'category_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'category_prov_sc'", 'blank': 'True'}),
            'category_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'category_prov_title'", 'blank': 'True'}),
            'category_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'category_prov_tf_id'", 'blank': 'True'}),
            'category_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'category_prov_tf_sys'", 'blank': 'True'}),
            'category_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'category_prov_tf_title'", 'blank': 'True'}),
            'category_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'category_title'", 'blank': 'True'}),
            'drug_allergen_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_allergen_code_id'", 'blank': 'True'}),
            'drug_allergen_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_allergen_code_sys'", 'blank': 'True'}),
            'drug_allergen_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_allergen_code_title'", 'blank': 'True'}),
            'drug_allergen_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_allergen_prov_sc'", 'blank': 'True'}),
            'drug_allergen_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_allergen_prov_title'", 'blank': 'True'}),
            'drug_allergen_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_allergen_prov_tf_id'", 'blank': 'True'}),
            'drug_allergen_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_allergen_prov_tf_sys'", 'blank': 'True'}),
            'drug_allergen_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_allergen_prov_tf_title'", 'blank': 'True'}),
            'drug_allergen_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_allergen_title'", 'blank': 'True'}),
            'drug_class_allergen_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_class_allergen_code_id'", 'blank': 'True'}),
            'drug_class_allergen_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_class_allergen_code_sys'", 'blank': 'True'}),
            'drug_class_allergen_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_class_allergen_code_title'", 'blank': 'True'}),
            'drug_class_allergen_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_class_allergen_prov_sc'", 'blank': 'True'}),
            'drug_class_allergen_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_class_allergen_prov_title'", 'blank': 'True'}),
            'drug_class_allergen_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_class_allergen_prov_tf_id'", 'blank': 'True'}),
            'drug_class_allergen_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_class_allergen_prov_tf_sys'", 'blank': 'True'}),
            'drug_class_allergen_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_class_allergen_prov_tf_title'", 'blank': 'True'}),
            'drug_class_allergen_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'drug_class_allergen_title'", 'blank': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'other_allergen_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'other_allergen_code_id'", 'blank': 'True'}),
            'other_allergen_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'other_allergen_code_sys'", 'blank': 'True'}),
            'other_allergen_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'other_allergen_code_title'", 'blank': 'True'}),
            'other_allergen_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'other_allergen_prov_sc'", 'blank': 'True'}),
            'other_allergen_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'other_allergen_prov_title'", 'blank': 'True'}),
            'other_allergen_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'other_allergen_prov_tf_id'", 'blank': 'True'}),
            'other_allergen_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'other_allergen_prov_tf_sys'", 'blank': 'True'}),
            'other_allergen_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'other_allergen_prov_tf_title'", 'blank': 'True'}),
            'other_allergen_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'other_allergen_title'", 'blank': 'True'}),
            'severity_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'severity_code_id'", 'blank': 'True'}),
            'severity_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'severity_code_sys'", 'blank': 'True'}),
            'severity_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'severity_code_title'"}),
            'severity_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'severity_prov_sc'", 'blank': 'True'}),
            'severity_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'severity_prov_title'", 'blank': 'True'}),
            'severity_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'severity_prov_tf_id'", 'blank': 'True'}),
            'severity_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'severity_prov_tf_sys'", 'blank': 'True'}),
            'severity_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'severity_prov_tf_title'", 'blank': 'True'}),
            'severity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'severity_title'", 'blank': 'True'})
        },
        'indivo.allergyexclusion': {
            'Meta': {'object_name': 'AllergyExclusion', '_ormbases': ['indivo.Fact']},
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'name_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_code_id'", 'blank': 'True'}),
            'name_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_code_sys'", 'blank': 'True'}),
            'name_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_code_title'"}),
            'name_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_sc'", 'blank': 'True'}),
            'name_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_title'", 'blank': 'True'}),
            'name_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_tf_id'", 'blank': 'True'}),
            'name_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_tf_sys'", 'blank': 'True'}),
            'name_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_tf_title'", 'blank': 'True'}),
            'name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_title'", 'blank': 'True'})
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
        'indivo.demographics': {
            'Meta': {'object_name': 'Demographics'},
            'adr_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'adr_city'", 'blank': 'True'}),
            'adr_country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'adr_country'", 'blank': 'True'}),
            'adr_postalcode': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'db_column': "'adr_postalcode'", 'blank': 'True'}),
            'adr_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'adr_region'", 'blank': 'True'}),
            'adr_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'adr_street'", 'blank': 'True'}),
            'bday': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Document']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ethnicity': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_family': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_family'", 'blank': 'True'}),
            'name_given': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_given'", 'blank': 'True'}),
            'name_middle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_middle'", 'blank': 'True'}),
            'name_prefix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prefix'", 'blank': 'True'}),
            'name_suffix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_suffix'", 'blank': 'True'}),
            'preferred_language': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tel_1_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'tel_1_number'", 'blank': 'True'}),
            'tel_1_preferred_p': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'tel_1_preferred_p'"}),
            'tel_1_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "'tel_1_type'", 'blank': 'True'}),
            'tel_2_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'tel_2_number'", 'blank': 'True'}),
            'tel_2_preferred_p': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'tel_2_preferred_p'"}),
            'tel_2_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "'tel_2_type'", 'blank': 'True'})
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
            'endDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'facility_adr_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'facility_adr_city'", 'blank': 'True'}),
            'facility_adr_country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'facility_adr_country'", 'blank': 'True'}),
            'facility_adr_postalcode': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'db_column': "'facility_adr_postalcode'", 'blank': 'True'}),
            'facility_adr_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'facility_adr_region'", 'blank': 'True'}),
            'facility_adr_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'facility_adr_street'", 'blank': 'True'}),
            'facility_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'facility_name'", 'blank': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'provider_adr_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_adr_city'", 'blank': 'True'}),
            'provider_adr_country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_adr_country'", 'blank': 'True'}),
            'provider_adr_postalcode': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'db_column': "'provider_adr_postalcode'", 'blank': 'True'}),
            'provider_adr_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_adr_region'", 'blank': 'True'}),
            'provider_adr_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_adr_street'", 'blank': 'True'}),
            'provider_bday': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'provider_bday'", 'blank': 'True'}),
            'provider_dea_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_dea_number'", 'blank': 'True'}),
            'provider_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_email'", 'blank': 'True'}),
            'provider_ethnicity': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_ethnicity'", 'blank': 'True'}),
            'provider_gender': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_gender'", 'blank': 'True'}),
            'provider_name_family': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_name_family'", 'blank': 'True'}),
            'provider_name_given': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_name_given'", 'blank': 'True'}),
            'provider_name_middle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_name_middle'", 'blank': 'True'}),
            'provider_name_prefix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_name_prefix'", 'blank': 'True'}),
            'provider_name_suffix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_name_suffix'", 'blank': 'True'}),
            'provider_npi_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_npi_number'", 'blank': 'True'}),
            'provider_preferred_language': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_preferred_language'", 'blank': 'True'}),
            'provider_race': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_race'", 'blank': 'True'}),
            'provider_tel_1_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'provider_tel_1_number'", 'blank': 'True'}),
            'provider_tel_1_preferred_p': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'provider_tel_1_preferred_p'"}),
            'provider_tel_1_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "'provider_tel_1_type'", 'blank': 'True'}),
            'provider_tel_2_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'provider_tel_2_number'", 'blank': 'True'}),
            'provider_tel_2_preferred_p': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'provider_tel_2_preferred_p'"}),
            'provider_tel_2_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "'provider_tel_2_type'", 'blank': 'True'}),
            'startDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'type_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'type_code_id'", 'blank': 'True'}),
            'type_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'type_code_sys'", 'blank': 'True'}),
            'type_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'type_code_title'"}),
            'type_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'type_prov_sc'", 'blank': 'True'}),
            'type_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'type_prov_title'", 'blank': 'True'}),
            'type_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'type_prov_tf_id'", 'blank': 'True'}),
            'type_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'type_prov_tf_sys'", 'blank': 'True'}),
            'type_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'type_prov_tf_title'", 'blank': 'True'}),
            'type_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'type_title'", 'blank': 'True'})
        },
        'indivo.equipment': {
            'Meta': {'object_name': 'Equipment', '_ormbases': ['indivo.Fact']},
            'date_started': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_stopped': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        'indivo.fact': {
            'Meta': {'object_name': 'Fact'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Document']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Record']", 'null': 'True', 'blank': 'True'})
        },
        'indivo.fill': {
            'Meta': {'object_name': 'Fill', '_ormbases': ['indivo.Fact']},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'dispenseDaysSupply': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'medication': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fulfillments'", 'null': 'True', 'to': "orm['indivo.Medication']"}),
            'pbm': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pharmacy_adr_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'pharmacy_adr_city'", 'blank': 'True'}),
            'pharmacy_adr_country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'pharmacy_adr_country'", 'blank': 'True'}),
            'pharmacy_adr_postalcode': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'db_column': "'pharmacy_adr_postalcode'", 'blank': 'True'}),
            'pharmacy_adr_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'pharmacy_adr_region'", 'blank': 'True'}),
            'pharmacy_adr_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'pharmacy_adr_street'", 'blank': 'True'}),
            'pharmacy_ncpdpid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'pharmacy_ncpdpid'", 'blank': 'True'}),
            'pharmacy_org': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'pharmacy_org'", 'blank': 'True'}),
            'provider_adr_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_adr_city'", 'blank': 'True'}),
            'provider_adr_country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_adr_country'", 'blank': 'True'}),
            'provider_adr_postalcode': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'db_column': "'provider_adr_postalcode'", 'blank': 'True'}),
            'provider_adr_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_adr_region'", 'blank': 'True'}),
            'provider_adr_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_adr_street'", 'blank': 'True'}),
            'provider_bday': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'provider_bday'", 'blank': 'True'}),
            'provider_dea_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_dea_number'", 'blank': 'True'}),
            'provider_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_email'", 'blank': 'True'}),
            'provider_ethnicity': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_ethnicity'", 'blank': 'True'}),
            'provider_gender': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_gender'", 'blank': 'True'}),
            'provider_name_family': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_name_family'", 'blank': 'True'}),
            'provider_name_given': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_name_given'", 'blank': 'True'}),
            'provider_name_middle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_name_middle'", 'blank': 'True'}),
            'provider_name_prefix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_name_prefix'", 'blank': 'True'}),
            'provider_name_suffix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_name_suffix'", 'blank': 'True'}),
            'provider_npi_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_npi_number'", 'blank': 'True'}),
            'provider_preferred_language': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_preferred_language'", 'blank': 'True'}),
            'provider_race': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_race'", 'blank': 'True'}),
            'provider_tel_1_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'provider_tel_1_number'", 'blank': 'True'}),
            'provider_tel_1_preferred_p': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'provider_tel_1_preferred_p'"}),
            'provider_tel_1_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "'provider_tel_1_type'", 'blank': 'True'}),
            'provider_tel_2_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'provider_tel_2_number'", 'blank': 'True'}),
            'provider_tel_2_preferred_p': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'provider_tel_2_preferred_p'"}),
            'provider_tel_2_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "'provider_tel_2_type'", 'blank': 'True'}),
            'quantityDispensed_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'quantityDispensed_unit'", 'blank': 'True'}),
            'quantityDispensed_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'quantityDispensed_value'", 'blank': 'True'})
        },
        'indivo.immunization': {
            'Meta': {'object_name': 'Immunization', '_ormbases': ['indivo.Fact']},
            'administration_status_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'administration_status_code_id'", 'blank': 'True'}),
            'administration_status_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'administration_status_code_sys'", 'blank': 'True'}),
            'administration_status_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'administration_status_code_title'"}),
            'administration_status_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'administration_status_prov_sc'", 'blank': 'True'}),
            'administration_status_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'administration_status_prov_title'", 'blank': 'True'}),
            'administration_status_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'administration_status_prov_tf_id'", 'blank': 'True'}),
            'administration_status_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'administration_status_prov_tf_sys'", 'blank': 'True'}),
            'administration_status_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'administration_status_prov_tf_title'", 'blank': 'True'}),
            'administration_status_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'administration_status_title'", 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'product_class_2_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_2_code_id'", 'blank': 'True'}),
            'product_class_2_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_2_code_sys'", 'blank': 'True'}),
            'product_class_2_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_2_code_title'", 'blank': 'True'}),
            'product_class_2_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_2_prov_sc'", 'blank': 'True'}),
            'product_class_2_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_2_prov_title'", 'blank': 'True'}),
            'product_class_2_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_2_prov_tf_id'", 'blank': 'True'}),
            'product_class_2_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_2_prov_tf_sys'", 'blank': 'True'}),
            'product_class_2_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_2_prov_tf_title'", 'blank': 'True'}),
            'product_class_2_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_2_title'", 'blank': 'True'}),
            'product_class_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_code_id'", 'blank': 'True'}),
            'product_class_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_code_sys'", 'blank': 'True'}),
            'product_class_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_code_title'", 'blank': 'True'}),
            'product_class_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_prov_sc'", 'blank': 'True'}),
            'product_class_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_prov_title'", 'blank': 'True'}),
            'product_class_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_prov_tf_id'", 'blank': 'True'}),
            'product_class_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_prov_tf_sys'", 'blank': 'True'}),
            'product_class_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_prov_tf_title'", 'blank': 'True'}),
            'product_class_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_class_title'", 'blank': 'True'}),
            'product_name_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_name_code_id'"}),
            'product_name_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_name_code_sys'", 'blank': 'True'}),
            'product_name_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_name_code_title'"}),
            'product_name_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_name_prov_sc'", 'blank': 'True'}),
            'product_name_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_name_prov_title'", 'blank': 'True'}),
            'product_name_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_name_prov_tf_id'", 'blank': 'True'}),
            'product_name_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_name_prov_tf_sys'", 'blank': 'True'}),
            'product_name_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_name_prov_tf_title'", 'blank': 'True'}),
            'product_name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'product_name_title'", 'blank': 'True'}),
            'refusal_reason_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'refusal_reason_code_id'", 'blank': 'True'}),
            'refusal_reason_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'refusal_reason_code_sys'", 'blank': 'True'}),
            'refusal_reason_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'refusal_reason_code_title'", 'blank': 'True'}),
            'refusal_reason_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'refusal_reason_prov_sc'", 'blank': 'True'}),
            'refusal_reason_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'refusal_reason_prov_title'", 'blank': 'True'}),
            'refusal_reason_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'refusal_reason_prov_tf_id'", 'blank': 'True'}),
            'refusal_reason_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'refusal_reason_prov_tf_sys'", 'blank': 'True'}),
            'refusal_reason_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'refusal_reason_prov_tf_title'", 'blank': 'True'}),
            'refusal_reason_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'refusal_reason_title'", 'blank': 'True'})
        },
        'indivo.labresult': {
            'Meta': {'object_name': 'LabResult', '_ormbases': ['indivo.Fact']},
            'abnormal_interpretation_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'abnormal_interpretation_code_id'", 'blank': 'True'}),
            'abnormal_interpretation_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'abnormal_interpretation_code_sys'", 'blank': 'True'}),
            'abnormal_interpretation_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'abnormal_interpretation_code_title'", 'blank': 'True'}),
            'abnormal_interpretation_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'abnormal_interpretation_prov_sc'", 'blank': 'True'}),
            'abnormal_interpretation_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'abnormal_interpretation_prov_title'", 'blank': 'True'}),
            'abnormal_interpretation_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'abnormal_interpretation_prov_tf_id'", 'blank': 'True'}),
            'abnormal_interpretation_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'abnormal_interpretation_prov_tf_sys'", 'blank': 'True'}),
            'abnormal_interpretation_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'abnormal_interpretation_prov_tf_title'", 'blank': 'True'}),
            'abnormal_interpretation_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'abnormal_interpretation_title'", 'blank': 'True'}),
            'accession_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'name_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_code_id'"}),
            'name_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_code_sys'", 'blank': 'True'}),
            'name_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_code_title'"}),
            'name_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_sc'", 'blank': 'True'}),
            'name_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_title'", 'blank': 'True'}),
            'name_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_tf_id'", 'blank': 'True'}),
            'name_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_tf_sys'", 'blank': 'True'}),
            'name_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_tf_title'", 'blank': 'True'}),
            'name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_title'", 'blank': 'True'}),
            'narrative_result': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '600', 'null': 'True', 'blank': 'True'}),
            'quantitative_result_non_critical_range_max_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'quantitative_result_non_critical_range_max_unit'", 'blank': 'True'}),
            'quantitative_result_non_critical_range_max_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'quantitative_result_non_critical_range_max_value'", 'blank': 'True'}),
            'quantitative_result_non_critical_range_min_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'quantitative_result_non_critical_range_min_unit'", 'blank': 'True'}),
            'quantitative_result_non_critical_range_min_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'quantitative_result_non_critical_range_min_value'", 'blank': 'True'}),
            'quantitative_result_normal_range_max_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'quantitative_result_normal_range_max_unit'", 'blank': 'True'}),
            'quantitative_result_normal_range_max_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'quantitative_result_normal_range_max_value'", 'blank': 'True'}),
            'quantitative_result_normal_range_min_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'quantitative_result_normal_range_min_unit'", 'blank': 'True'}),
            'quantitative_result_normal_range_min_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'quantitative_result_normal_range_min_value'", 'blank': 'True'}),
            'quantitative_result_value_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'quantitative_result_value_unit'", 'blank': 'True'}),
            'quantitative_result_value_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'quantitative_result_value_value'", 'blank': 'True'}),
            'status_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_code_id'", 'blank': 'True'}),
            'status_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_code_sys'", 'blank': 'True'}),
            'status_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_code_title'", 'blank': 'True'}),
            'status_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_prov_sc'", 'blank': 'True'}),
            'status_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_prov_title'", 'blank': 'True'}),
            'status_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_prov_tf_id'", 'blank': 'True'}),
            'status_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_prov_tf_sys'", 'blank': 'True'}),
            'status_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_prov_tf_title'", 'blank': 'True'}),
            'status_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_title'", 'blank': 'True'})
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
            'datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {'blank': 'True'})
        },
        'indivo.medication': {
            'Meta': {'object_name': 'Medication', '_ormbases': ['indivo.Fact']},
            'endDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'frequency_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'frequency_unit'", 'blank': 'True'}),
            'frequency_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'frequency_value'", 'blank': 'True'}),
            'instructions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_code_id'"}),
            'name_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_code_sys'", 'blank': 'True'}),
            'name_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_code_title'"}),
            'name_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_sc'", 'blank': 'True'}),
            'name_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_title'", 'blank': 'True'}),
            'name_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_tf_id'", 'blank': 'True'}),
            'name_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_tf_sys'", 'blank': 'True'}),
            'name_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_tf_title'", 'blank': 'True'}),
            'name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_title'", 'blank': 'True'}),
            'provenance_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provenance_code_id'", 'blank': 'True'}),
            'provenance_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provenance_code_sys'", 'blank': 'True'}),
            'provenance_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provenance_code_title'", 'blank': 'True'}),
            'provenance_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provenance_prov_sc'", 'blank': 'True'}),
            'provenance_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provenance_prov_title'", 'blank': 'True'}),
            'provenance_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provenance_prov_tf_id'", 'blank': 'True'}),
            'provenance_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provenance_prov_tf_sys'", 'blank': 'True'}),
            'provenance_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provenance_prov_tf_title'", 'blank': 'True'}),
            'provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provenance_title'", 'blank': 'True'}),
            'quantity_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'quantity_unit'", 'blank': 'True'}),
            'quantity_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'quantity_value'", 'blank': 'True'}),
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
            'endDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'name_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_code_id'"}),
            'name_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_code_sys'", 'blank': 'True'}),
            'name_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_code_title'"}),
            'name_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_sc'", 'blank': 'True'}),
            'name_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_title'", 'blank': 'True'}),
            'name_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_tf_id'", 'blank': 'True'}),
            'name_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_tf_sys'", 'blank': 'True'}),
            'name_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_tf_title'", 'blank': 'True'}),
            'name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_title'", 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'startDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'indivo.procedure': {
            'Meta': {'object_name': 'Procedure', '_ormbases': ['indivo.Fact']},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'name_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_code_id'", 'blank': 'True'}),
            'name_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_code_sys'", 'blank': 'True'}),
            'name_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_code_title'", 'blank': 'True'}),
            'name_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_sc'", 'blank': 'True'}),
            'name_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_title'", 'blank': 'True'}),
            'name_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_tf_id'", 'blank': 'True'}),
            'name_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_tf_sys'", 'blank': 'True'}),
            'name_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_prov_tf_title'", 'blank': 'True'}),
            'name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'name_title'", 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'provider_adr_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_adr_city'", 'blank': 'True'}),
            'provider_adr_country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_adr_country'", 'blank': 'True'}),
            'provider_adr_postalcode': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'db_column': "'provider_adr_postalcode'", 'blank': 'True'}),
            'provider_adr_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_adr_region'", 'blank': 'True'}),
            'provider_adr_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_adr_street'", 'blank': 'True'}),
            'provider_bday': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'provider_bday'", 'blank': 'True'}),
            'provider_dea_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_dea_number'", 'blank': 'True'}),
            'provider_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_email'", 'blank': 'True'}),
            'provider_ethnicity': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_ethnicity'", 'blank': 'True'}),
            'provider_gender': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_gender'", 'blank': 'True'}),
            'provider_name_family': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_name_family'", 'blank': 'True'}),
            'provider_name_given': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_name_given'", 'blank': 'True'}),
            'provider_name_middle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_name_middle'", 'blank': 'True'}),
            'provider_name_prefix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_name_prefix'", 'blank': 'True'}),
            'provider_name_suffix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_name_suffix'", 'blank': 'True'}),
            'provider_npi_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_npi_number'", 'blank': 'True'}),
            'provider_preferred_language': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_preferred_language'", 'blank': 'True'}),
            'provider_race': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'provider_race'", 'blank': 'True'}),
            'provider_tel_1_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'provider_tel_1_number'", 'blank': 'True'}),
            'provider_tel_1_preferred_p': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'provider_tel_1_preferred_p'"}),
            'provider_tel_1_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "'provider_tel_1_type'", 'blank': 'True'}),
            'provider_tel_2_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'provider_tel_2_number'", 'blank': 'True'}),
            'provider_tel_2_preferred_p': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'provider_tel_2_preferred_p'"}),
            'provider_tel_2_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'db_column': "'provider_tel_2_type'", 'blank': 'True'}),
            'status_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_code_id'", 'blank': 'True'}),
            'status_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_code_sys'", 'blank': 'True'}),
            'status_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_code_title'", 'blank': 'True'}),
            'status_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_prov_sc'", 'blank': 'True'}),
            'status_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_prov_title'", 'blank': 'True'}),
            'status_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_prov_tf_id'", 'blank': 'True'}),
            'status_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_prov_tf_sys'", 'blank': 'True'}),
            'status_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_prov_tf_title'", 'blank': 'True'}),
            'status_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'status_title'", 'blank': 'True'})
        },
        'indivo.record': {
            'Meta': {'object_name': 'Record'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'record_created_by'", 'null': 'True', 'to': "orm['indivo.Principal']"}),
            'demographics': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Demographics']", 'unique': 'True', 'null': 'True'}),
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
            'chief_complaint': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_visit': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'finalized_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'provider_institution': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'provider_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'signed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'specialty': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'specialty_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'specialty_type': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'specialty_value': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'visit_location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'visit_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'visit_type_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'visit_type_type': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'visit_type_value': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        'indivo.statusname': {
            'Meta': {'object_name': 'StatusName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '24'})
        },
        'indivo.vitalsigns': {
            'Meta': {'object_name': 'VitalSigns', '_ormbases': ['indivo.Fact']},
            'bmi_name_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bmi_name_code_id'", 'blank': 'True'}),
            'bmi_name_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bmi_name_code_sys'", 'blank': 'True'}),
            'bmi_name_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bmi_name_code_title'", 'blank': 'True'}),
            'bmi_name_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bmi_name_prov_sc'", 'blank': 'True'}),
            'bmi_name_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bmi_name_prov_title'", 'blank': 'True'}),
            'bmi_name_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bmi_name_prov_tf_id'", 'blank': 'True'}),
            'bmi_name_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bmi_name_prov_tf_sys'", 'blank': 'True'}),
            'bmi_name_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bmi_name_prov_tf_title'", 'blank': 'True'}),
            'bmi_name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bmi_name_title'", 'blank': 'True'}),
            'bmi_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bmi_unit'", 'blank': 'True'}),
            'bmi_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'bmi_value'", 'blank': 'True'}),
            'bp_diastolic_name_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_diastolic_name_code_id'", 'blank': 'True'}),
            'bp_diastolic_name_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_diastolic_name_code_sys'", 'blank': 'True'}),
            'bp_diastolic_name_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_diastolic_name_code_title'", 'blank': 'True'}),
            'bp_diastolic_name_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_diastolic_name_prov_sc'", 'blank': 'True'}),
            'bp_diastolic_name_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_diastolic_name_prov_title'", 'blank': 'True'}),
            'bp_diastolic_name_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_diastolic_name_prov_tf_id'", 'blank': 'True'}),
            'bp_diastolic_name_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_diastolic_name_prov_tf_sys'", 'blank': 'True'}),
            'bp_diastolic_name_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_diastolic_name_prov_tf_title'", 'blank': 'True'}),
            'bp_diastolic_name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_diastolic_name_title'", 'blank': 'True'}),
            'bp_diastolic_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_diastolic_unit'", 'blank': 'True'}),
            'bp_diastolic_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'bp_diastolic_value'", 'blank': 'True'}),
            'bp_method_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_method_code_id'", 'blank': 'True'}),
            'bp_method_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_method_code_sys'", 'blank': 'True'}),
            'bp_method_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_method_code_title'", 'blank': 'True'}),
            'bp_method_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_method_prov_sc'", 'blank': 'True'}),
            'bp_method_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_method_prov_title'", 'blank': 'True'}),
            'bp_method_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_method_prov_tf_id'", 'blank': 'True'}),
            'bp_method_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_method_prov_tf_sys'", 'blank': 'True'}),
            'bp_method_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_method_prov_tf_title'", 'blank': 'True'}),
            'bp_method_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_method_title'", 'blank': 'True'}),
            'bp_position_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_position_code_id'", 'blank': 'True'}),
            'bp_position_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_position_code_sys'", 'blank': 'True'}),
            'bp_position_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_position_code_title'", 'blank': 'True'}),
            'bp_position_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_position_prov_sc'", 'blank': 'True'}),
            'bp_position_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_position_prov_title'", 'blank': 'True'}),
            'bp_position_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_position_prov_tf_id'", 'blank': 'True'}),
            'bp_position_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_position_prov_tf_sys'", 'blank': 'True'}),
            'bp_position_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_position_prov_tf_title'", 'blank': 'True'}),
            'bp_position_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_position_title'", 'blank': 'True'}),
            'bp_site_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_site_code_id'", 'blank': 'True'}),
            'bp_site_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_site_code_sys'", 'blank': 'True'}),
            'bp_site_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_site_code_title'", 'blank': 'True'}),
            'bp_site_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_site_prov_sc'", 'blank': 'True'}),
            'bp_site_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_site_prov_title'", 'blank': 'True'}),
            'bp_site_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_site_prov_tf_id'", 'blank': 'True'}),
            'bp_site_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_site_prov_tf_sys'", 'blank': 'True'}),
            'bp_site_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_site_prov_tf_title'", 'blank': 'True'}),
            'bp_site_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_site_title'", 'blank': 'True'}),
            'bp_systolic_name_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_systolic_name_code_id'", 'blank': 'True'}),
            'bp_systolic_name_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_systolic_name_code_sys'", 'blank': 'True'}),
            'bp_systolic_name_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_systolic_name_code_title'", 'blank': 'True'}),
            'bp_systolic_name_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_systolic_name_prov_sc'", 'blank': 'True'}),
            'bp_systolic_name_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_systolic_name_prov_title'", 'blank': 'True'}),
            'bp_systolic_name_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_systolic_name_prov_tf_id'", 'blank': 'True'}),
            'bp_systolic_name_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_systolic_name_prov_tf_sys'", 'blank': 'True'}),
            'bp_systolic_name_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_systolic_name_prov_tf_title'", 'blank': 'True'}),
            'bp_systolic_name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_systolic_name_title'", 'blank': 'True'}),
            'bp_systolic_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'bp_systolic_unit'", 'blank': 'True'}),
            'bp_systolic_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'bp_systolic_value'", 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'encounter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['indivo.Encounter']", 'null': 'True', 'blank': 'True'}),
            'fact_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['indivo.Fact']", 'unique': 'True', 'primary_key': 'True'}),
            'head_circ_name_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'head_circ_name_code_id'", 'blank': 'True'}),
            'head_circ_name_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'head_circ_name_code_sys'", 'blank': 'True'}),
            'head_circ_name_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'head_circ_name_code_title'", 'blank': 'True'}),
            'head_circ_name_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'head_circ_name_prov_sc'", 'blank': 'True'}),
            'head_circ_name_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'head_circ_name_prov_title'", 'blank': 'True'}),
            'head_circ_name_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'head_circ_name_prov_tf_id'", 'blank': 'True'}),
            'head_circ_name_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'head_circ_name_prov_tf_sys'", 'blank': 'True'}),
            'head_circ_name_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'head_circ_name_prov_tf_title'", 'blank': 'True'}),
            'head_circ_name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'head_circ_name_title'", 'blank': 'True'}),
            'head_circ_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'head_circ_unit'", 'blank': 'True'}),
            'head_circ_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'head_circ_value'", 'blank': 'True'}),
            'heart_rate_name_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'heart_rate_name_code_id'", 'blank': 'True'}),
            'heart_rate_name_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'heart_rate_name_code_sys'", 'blank': 'True'}),
            'heart_rate_name_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'heart_rate_name_code_title'", 'blank': 'True'}),
            'heart_rate_name_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'heart_rate_name_prov_sc'", 'blank': 'True'}),
            'heart_rate_name_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'heart_rate_name_prov_title'", 'blank': 'True'}),
            'heart_rate_name_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'heart_rate_name_prov_tf_id'", 'blank': 'True'}),
            'heart_rate_name_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'heart_rate_name_prov_tf_sys'", 'blank': 'True'}),
            'heart_rate_name_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'heart_rate_name_prov_tf_title'", 'blank': 'True'}),
            'heart_rate_name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'heart_rate_name_title'", 'blank': 'True'}),
            'heart_rate_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'heart_rate_unit'", 'blank': 'True'}),
            'heart_rate_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'heart_rate_value'", 'blank': 'True'}),
            'height_name_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'height_name_code_id'", 'blank': 'True'}),
            'height_name_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'height_name_code_sys'", 'blank': 'True'}),
            'height_name_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'height_name_code_title'", 'blank': 'True'}),
            'height_name_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'height_name_prov_sc'", 'blank': 'True'}),
            'height_name_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'height_name_prov_title'", 'blank': 'True'}),
            'height_name_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'height_name_prov_tf_id'", 'blank': 'True'}),
            'height_name_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'height_name_prov_tf_sys'", 'blank': 'True'}),
            'height_name_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'height_name_prov_tf_title'", 'blank': 'True'}),
            'height_name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'height_name_title'", 'blank': 'True'}),
            'height_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'height_unit'", 'blank': 'True'}),
            'height_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'height_value'", 'blank': 'True'}),
            'oxygen_saturation_name_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'oxygen_saturation_name_code_id'", 'blank': 'True'}),
            'oxygen_saturation_name_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'oxygen_saturation_name_code_sys'", 'blank': 'True'}),
            'oxygen_saturation_name_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'oxygen_saturation_name_code_title'", 'blank': 'True'}),
            'oxygen_saturation_name_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'oxygen_saturation_name_prov_sc'", 'blank': 'True'}),
            'oxygen_saturation_name_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'oxygen_saturation_name_prov_title'", 'blank': 'True'}),
            'oxygen_saturation_name_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'oxygen_saturation_name_prov_tf_id'", 'blank': 'True'}),
            'oxygen_saturation_name_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'oxygen_saturation_name_prov_tf_sys'", 'blank': 'True'}),
            'oxygen_saturation_name_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'oxygen_saturation_name_prov_tf_title'", 'blank': 'True'}),
            'oxygen_saturation_name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'oxygen_saturation_name_title'", 'blank': 'True'}),
            'oxygen_saturation_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'oxygen_saturation_unit'", 'blank': 'True'}),
            'oxygen_saturation_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'oxygen_saturation_value'", 'blank': 'True'}),
            'respiratory_rate_name_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'respiratory_rate_name_code_id'", 'blank': 'True'}),
            'respiratory_rate_name_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'respiratory_rate_name_code_sys'", 'blank': 'True'}),
            'respiratory_rate_name_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'respiratory_rate_name_code_title'", 'blank': 'True'}),
            'respiratory_rate_name_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'respiratory_rate_name_prov_sc'", 'blank': 'True'}),
            'respiratory_rate_name_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'respiratory_rate_name_prov_title'", 'blank': 'True'}),
            'respiratory_rate_name_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'respiratory_rate_name_prov_tf_id'", 'blank': 'True'}),
            'respiratory_rate_name_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'respiratory_rate_name_prov_tf_sys'", 'blank': 'True'}),
            'respiratory_rate_name_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'respiratory_rate_name_prov_tf_title'", 'blank': 'True'}),
            'respiratory_rate_name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'respiratory_rate_name_title'", 'blank': 'True'}),
            'respiratory_rate_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'respiratory_rate_unit'", 'blank': 'True'}),
            'respiratory_rate_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'respiratory_rate_value'", 'blank': 'True'}),
            'temperature_name_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'temperature_name_code_id'", 'blank': 'True'}),
            'temperature_name_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'temperature_name_code_sys'", 'blank': 'True'}),
            'temperature_name_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'temperature_name_code_title'", 'blank': 'True'}),
            'temperature_name_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'temperature_name_prov_sc'", 'blank': 'True'}),
            'temperature_name_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'temperature_name_prov_title'", 'blank': 'True'}),
            'temperature_name_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'temperature_name_prov_tf_id'", 'blank': 'True'}),
            'temperature_name_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'temperature_name_prov_tf_sys'", 'blank': 'True'}),
            'temperature_name_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'temperature_name_prov_tf_title'", 'blank': 'True'}),
            'temperature_name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'temperature_name_title'", 'blank': 'True'}),
            'temperature_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'temperature_unit'", 'blank': 'True'}),
            'temperature_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'temperature_value'", 'blank': 'True'}),
            'weight_name_code_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'weight_name_code_id'", 'blank': 'True'}),
            'weight_name_code_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'weight_name_code_sys'", 'blank': 'True'}),
            'weight_name_code_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'weight_name_code_title'", 'blank': 'True'}),
            'weight_name_provenance_source_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'weight_name_prov_sc'", 'blank': 'True'}),
            'weight_name_provenance_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'weight_name_prov_title'", 'blank': 'True'}),
            'weight_name_provenance_translation_fidelity_identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'weight_name_prov_tf_id'", 'blank': 'True'}),
            'weight_name_provenance_translation_fidelity_system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'weight_name_prov_tf_sys'", 'blank': 'True'}),
            'weight_name_provenance_translation_fidelity_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'weight_name_prov_tf_title'", 'blank': 'True'}),
            'weight_name_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'weight_name_title'", 'blank': 'True'}),
            'weight_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'weight_unit'", 'blank': 'True'}),
            'weight_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'weight_value'", 'blank': 'True'})
        }
    }

    complete_apps = ['indivo']
