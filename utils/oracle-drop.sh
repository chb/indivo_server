#!/bin/bash
python manage.py sqlclear codingsystems | sqlplus system/test@xe
python manage.py sqlclear indivo | sqlplus system/test@xe