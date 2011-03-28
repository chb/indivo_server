import sys
import hashlib
import string
from indivo.models import PHA
from indivo.models import Account
from indivo.models import Record
from indivo.models import DocumentSchema

#Order on the arguments: pha_name, contact_email, pha_start_url_template, pha_callback_url


class PHA_Creation:

  def __init__(self, pha_name, pha_start_url_template, pha_callback_url):
    self.pha_name = pha_name.capitalize()
    self.pha_key = pha_name.lower()
    self.pha_secret = self.generate_secret(pha_name)
    self.pha_description = 'default description'
    self.pha_start_url_template = pha_start_url_template
    self.pha_callback_url = pha_callback_url
    self.pha_email = pha_name + '@apps.indivo.org'
    self.pha_frameable = True
    self.pha_has_ui = True
    self.pha_document_schema = pha_name.capitalize()

  def generate_secret(self, name):
    return hashlib.sha1(name + 'indivo_test:abcdefg123').hexdigest()[0:12]

  def create_pha(self): 
    try:
      #try:
      #  pha_document_schema = DocumentSchema.objects.get(type=self.pha_document_schema)
      #except DocumentSchema.DoesNotExist:
      #  DocumentSchema.objects.create(type=self.pha_document_schema)

      try:
        pha = PHA.objects.get(consumer_key=self.pha_key)
      except PHA.DoesNotExist:
        pha = PHA.objects.create( consumer_key=self.pha_key, 
                                  secret=self.pha_secret, 
                                  name=self.pha_name,
                                  description=self.pha_description,
                                  start_url_template=self.pha_start_url_template,
                                  callback_url=self.pha_callback_url,
                                  email=self.pha_email,
                                  frameable=self.pha_frameable,
                                  has_ui=self.pha_has_ui,
                                  schema=None)
        return pha
    except:
      return False

def get_argv(index):
  if len(sys.argv) > index:
    return sys.argv[index]
  return ''

def create_accounts_and_records(pha_create_obj, pha_name, contact_email):
  domain = '@x-staging.indivo.org'
  user_list = ['user_1', 'user_2', 'user_3']
  for user in user_list:
    username = pha_name + '_' + user
    password = pha_create_obj.generate_secret(pha_name + user)
    account = Account.objects.create( email=username + domain, 
                                      full_name=pha_name, 
                                      contact_email=contact_email)
    account.set_username_and_password(username=username, password=password)
    record = Record.objects.create(owner=account, label=username)
    print "\n"
    print "Account: " + username + domain
    print "Password: " + password
    print "Record: " + record.id
    print "="*50

if __name__ == '__main__':
  pha_name                = ''
  pha_callback_url        = ''
  pha_start_url_template  = ''
  pha_name, contact_email, pha_start_url_template, pha_callback_url = get_argv(1), get_argv(2), get_argv(3), get_argv(4)
  if pha_name and contact_email:
    pha_create_obj = PHA_Creation(pha_name, pha_start_url_template, pha_callback_url)
    pha = pha_create_obj.create_pha()
    if pha:
      print 'pha creation successful'
      print "Consumer Key: " + pha.consumer_key
      print "Consumer Secret: " + pha.secret
      print "PHA Name: " + pha.name
      print "PHA Description: " + pha.description
      print "PHA Start URL Template: " + pha.start_url_template
      print "PHA Callback URL: " + pha.callback_url
      print "PHA Email: " + pha.email
      print "PHA Frameable: " + str(pha.frameable)
      print "PHA HasUI: " + str(pha.has_ui)
      print "PHA Document Schema: None"

      create_accounts_and_records(pha_create_obj, pha_name, contact_email)
    else:
      print "A PHA by this name already exists"
