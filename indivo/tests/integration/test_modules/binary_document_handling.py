import os
import data

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

def test_binary_document_handling(IndivoClient):
  PRD = 'prd'
  try:
    test_file_name = 'xxsmall_binary.chp'
    test_file_location = THIS_DIR + '/../files/'
    test_file = test_file_location + test_file_name
    
    user_client = IndivoClient(data.app_email, data.app_secret)
    user_client.set_app_id(data.app_email)
    if not os.path.exists(test_file):
      raise Exception, test_file_name + ' does not exist'
    else:
      try:
        import fileinput
        lines = ''.join([line for line in fileinput.input(test_file)])
      except ImportError:
        f = open(test_file)
        lines = ''.join([line for line in f])
      doc_id = user_client.post_app_document(data=lines)
  except Exception, e:
    return False, e
  return True

