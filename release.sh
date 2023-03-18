#!/usr/bin/bash
set -ex
python manage.py migrate --no-input
python manage.py collectstatic --no-input
