#!/bin/sh

cd /api/

python manage.py migrate
python manage.py generate_geodb

ssh-keygen -t rsa -b 4096 -m PEM -f /api/snow/api/snow/settings/jwtRS256.key -P ""
openssl rsa -in jwtRS256.key -pubout -outform PEM -out /api/snow/api/snow/settings/jwtRS256.key.pub

exec "$@"
