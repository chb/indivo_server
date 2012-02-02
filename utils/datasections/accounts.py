import sys
from indivo import models
from indivo.lib.sample_data import IndivoDataLoader

class Accounts:
  LABELS = 'labels'

  account_tags = ('email', 'full_name', 'contact_email', 'username', 'password', 'records')

  def __init__(self, elements, verbosity):
    self.verbosity = verbosity
    self.process_accounts(elements)

  def process_accounts(self, elements):
    accounts = []
    for node in elements.childNodes:
      account = {}
      account_email = node.getAttribute(self.account_tags[0])
      account[self.account_tags[0]] = account_email
      if self.verbosity:
        print "\tAdding account: ", account_email
      for tag_name in self.account_tags:
        if tag_name == self.account_tags[-1]:
          records_node = node.getElementsByTagName(self.account_tags[-1])[0]
          if records_node and records_node.hasChildNodes:
            account[self.LABELS] = []
            for record in records_node.childNodes:
              account[self.LABELS].append((record.getAttribute('label'), 
                                           record.getAttribute('data_profile')))
        elem_node = node.getElementsByTagName(tag_name)
        if elem_node and len(elem_node) > 0 and elem_node[0].firstChild:
          account[tag_name] = elem_node[0].firstChild.nodeValue
      accounts.append(account)
    return self.create_accounts(accounts)

  def create_accounts(self, accounts):
    for acct_info in accounts:
      account, account_created = models.Account.objects.get_or_create( 
                                      email         = acct_info['email'], 
                                      full_name     = acct_info['full_name'], 
                                      contact_email = acct_info['contact_email'])
      if account_created:
        account.set_username_and_password(  username = acct_info['username'], 
                                            password = acct_info['password'])
        if acct_info.has_key(self.LABELS):
          for label, data_profile in acct_info[self.LABELS]:
            record, record_created = models.Record.objects.get_or_create(owner = account, label = label)
            if record_created:
              record.create_default_carenets()

              if data_profile:
                if self.verbosity:
                  print "\tLoading data profile %s for record %s"%(data_profile, label)
                loader = IndivoDataLoader(models.NoUser.objects.get_or_create(email="", 
                                                                              type='NoUser')[0])
                try:
                  loader.load_profile(record, data_profile)
                except Exception, e:
                  if self.verbosity:
                    print "\t\tError loading profile: %s"%str(e)
    return True
