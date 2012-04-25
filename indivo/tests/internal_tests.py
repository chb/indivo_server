import django.test
from django.conf import settings
from django.test.testcases import disable_transaction_methods, restore_transaction_methods
from django.db.models.loading import cache

from south.db import db

from indivo.data_models import attach_filter_fields
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

class IndivoTests(object):
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

    def create_db_model(self, django_class):
        fields = [(f.name, f) for f in django_class._meta.local_fields]
        table_name = django_class._meta.db_table
        db.create_table(table_name, fields)

    def finish_db_creation(self):
        db.execute_deferred_sql()

    def drop_db_model(self, django_class):
        # Drop the table. Also force a commit, or we'll have trouble with pending triggers in future operations.
        # This means you can ONLY USE THIS FUNCTION IF TRANSACTIONS ARE ENABLED (i.e. in a subclass of 
        # django.test.TransactionTestCase
        table_name = django_class._meta.db_table
        db.start_transaction()
        db.delete_table(table_name)
        db.commit_transaction()

    def remove_model_from_cache(self, modelname):
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

        # Redirect Schema and Datamodel file locations, so we can play with them during tests
        self.save_and_modify_setting('CORE_SCHEMA_DIRS', 
                                     [os.path.join(settings.APP_HOME, 'indivo/tests/schemas/core')])
        self.save_and_modify_setting('CONTRIB_SCHEMA_DIRS',
                                     [os.path.join(settings.APP_HOME, 'indivo/tests/schemas/contrib')])

        self.save_and_modify_setting('CORE_DATAMODEL_DIRS',
                                     [os.path.join(settings.APP_HOME, 'indivo/tests/data_models/core')])
        self.save_and_modify_setting('CONTRIB_DATAMODEL_DIRS',
                                     [os.path.join(settings.APP_HOME, 'indivo/tests/data_models/contrib')])

    def restore_test_settings(self):
        # clear out any test files we created, and restore the MEDIA_ROOT setting
        for subtree in os.listdir(settings.MEDIA_ROOT):
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, subtree))
        self.restore_setting('MEDIA_ROOT')

        # Restore settings for schema and datamodel locations
        self.restore_setting('CORE_SCHEMA_DIRS')
        self.restore_setting('CONTRIB_SCHEMA_DIRS')
        self.restore_setting('CORE_DATAMODEL_DIRS')
        self.restore_setting('CONTRIB_DATAMODEL_DIRS')

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
    
    def load_classes_from_sdml(self, sdml):
        added_classes = []
        
        klasses = [k for k in SDML(sdml).get_output()]
        
        # Make sure the classes are in indivo.models, so we can find them
        indivo_models_module = sys.modules['indivo.models']
        for klass in klasses:
            attach_filter_fields(klass)
            added_classes.append(klass)
            klass.__module__ = 'indivo.models'
            klass.Meta.app_label = 'indivo'
            setattr(indivo_models_module, klass.__name__, klass)

            # Make sure the DB is up to date, so we can save objects
            self.create_db_model(klass)
        self.finish_db_creation()
        
        return added_classes
        
    def unload_classes(self, klasses):
        indivo_models_module = sys.modules['indivo.models']
        for klass in klasses:
            attr = getattr(indivo_models_module, klass.__name__, None)
            if attr:
                del attr

            self.drop_db_model(klass)
            self.remove_model_from_cache(klass.__name__)

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
