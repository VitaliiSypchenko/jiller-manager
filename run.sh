#!/bin/bash

python manage.py makemigrations

# migrate db, so we have the latest db schema
python manage.py migrate

# load fixutres
#su -m myuser -c "python manage.py loaddata project/fixtures/init_data.json"

# Collect static
python manage.py collectstatic --noinput

# start development server on public ip interface, on port 8000
gunicorn -b 0.0.0.0:8000 jiller_manager.wsgi
