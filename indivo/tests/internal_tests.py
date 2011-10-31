import django.test
from django.conf import settings
from django.test.testcases import disable_transaction_methods, restore_transaction_methods

from indivo.models import *
from indivo.tests.data import *

import functools
import os
import os.path
import shutil
from xml.dom import minidom

ORIGINAL_MEDIA_ROOT = settings.MEDIA_ROOT

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

    def setUp(self):
        self.test_data_context = TestDataContext()
        self.disableAccessControl()
        self.loadModelDependencies()

        # Redirect settings.MEDIA_ROOT, so flat files are saved separately
        # from existing files
        self.old_media_root = ORIGINAL_MEDIA_ROOT
        new_path = os.path.join(self.old_media_root, 'test_files')
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        settings.MEDIA_ROOT = new_path

    def tearDown(self):
        
        # clear out any test files we created
        for subtree in os.listdir(settings.MEDIA_ROOT):
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, subtree))

        # reset settings.MEDIA_ROOT
        settings.MEDIA_ROOT = self.old_media_root

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
    pass

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
        ret = func(*args, **kwargs)
        disable_transaction_methods()
        return ret

    return functools.update_wrapper(_enable_transactions, func)
