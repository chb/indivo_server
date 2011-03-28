#!/bin/bash

###################################
#                                 #
# Usage:                          #
#                                 #
# -b Load bootstrap               #
# -c Load coding systems          #
# -s syncdb                       #
#                                 #
# For all simply run:             #
#                                 #
# ./reset.sh -bcs"                #
#                                 #
###################################


args=`getopt bcs $*`
if test $? != 0; then exit 1; fi
set -- $args
for i
do
  case "$i" in
        -b) LOAD_BS=1;;
        -c) LOAD_CS=1;;
        -s) SYNCDB=1;;
  esac
done

if [ -e "/usr/local/pgsql/bin" ]
then
    PG_PATH="/usr/local/pgsql/bin"
else
    PG_PATH="/usr/bin"
fi

CODING_SYSTEMS=(load-snomedctcore.sql load-hl7-v3-vaccines.sql)

# Assumption is that settings.py is at the same level as manage.py
if [ -e settings.py ]
then
  UP=''
  UTILS_FOLDER='utils/'
elif [ -e ../settings.py ]
then
  UP='../'
  UTILS_FOLDER=''
fi

CS_DATA_PATH=${UP}codingsystems/data
MANAGE_PATH=${UP}manage.py
LOAD_CS_PATH=${UP}load_codingsystems.py
SETTINGS_PATH=${UP}settings.py
IMPORTER_PATH=${UTILS_FOLDER}importer.py

get_settings_info() {
    local  __arg=$1
    SETTINGSCONF=`grep ${__arg} ${SETTINGS_PATH} | cut -d '=' -f2 | cut -d '#' -f1 | tr -d \' | tr -d \ `
    echo $SETTINGSCONF
};

DBNAME=$(get_settings_info DATABASE_NAME)
DBUSER=$(get_settings_info DATABASE_USER)
if [ ! -n $DBUSER ]; then
  DBUSER=`whoami`
fi

createdb() {
  $PG_PATH/createdb -U $DBUSER $DBNAME
};

syncdb(){
  python $MANAGE_PATH syncdb --verbosity 0
  python $MANAGE_PATH migrate
};

load_codingsystems(){
  python $LOAD_CS_PATH
};

reset(){
  drop_create_db && load_indivo_data;
};

drop_create_db(){
  # Drop/Create DB
  if [ -z `psql -U ${DBUSER} ${DBNAME} -q -c "" 2>/dev/null || echo "-"` ]
  then
    $PG_PATH/dropdb -U ${DBUSER} $DBNAME;
    if test $? != 0; then
      echo "Cannot drop current db.  Exiting..." 
      exit 1; 
    fi
    echo "Creating DB ${DBNAME}..." && createdb;
  else
    echo "DB ${DBNAME} does not exist." && \
    echo "Creating DB ${DBNAME}..." && createdb;
  fi
  if test $? != 0; then
    echo "Cannot create current db.  Exiting..." 
    exit 1; 
  fi
};

load_indivo_data(){
  # Load indivo data
  if [[ $SYNCDB = 1 ]]; then
    echo "Syncing DB..." && syncdb;    
    if [[ $LOAD_CS = 1 ]]; then
      echo "Loading coding systems..." && load_codingsystems;
    fi
    if [[ $LOAD_BS = 1 ]]; then
      echo "Loading indivo data..." && python ${IMPORTER_PATH} -v;
    fi
  else
    if [[ $LOAD_BS = 1 || $LOAD_CS = 1 ]]; then
      echo "In order to add to the DB a syncdb operation must occur first, try adding -s"
    fi
  fi
};


reset && exit 0
