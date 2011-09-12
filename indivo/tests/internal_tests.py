import django.test
from django.conf import settings
from django.db import models
from django.utils.http import urlencode

from indivo.models import *
from indivo.tests.data.reports import TEST_REPORTS
import urls
import re
from xml.dom import minidom

class InternalTests(django.test.TestCase):
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

    def createDocument(self, **kwargs):
        doc = Document.objects.create(**kwargs)
        return doc

    def addAppToRecord(self, **kwargs):
        share = PHAShare.objects.create(**kwargs)
        return share

    def createCarenet(self, **kwargs):
        carenet = Carenet.objects.create(**kwargs)
        return carenet

    def createUserApp(self, test_userapp):
        test_userapp.save()
        return test_userapp.django_obj
    
    def createMachineApp(self, test_machineapp):
        test_machineapp.save()
        return test_machineapp.django_obj

    def createRecord(self, **kwargs):
        record = Record.objects.create(**kwargs)
        record.create_default_carenets()
        return record

    def createAccount(self, test_account):
        account = self.createUninitializedAccount(test_account)
        account.set_username_and_password(username = test_account.username, 
                                          password = test_account.password)
        return account
    
    def createUninitializedAccount(self, test_account):
        test_account.save()
        for label in test_account.records:
            self.createRecord(label=label, owner=test_account.django_obj)
        return test_account.django_obj

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
        
    def createMessage(self, **kwargs):
        message = Message.objects.create(**kwargs)
        return message

    def loadTestReports(self, record):
        for report in TEST_REPORTS:
            report_args = {'record':record,
                           'content':report.xml,
                           'size':report.size(),
                           'digest':report.digest(),
                           'label':report.label,
                           'creator':record.owner}
            self.createDocument(**report_args)

    def setUp(self):
        self.disableAccessControl()
        self.loadModelDependencies()

    def tearDown(self):

        # Delete all models from the DB: Blanket cleanup
        for m in models.get_models():

            # Don't mess with built in django models
            if m.__module__.startswith('django'):
                continue
            
            # Don't delete basic dependencies
            elif m in self.dependencies:
                continue

            else:
                m.objects.all().delete()
