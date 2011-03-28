#!/bin/bash

python manage.py reset_facts drop
python manage.py migrate indivo
python manage.py reset_facts process
