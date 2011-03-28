from indivo import models

class Accounts:
  LABELS = 'labels'

  account_tags = ('email', 'full_name', 'contact_email', 'username', 'password', 'records')

  def __init__(self, elements, verbosity):
    self.process_accounts(elements, verbosity)

  def process_accounts(self, elements, verbosity):
    accounts = []
    for node in elements.childNodes:
      account = {}
      account_email = node.getAttribute(self.account_tags[0])
      account[self.account_tags[0]] = account_email
      if verbosity:
        print "\tAdding account: ", account_email
      for tag_name in self.account_tags:
        if tag_name == self.account_tags[-1]:
          records_node = node.getElementsByTagName(self.account_tags[-1])[0]
          if records_node and records_node.hasChildNodes:
            account[self.LABELS] = []
            for record in records_node.childNodes:
              account[self.LABELS].append(record.getAttribute('label'))
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
          for label in acct_info[self.LABELS]:
            record, record_created = models.Record.objects.get_or_create(owner = account, label = label)
            if record_created:
              record.create_default_carenets()
    return True
