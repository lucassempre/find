#!/bin/sh

cd /api/

python manage.py migrate
python manage.py generate_geodb
exec "$@"
