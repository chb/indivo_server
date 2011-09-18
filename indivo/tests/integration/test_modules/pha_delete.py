import data

def test_pha_delete(IndivoClient):
  try:
    chrome_client = IndivoClient('chrome', 'chrome')
    # SZ: 403 expected since app_id != client
    chrome_client.delete_app(app_id='problems@apps.indivo.org')
  except Exception, e:
    return False, e
  return True
