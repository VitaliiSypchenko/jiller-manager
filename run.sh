#!/bin/bash
cd shop/
pip install -r requirementstxt
python manage.py collectstatic --noinput
gunicorn jiller_manager.wsgi