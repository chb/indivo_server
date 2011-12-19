""" The Indivo Application.

A Django app which implements a Personally-Controlled Health Record platform,
exposing an oAuth authenticated, RESTful API for substitutable medical apps.

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>
.. moduleauthor:: Ben Adida <ben@adida.net>

"""

AUTHORIZATION_MODULE_LOADED = False

def check_safety():
  """ Ensure that the Authorization Module is in place before serving API calls."""
  if not AUTHORIZATION_MODULE_LOADED:
    raise Exception("Authorization Module not loaded, refusing to serve.")
