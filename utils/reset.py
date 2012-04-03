#!/usr/bin/python

""" 
.. module:: utils.reset
   :synopsis: Script for resetting the Indivo Server Database and loading initial data

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>

"""

# Set up the Django environment
import sys,os
from django.core import management
from django.conf import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))
from django.db import connection, DatabaseError, IntegrityError

from load_codingsystems import load_codingsystems
from utils.importer import import_data

from optparse import OptionParser
import subprocess

# Prepare database-specific commands
CONN_DICT = connection.settings_dict
DB_MODULE, DB_NAME = CONN_DICT['ENGINE'].rsplit('.', 1)

if DB_NAME == 'mysql':
    import _mysql_exceptions as DB_EXCEPTION_MODULE
    CREATE_DB_CMD = 'mysqladmin -u%s -p%s create %s'%(CONN_DICT['USER'],
                                                        CONN_DICT['PASSWORD'],
                                                        CONN_DICT['NAME'])
    DROP_DB_CMD = 'mysqladmin -u%s -p%s drop %s'%(CONN_DICT['USER'],
                                                    CONN_DICT['PASSWORD'],
                                                    CONN_DICT['NAME'])
elif DB_NAME == 'postgresql_psycopg2':
    import psycopg2 as DB_EXCEPTION_MODULE
    CREATE_DB_CMD = 'createdb -U %s -W %s'%(CONN_DICT['USER'], CONN_DICT['NAME'])
    DROP_DB_CMD = 'dropdb -U %s -W %s'%(CONN_DICT['USER'], CONN_DICT['NAME'])

else:
    raise ValueError("Reset Script doesn't support backend %s"%DB_NAME)

def create_db():
    return subprocess.check_call(CREATE_DB_CMD, shell=True)

def drop_db():
    # close django's connection to the database
    connection.close()
    return subprocess.check_call(DROP_DB_CMD, shell=True)

# Parse commandline Arguments
usage = ''' %prog [options]

Reset the Indivo database, optionally loading initial data and codingsystems data. Initial data should
be placed in indivo_server/utils/indivo_data.xml.

Some of the commands (i.e. dropping and creating the database) require authentication to the underlying 
database. If you are prompted for a password, use the password for your database user (the same one you 
specified in settings.py)'''

parser = OptionParser(usage=usage)
parser.add_option("-s", 
                  action="store_true", dest="syncdb", default=True,
                  help="Reset the Database (default behavior).")
parser.add_option("--no-syncdb",
                  action="store_false", dest="syncdb",
                  help="Don't reset the database.")
parser.add_option("-b",
                  action="store_true", dest="load_data", default=True,
                  help="Load initial data from indivo_data.xml, if available (default behavior).")
parser.add_option("--no-data",
                  action="store_false", dest="load_data",
                  help="Don't load initial data from indivo_data.xml.")
parser.add_option("-c", 
                  action="store_true", dest="load_codingsystems", default=False,
                  help="Load codingsystems data, if available.")
parser.add_option("--no-codingsystems", 
                  action="store_false", dest="load_codingsystems",
                  help="Don't load codingsystems data (default behavior).")
parser.add_option("--force-drop", 
                  action="store_true", dest="force_drop", default=False,
                  help="Force a drop and recreate of the database (useful if flushing the database fails).")
parser.add_option("--no-force-drop", 
                  action="store_false", dest="force_drop",
                  help="Don't force a drop and recreate of the database unless necessary (default behavior).")

(options, args) = parser.parse_args()

# Prompt for confirmation--we are about to trash a database, after all
confirm = raw_input("""You have requested a reset of the database.
This will IRREVERSIBLY DESTROY all data currently in the %r database,
and return each table to its initial state.
Are you sure you want to do this?

    Type 'yes' to continue, or 'no' to cancel: """ % CONN_DICT['NAME'])

if confirm != 'yes':
    print "Reset Cancelled."

else:

    # Reset the Database
    if options.syncdb:
        print "RESETTING DATABASE..."

        # Assume the database exists and is synced: try flushing the database
        force_drop = options.force_drop
        if not force_drop:
            try:
                print "Flushing the Database of existing data..."
                management.call_command('flush', verbosity=0, interactive=False)
                management.call_command('migrate', fake=True, verbosity=0)
                print "Database Flushed."

            # Couldn't flush. Either the database doesn't exist, or it is corrupted.
            # Try dropping and recreating, below
            except (DB_EXCEPTION_MODULE.OperationalError, DatabaseError, IntegrityError) as e:
                force_drop = True

            # Unknown exception. For now, just treat same as other exceptions
            except Exception as e:
                force_drop = True
    
        if force_drop:

            # Try dropping the database, in case it existed
            print "Database nonexistent or corrupted, or Database drop requeseted. Attempting to drop database..."
            try:
                drop_db()
            except subprocess.CalledProcessError:
                print "Couldn't drop database. Probably because it didn't exist."
            
            # Create the Database
            print "Creating the Database..."
            try:
                create_db()
            except subprocess.CalledProcessError:
                print "Couldn't create database. Database state likely corrupted. Exiting..."
                exit()

            # Sync the Database
            print "Syncing and Migrating the database..."
            management.call_command('syncdb', verbosity=0)

            # Migrate the Database
            management.call_command('migrate', verbosity=0)
            print "Database Synced."

    # Load codingsystems
    if options.load_codingsystems:
        print "LOADING CODINGSYSTEMS DATA..."
        try:
            load_codingsystems()
            print "LOADED."
        except Exception as e:
            print str(e)
            print "COULDN'T LOAD DATA. SKIPPING."

    # Import initial data
    if options.load_data:
        print "LOADING INITIAL INDIVO DATA..."
        try:
            import_data()
            print "LOADED."
        except Exception as e:
            print str(e)
            print "COULDN'T LOAD DATA. SKIPPING."
