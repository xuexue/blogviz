#!/bin/bash
source env.sh;
python manage.py test --settings=settings_testing bviz
