#!/bin/bash
./manage.py sqlclear cms | ./manage.py dbshell
./manage.py syncdb && ./manage.py loaddata cms
