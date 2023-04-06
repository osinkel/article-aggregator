#!/bin/bash

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Make database migrations"
python manage.py makemigrations

echo "Apply database migrations"
python manage.py migrate

echo "Start gunicorn"
gunicorn -c gunicorn.py article_aggregator.wsgi