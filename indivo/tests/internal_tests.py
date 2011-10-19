import django.test
from django.conf import settings
from django.db import models
from django.utils.http import urlencode

from indivo.models import *
from indivo.tests.data import *

import urls
import re
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

    def addAppToRecord(self, **kwargs):
        share = PHAShare.objects.create(**kwargs)
        return share

    def shareRecordFull(self, record, account):
        return AccountFullShare.objects.create(record=record, with_account=account)

    def addDocToCarenet(self, doc, carenet):
        cd = CarenetDocument.objects.create(carenet=carenet, document=doc)
        return cd

    def addAccountToCarenet(self, account, carenet):
        ca = CarenetAccount.objects.create(account=account, carenet=carenet)
        return ca
    
    def addAppToCarenet(self, pha, carenet):
        # make sure PHA is already in record
        try:
            share = carenet.record.pha_shares.get(with_pha__email = pha.email)
        except PHAShare.DoesNotExist:
            share = self.addAppToRecord(record=carenet.record, with_pha=pha)

        return CarenetPHA.objects.create(carenet=carenet, pha=pha)

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

    def loadTestReports(self, **overrides):
        for i in range(len(TEST_REPORTS)):
            self.createTestItem(TEST_REPORTS, i, overrides)

    def createTestItem(self, test_item_list, index, overrides_dict={}):
        tdi = TestDataItem(index, data_list=test_item_list)
        try:
            scoped_test_model = self.test_data_context.add_model(tdi, **overrides_dict)
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

    def tearDown(self):
        pass

class InternalTests(IndivoTests, django.test.TestCase):
    """ subclass of Django's TestCase with access to useful utils 
        specific to Indivo tests (model creation, access control overrides, etc.).
        Doesn't allow transaction management in tests. """
    pass

class TransactionInternalTests(IndivoTests, django.test.TransactionTestCase):
    """ subclass of Django's TransactionTestCase with access to useful utils 
        specific to Indivo tests (model creation, access control overrides, etc.).
        Allows transaction management in tests. """
    pass
