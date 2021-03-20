#!/bin/sh
# python manager.py db migrate -m "how"
python manager.py db migrate
python manager.py db upgrade
gunicorn --bind=0.0.0.0:8080 --log-level info --workers 4 detectweb.wsgi:application
