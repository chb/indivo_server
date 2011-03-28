"""
Management of the App, hooks for django
"""

from django.dispatch import dispatcher
from django.db.models import get_models, signals

def setup_bootstrap(app, created_models, verbosity, **kwargs):
  try:
    import bootstrap
  except ImportError:
    # Ignore a missing bootstrap
    pass

# add the dispatcher to set things up
signals.post_syncdb.connect(setup_bootstrap)
