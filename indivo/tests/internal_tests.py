import django.test
from django.conf import settings
from django.db import models
from django.utils.http import urlencode

from indivo.models import *
from indivo.tests.data.reports.lab import *
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
    def disableAccessControl(self):
        self.client.get("/")
        
        # find the right middleware
        for middleware in self.client.handler._view_middleware:
            cls = middleware.__self__.__class__
            if cls.__name__ == 'Authorization':
                cls.override()
                break

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
        share = Share.objects.create(**kwargs)
        return share

    def createCarenet(self, **kwargs):
        carenet = Carenet.objects.create(**kwargs)
        return carenet


    def createPHA(self, **kwargs):
        try:
            if kwargs.has_key('schema'):
                kwargs['schema'] = models.DocumentSchema.objects.get(type=kwargs['schema'])
        except models.DocumentSchema.DoesNotExist:
            del kwargs['schema']
        pha = PHA.objects.create(**kwargs)
        return pha

    def createRecord(self, **kwargs):
        record = Record.objects.create(**kwargs)
        record.create_default_carenets()
        return record
              
    def createAccount(self, username, password, records, **acctargs):
        account = self.createUninitializedAccount(records, **acctargs)
        account.set_username_and_password(username = username, 
                                          password = password)
        return account
    
    def createUninitializedAccount(self, records, **acctargs):
        account = Account.objects.create(**acctargs)
        for label in records:
            self.createRecord(label=label, owner=account)
        return account

    def addDocToCarenet(self, doc, carenet):
        cd = CarenetDocument.objects.create(carenet=carenet, document=doc)
        return cd

    def addAccountToCarenet(self, account, carenet):
        ca = CarenetAccount.objects.create(account=account, carenet=carenet)
        return ca
    
    def addAppToCarenet(self, pha, carenet):
        # make sure PHA is already in record
        try:
            share = carenet.record.shares.get(with_pha__email = pha.email)
        except Share.DoesNotExist:
            share = self.addAppToRecord(record=carenet.record, with_pha=pha)

        return CarenetPHA.objects.create(carenet=carenet, pha=pha)
        
    def createMessage(self, **kwargs):
        message = Message.objects.create(**kwargs)
        return message

    def loadTestLabs(self, record, creator):
        md = hashlib.sha256()
        labs = [lab01, lab02, lab03, lab04]
        for lab in labs:
            md.update(lab)
            lab_args = {'record':record,
                        'content':lab,
                        'size':len(lab),
                        'digest':md.hexdigest(),
                        'label':'testing',
                        'creator':creator}
            self.createDocument(**lab_args)
        return list(Lab.objects.all())
            
        

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
        
    # def test_gettable_urls(self):
    #     patternMapper = {'record_id':str(Record.objects.all()[0].id),
    #                      'carenet_id':str(Carenet.objects.all()[0].id),
    #                      'pha_email':str(PHA.objects.all()[0].email),
    #                      'pha_id':self.carenetId,
    #                      'document_id':self.carenetId,
    #                      'request_token':self.carenetId,
    #                      'account_id':str(Account.objects.all()[0].email),
    #                      'account_email':str(Account.objects.all()[0].email),
    #                      'primary_secret':self.carenetId,
    #                      'secondary_secret':self.carenetId,
    #                      'message_id':self.carenetId,
    #                      'special_document':self.carenetId,
    #                      'short_name':self.carenetId,
    #                      'external_id':self.carenetId,
    #                      'rel_type':self.carenetId,
    #                      'type':self.carenetId,
    #                      'app_id':self.carenetId,
    #                      'app_email':self.carenetId,
    #                      'category':self.carenetId,
    #                      'lab':self.carenetId,
    #                      'function_name':self.carenetId,
    #                      'rel':self.carenetId,
    #                      'lab_code':self.carenetId,
    #                      'other_account_id':self.carenetId,
    #                      'path':self.carenetId,
    #                      'principal_email':self.carenetId,
    #                      'attachment_num':'0',
    #                      'document_id_0':self.carenetId,
    #                      'document_id_1':self.carenetId}

        
    #     allIndivoURLs = {}
        
    #     def show_urls(urllist, parentPath):            
    #         for entry in urllist:
                
    #             if hasattr(entry, 'url_patterns'):
    #                 newParentPath = parentPath + entry.regex.pattern[1:]
    #                 show_urls(entry.url_patterns, newParentPath)
    #             else:
    #                 if isinstance(entry.callback, indivo.lib.utils.MethodDispatcher):
    #                     allIndivoURLs[(parentPath + entry.regex.pattern[1:-1])] = entry.callback.methods.keys()
    #                 else:
    #                     allIndivoURLs[(parentPath + entry.regex.pattern[1:-1])] = ['GET']       
    #     show_urls(urls.urlpatterns, "")
    #     #import pdb;pdb.set_trace()
    #     # match things inside <> that are in the context of (?P< your match >..) 
    #     for url,methods in allIndivoURLs.iteritems():            
    #         testUrl = url
    #         for pattern in re.finditer( '\(\?P<(.*?)>.*?\)', url):
    #             testUrl = testUrl.replace(pattern.group(0),patternMapper[pattern.group(1)])

    #         for method in methods:
    #             #import pdb; pdb.set_trace()
    #             response = getattr(self.client,method.lower())(testUrl, {})
    #             self.assertFalse(response.status_code / 500 > 1)
                
        

    # def test_record(self):
    #     method = 'GET'
    #     testUrl = "records/684b0337-db87-4143-8d55-08800be5126c/reports/minimal/procedures/"
    #     response = getattr(self.client,method.lower())(testUrl,{})
    #     response = getattr(self.client,method.lower())(testUrl,{})
    #     import pdb;pdb.set_trace()
    #     self.assertFalse(response.status_code / 500 > 1)

