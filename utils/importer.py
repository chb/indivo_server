import os
import sys
from xml.dom import minidom
import datasections
from django.conf import settings
from indivo.models import PHA, MachineApp

class AppSyncer(object):
	def __init__(self, app_paths=None):
		self.app_paths = app_paths or settings.APPS_DIRS
		self.db_phas = dict([(app.email, app) for app in PHA.objects.all()])
		self.db_machine_apps = dict([(app.email, app) for app in MachineApp.objects.all()])

	def sync(self, verbosity=True):
		ui_app_paths = self.app_paths['ui']
		admin_app_paths = self.app_paths['admin']
		user_app_paths = self.app_paths['user']
    
		# sync the UI apps
		for path in ui_app_paths:
			self.sync_app_dir(path, user_app=False, verbosity=verbosity)

		# sync the admin apps
		for path in admin_app_paths:
			self.sync_app_dir(path, user_app=False, verbosity=verbosity)

		# sync the user apps
		for path in user_app_paths:
			self.sync_app_dir(path, verbosity=verbosity)

		# delete all apps that weren't registered
		for app_email, app in self.db_phas.iteritems():
			print "\tUser App %s no longer registered. Deleting..." % app.email
			app.delete()

		for app_email, app in self.db_machine_apps.iteritems():
			print "\tMachine App %s no longer registered. Deleting..." % app.email
			app.delete()

	def sync_app_dir(self, dir_path, user_app=True, verbosity=True):
		for app_dir in os.listdir(dir_path):
			full_app_path = os.path.join(dir_path, app_dir)
			if os.path.isdir(full_app_path):
				self.sync_app(full_app_path, user_app=user_app, verbosity=verbosity)

	def sync_app(self, full_path, user_app=True, verbosity=True):
		manifest_fp = os.path.join(full_path, 'manifest.json')
		credentials_fp = os.path.join(full_path, 'credentials.json')

		if verbosity:
			print "\tProcessing %s App %s..." % ("User" if user_app else "Machine", os.path.basename(full_path))
  
		try:
			with open(manifest_fp, 'r') as f:
				manifest = f.read()
			with open(credentials_fp, 'r') as f:
				credentials = f.read()
    
			app_klass = PHA if user_app else MachineApp
			app = app_klass.from_manifest(manifest, credentials, save=False)

			app_dict = self.db_phas if user_app else self.db_machine_apps
			db_app = app_dict.get(app.email, None)

			# if the app already exists, just update it
			if db_app:				
				if verbosity:
					print "\t\tApp exists. Updating... "
					
				# update all the necessary fields
				app.id = db_app.id
				app.created_at = db_app.created_at
				app.creator = db_app.creator
				
				# mark the app as synced
				del app_dict[app.email]

			elif verbosity:
				print "\t\tNew app. Registering... "
    
			app.save()

		except Exception as e:
			if verbosity:
				print "\t\tError loading app: %s. Skipping..."%str(e)
			return None

def import_data(verbosity=True):
  bf_prefix = ''
  if os.path.dirname(__file__):
    bf_prefix = os.path.dirname(__file__) + '/'
    data_file  = bf_prefix + 'indivo_data.xml'

  if os.path.isfile(data_file):
    f = open(data_file)
    lines = []
    for line in f:
      lines.append(line.strip())
    dom = minidom.parseString(''.join(lines))
    for root in dom.childNodes:
      # Make sure to pull in required info first
      # This is hack, but the required stuff shouldn't
      # really be in the data file anyways.
      
      # Required info is auth_systems, status_names, document_schemas
      req_secs = ['auth_systems', 'status_names', 'document_schemas']

      for section in root.childNodes:
        if section and getattr(section, 'nodeName', None) in req_secs:
          import_section(section, verbosity)

      # Now import the others
      for section in root.childNodes:
        if section and getattr(section, 'nodeName', None) not in req_secs:
          import_section(section, verbosity)
  else:
    raise ValueError("No indivo_data.xml file found")

def import_section(section, verbosity):
  try:
    # Note the nodeName, className and fileName relationship
    if hasattr(section, 'nodeName'):
      if hasattr(datasections, section.nodeName):
        class_name = section.nodeName.capitalize()
        seclib = getattr(datasections, section.nodeName)
        if hasattr(seclib, class_name):
          getattr(seclib, class_name)(section, verbosity)
  except ImportError:
    pass

