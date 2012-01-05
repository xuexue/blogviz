#!/bin/bash
#Author : Jeeyoung Kim
#An example run of dumpdata.

source env.sh;
python manage.py dumpdata --indent=2 auth.User social_auth
