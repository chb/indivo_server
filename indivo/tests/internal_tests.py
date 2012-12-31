import django.test
from django.conf import settings
from django.test.testcases import disable_transaction_methods, restore_transaction_methods
from django.db import connection
from django.db.models.loading import cache

from south.db import db

from indivo.data_models import attach_filter_fields, IndivoDataModelLoader
from indivo.models import *
from indivo.tests.data import *
from indivo.lib import iso8601
from indivo.lib.simpledatamodel import SDML

import functools
import os
import os.path
import shutil
import datetime
from xml.dom import minidom
from lxml import etree

class IndivoTests(object):
    TEST_MODEL_MODULE = sys.modules['indivo.models'] # models module to which we can add test datamodels, etc.
    # Add in testing Schema and Datamodel locations
    TEST_SCHEMA_DIR = os.path.join(settings.APP_HOME, 'indivo/tests/schemas/test')
    TEST_DATAMODEL_DIR = os.path.join(settings.APP_HOME, 'indivo/tests/data_models/test')
    dependencies_loaded = False
    dependencies = {DocumentSchema:('document_schemas',['type']),
                    AuthSystem:('auth_systems', ['short_name', 'internal_p']),
                    StatusName:('status_names', ['id', 'name'])}
    dependency_data_sections = {}

    # hackish, like we like it
    def _get_auth_middleware(self):
        self.client.get("/")
        
        # find the right middleware
        for middleware in self.client.handler._view_middleware:
            cls = middleware.__self__.__class__
            if cls.__name__ == 'Authorization':
                return cls

    def disableAccessControl(self):
        mw = self._get_auth_middleware()
        mw.override()

    def enableAccessControl(self):
        mw = self._get_auth_middleware()
        mw.cancel_override()

    def loadModelDependencies(self):
        def get_indivo_data_xml():
            '''Read default data from the indivo_data.xml file'''
            if self.dependency_data_sections:
                return
            data_file = 'utils/indivo_data.xml'
            XMLdata = minidom.parseString(open(settings.APP_HOME + '/' + data_file).read())
            for root in XMLdata.childNodes:
                for section in root.childNodes:
                    if section and hasattr(section, 'nodeName') and section.nodeName != '#text':
                        self.dependency_data_sections[section.nodeName] = section

        def loadDataSection(section, attributes, indivo_model):
            data = self.dependency_data_sections[section]
            for instance in data.childNodes:
                if hasattr(instance, 'getAttribute'):
                    kwargs = {}
                    for attr in attributes:
                        attrval = instance.getAttribute(attr)
                        if attrval.lower() == 'true': attrval = True
                        elif attrval.lower() == 'false': attrval = False
                        kwargs[attr] = attrval
                    indivo_model.objects.get_or_create(**kwargs)                      

        if not self.dependencies_loaded:
            # load xml data for dependencies
            get_indivo_data_xml()

            # Load the data
            for model, ds_info in self.dependencies.iteritems():
                loadDataSection(ds_info[0], ds_info[1], model)

        self.dependencies_loaded = True

    def assertValidSDMXModel(self, model_tag_el, model_tag_attrs, required_fields):
        """ Test that the passed etree._Element validates against the passed arguments.

        Namely, that:

        * The Model tag has all of the attributes/values in **model_tag_attrs**, where
          **model_tag_attrs** is a dict of ``{ 'attribute_name': 'attribute_value' }`` pairs.

        * For each field in **required_fields**, a dict of 
          ``{ 'field_name': (test_func, 'required_value') }`` entries, when ``test_func`` is applied
          to the field named ``'field_name'`` on the Model tag, the output is ``'required_value'``.

        if ``None`` is passed for a value in **required_fields** instead of a ``(test_func, 'required_value')``
        tuple, then the field is checked for existence, but not for correctness.
          
        """

        def check_required_fields(fields, required_fields):
            self.assertEqual(len(fields), len(required_fields))
            self.assertEqual(set([f.get('name') for f in fields]), set(required_fields.keys()))
            for f in fields:
                req_field = required_fields[f.get('name')]
                if req_field:
                    func, val = req_field
                    self.assertEqual(func(f.text), val)
                    
        for attr_name, attr_val in model_tag_attrs.iteritems():
            self.assertEqual(model_tag_el.get(attr_name), attr_val)
        fields = model_tag_el.findall('Field')
        check_required_fields(fields, required_fields)

    def assertTimeStampsAlmostEqual(self, first, second=None, **kwargs):
        """ Test that *first* (a datetime.datetime object) is close in time to *second*.

        kwargs contains arguments for constructing a timedelta object, which defines how
        close the two datetimes should be.

        For example, passing seconds=10, minutes=2 will test that the two dates are within
        2 minutes and 10 seconds of each other.

        By default, the function is run with a constructor of seconds=10, and compared to the
        current time.

        """

        if not second:
            second = datetime.datetime.now()

        defaults = {'seconds':10}
        defaults.update(kwargs)
        td = datetime.timedelta(**defaults)

        if first == second:
            return
        elif first < second and first + td >= second:
            return
        elif first > second and second + td >= first:
            return
        else:
            msg_start = 'Timestamps Not Almost Equal: '
            human_readable_delta = ', '.join(['%s %s'%(v, k) for k,v in defaults.iteritems()])
            msg_main = '%s not within %s of %s.'%(iso8601.format_utc_date(first),
                                                  human_readable_delta,
                                                  iso8601.format_utc_date(second))
            raise self.failureException('%s%s' % (msg_start, msg_main))

    def assertNotRaises(self, exception, call, *args, **kwargs):
        if not hasattr(exception, '__iter__'):
            exception = [exception]
        try:
            result = call(*args, **kwargs)
        except Exception as e:
            for exc in exception:
                if isinstance(e, exc):
                    raise self.failureException('Exception Raised: %s'%e.__class__.__name__)
        return

    def validateIso8601(self, datestring, accept_null = True):
        if not datestring and accept_null:
            return
        else:
            return iso8601.parse_utc_date(datestring)

    def addAppToRecord(self, record, with_pha, carenet=None):
        share = PHAShare.objects.create(record=record, with_pha=with_pha, carenet=carenet)
        return share

    def shareRecordFull(self, record, account):
        return AccountFullShare.objects.create(record=record, with_account=account)

    def addDocToCarenet(self, doc, carenet, share_p=True):
        cd = CarenetDocument.objects.create(carenet=carenet, document=doc, share_p=share_p)
        return cd

    def addAccountToCarenet(self, account, carenet, can_write=False):
        ca = CarenetAccount.objects.create(account=account, carenet=carenet, can_write=can_write)
        return ca
    
    def addAppToCarenet(self, pha, carenet):
        # make sure PHA is already in record
        try:
            share = carenet.record.pha_shares.get(with_pha__email = pha.email)
        except PHAShare.DoesNotExist:
            share = self.addAppToRecord(record=carenet.record, with_pha=pha)

        return CarenetPHA.objects.create(carenet=carenet, pha=pha)

    def relateDocs(self, doc_a, doc_b, rel_type):
        return DocumentRels.objects.create(document_0=doc_a, document_1=doc_b, relationship=rel_type)

    def createDocument(self, test_document_list, index, **overrides):
        return self.createTestItem(test_document_list, index, overrides)

    def createCarenet(self, test_carenet_list, index, **overrides):
        return self.createTestItem(test_carenet_list, index, overrides)

    def createUserApp(self, test_userapp_list, index, **overrides):
        return self.createTestItem(test_userapp_list, index, overrides)
    
    def createMachineApp(self, test_machineapp_list, index, **overrides):
        return self.createTestItem(test_machineapp_list, index, overrides)

    def createRecord(self, test_record_list, index, **overrides):
        record = self.createTestItem(test_record_list, index, overrides)
        record.create_default_carenets()
        return record

    def createAccount(self, test_account_list, index, **overrides):
        account = self.createUninitializedAccount(test_account_list, index, **overrides)
        account.set_username_and_password(username = test_account_list[index]['username'], 
                                          password = test_account_list[index]['password'])
        return account
    
    def createUninitializedAccount(self, test_account_list, index, **overrides):
        return self.createTestItem(test_account_list, index, overrides)

    def createMessage(self, test_message_list, index, **overrides):
        return self.createTestItem(test_message_list, index, overrides)

    def createAttachment(self, test_attachment_list, index, **overrides):
        return self.createTestItem(test_attachment_list, index, overrides)

    def createAuthSystem(self, test_authsystem_list, index, **overrides):
        return self.createTestItem(test_authsystem_list, index, overrides)

    def loadTestReports(self, **overrides):
        for i in range(len(TEST_REPORTS)):
            self.createTestItem(TEST_REPORTS, i, overrides)

    def createTestItem(self, test_item_list, index, overrides_dict={}):
        tdi = TestDataItem(index, data_list=test_item_list)
        scoped_test_model = self.test_data_context.add_model(tdi, **overrides_dict)
        try:
            model_obj = scoped_test_model.save()
        except Exception:
            
            # remove the failed item from our context
            self.test_data_context.del_model(scoped_test_model.identifier, 
                                             scoped_test_model.subcontext_id)
            raise

        return model_obj

    def check_unsupported_http_methods(self, invalid_methods, url):
        for method_name in invalid_methods:
            method_func = getattr(self.client, method_name)
            response = method_func(url)
            self.assertEquals(response.status_code, 405)

    def remove_model_from_cache(self, modelname):
        """ Delete a model from Django's internal cache. """
        try:
            del cache.app_models['indivo'][modelname]
        except KeyError:
            pass

    def save_setting(self, setting_name):
        curr_val = getattr(settings, setting_name, None)
        if self.saved_settings.has_key(setting_name):
            raise ValueError("Already saved setting %s, can't save it again"%setting_name)
        self.saved_settings[setting_name] = curr_val        

    def save_and_modify_setting(self, setting_name, setting_val):
        self.save_setting(setting_name)
        setattr(settings, setting_name, setting_val)

    def restore_setting(self, setting_name):
        old_val = self.saved_settings.get(setting_name, None)
        if not old_val:
            raise ValueError("Cannot restore setting %s, which was never saved"%setting_name)
        setattr(settings, setting_name, old_val)


    def setup_test_settings(self):
        self.saved_settings = {}

        # Redirect settings.MEDIA_ROOT, so flat files are saved separately
        # from existing files
        test_media_root = os.path.join(settings.APP_HOME, 'indivo/tests/test_files')
        if not os.path.exists(test_media_root):
            os.makedirs(test_media_root)
        self.save_and_modify_setting('MEDIA_ROOT', test_media_root)

    def restore_test_settings(self):
        # clear out any test files we created, and restore the MEDIA_ROOT setting
        for subtree in os.listdir(settings.MEDIA_ROOT):
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, subtree))
        self.restore_setting('MEDIA_ROOT')

    def setUp(self):
        self.test_data_context = TestDataContext()
        self.disableAccessControl()
        self.loadModelDependencies()
        self.setup_test_settings()

    def tearDown(self):
        self.restore_test_settings()

class InternalTests(IndivoTests, django.test.TestCase):
    """ subclass of Django's TestCase with access to useful utils 
        specific to Indivo tests (model creation, access control overrides, etc.).
        Doesn't allow transaction management in tests. """
    pass

class TransactionInternalTests(IndivoTests, django.test.TransactionTestCase):
    """ subclass of Django's TransactionTestCase with access to useful utils 
    specific to Indivo tests (model creation, access control overrides, etc.).
    Allows transaction management in tests. 

    WARNING: Transaction Tests are VERY slow. Only use this if you really need
    to test transactions. If you just need to deal with IntegrityErrors by
    calling rollback, see enable_transactions below. """
    
    def load_model_dir(self, dirpath):
        """ Load data models from a directory (like we do when running Indivo normally). """
        loader = IndivoDataModelLoader(dirpath)
        models = [model_class for model_name, model_class in loader.discover_data_models()]
        self.load_models(models)
        return models
 
    def unload_model_dir(self, dirpath):
        """ Unload data models that have been loaded from a directory."""
        loader = IndivoDataModelLoader(dirpath)
        models = [model_class for model_name, model_class in loader.discover_data_models()]
        self.unload_models(models)

    def load_models_from_sdml(self, sdml):
        """ Load data models from an SDML literal. """
        models = [] 
        for model in SDML(sdml).get_output():
            attach_filter_fields(model)
            models.append(model)
        self.load_models(models)
        return models
        
    def load_models(self, models):
        """ Do the heavy lifting for loading data models.
        
        Registers the models, then migrates the DB to support them.

        """

        loader = IndivoDataModelLoader('')
        for m in models:

            # Register the model in indivo.models
            loader.add_model_to_module(m.__name__, m, self.TEST_MODEL_MODULE)

            # Migrate the database to contain the model
            db.start_transaction()
            try:
                self.create_db_model(m)
            except Exception, e:
                db.rollback_transaction()
            else:
                db.commit_transaction()
        self.finish_db_creation()

    def unload_models(self, models):
        """ Do the heavy lifting for unloading data models.
        
        Unregisters the models, then migrates the DB to remove them.
        
        """

        for m in models:

            # Unregister the model from indivo.models
            delattr(self.TEST_MODEL_MODULE, m.__name__)

            # Remove the model from django's internal model cache
            self.remove_model_from_cache(m.__name__)

            # Migrate the database to no longer contain the model
            db.start_transaction()
            try:
                self.drop_db_model(m)
            except Exception, e:
                db.rollback_transaction()
            else:
                db.commit_transaction()

    def create_db_model(self, django_class):
        """ Migrate the DB to support a single model. """
        fields = [(f.name, f) for f in django_class._meta.local_fields]
        table_name = django_class._meta.db_table
        db.create_table(table_name, fields)
        
        # create any ManyToMany tables
        for m2m_field in django_class._meta.many_to_many:
            m2m_table_name = m2m_field.m2m_db_table()
            if m2m_table_name not in connection.introspection.table_names():
                # build list of fields in the m2m "through" table
                m2m_fields = [(f.name, f) for f in getattr(django_class, m2m_field.name).through._meta.local_fields]
                db.create_table(m2m_field.m2m_db_table(), m2m_fields)
        

    def finish_db_creation(self):
        """ Exceute deferred SQL after creating several models. 
        
        MUST BE CALLED after self.create_db_model()
        
        """

        db.execute_deferred_sql()

    def drop_db_model(self, django_class):
        """ Migrate the DB to remove a single model. """
        # Drop the table. Also force a commit, or we'll have trouble with pending triggers in future operations.
        table_name = django_class._meta.db_table
        db.start_transaction()
        db.delete_table(table_name)
        
        # drop any ManyToMany tables
        for m2m_field in django_class._meta.many_to_many:
            m2m_table_name = m2m_field.m2m_db_table()
            if m2m_table_name in connection.introspection.table_names():
                # delete table if it exists
                db.delete_table(m2m_table_name)
        
        db.commit_transaction()

def enable_transactions(func):
    """ Hackish decorator that re-enables transaction management in tests
        from subclasses of django.test.TestCase (where transaction 
        management is disabled by default). We're doing this instead of 
        subclassing django.test.TransactionTestCase because TransactionTestCase 
        is prohibitively slow.

        WARNING: DO NOT COMMIT, as this will break Django's DB resets
        between tests. This class should only be used for tests that
        require periodic rollbacks. 

        WARNING: DO NOT CALL TRANSACTION-MANAGED CODE in tests with this decorator,
        as they will probably call commit. This includes the @commit-on-success 
        style decorators.

        WARNING: If you use this decorator, you are responsible for making sure
        that the DB is clean afterwards. django.test.TestCase will call one
        final rollback after your test method, and if the database isn't clean
        after that call, you're in trouble. """

    def _enable_transactions(*args, **kwargs):
        restore_transaction_methods()
        try:
            ret = func(*args, **kwargs)
        except:
            raise
        finally:
            disable_transaction_methods()

        return ret

    return functools.update_wrapper(_enable_transactions, func)
