#!/bin/bash
# Run this script to set up environment variables required for django / python.
export PYTHONPATH=`pwd`:`pwd`/thirdparty/django-social-auth/
export DJANGO_SETTINGS_MODULE='settings'
