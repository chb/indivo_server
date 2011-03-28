
AUTHORIZATION_MODULE_LOADED = False

def check_safety():
  if not AUTHORIZATION_MODULE_LOADED:
    raise Exception("Authorization Module not loaded, refusing to serve.")
