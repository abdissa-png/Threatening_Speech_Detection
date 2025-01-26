#!/bin/bash
export DJANGO_SETTINGS_MODULE=threat_detection.settings
python manage.py migrate --noinput
python manage.py collectstatic --noinput
daphne -b 0.0.0.0 -p 8000 threat_detection.asgi:application