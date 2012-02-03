#!/bin/bash

target=$1
usage="Usage: ./migration_scripts/migrate_indivo <release_target>\nScript must be run from top-level Indivo Server directory.\nValid Targets:\n\tbeta1\n\tbeta2\n\tbeta3\n\t1.0"
arg=""

if [ -z $target ]; then
    echo -e $usage
elif [ $target = 'beta1' ]; then
    echo "Starting Migration to Beta 1"
    arg="0001"
elif [ $target = 'beta2' ]; then
    arg="0004"
    echo "Starting Migration to Beta 2"
elif [ $target = 'beta3' ]; then
    echo "Starting Migration to Beta 3"
    arg="0010"
elif [ $target = '1.0' ]; then
    echo "Starting Migration to v1.0"
    arg="0013"
else
    echo -e $usage
fi

if [ ! -z $arg ]; then

    # Get rid of old Nonces and tokens that will complicate the migration
    python manage.py cleanup_old_tokens

    # Get rid of fact objects: we can reprocess them afterwards
    python manage.py reset_facts drop

    # Run the Migration
    python manage.py migrate indivo $arg

    # Reprocess the documents to get our fact objects back
    python manage.py reset_facts process
fi
