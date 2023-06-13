#!/bin/bash
echo "Collect static files"
python manage.py collectstatic --noinput

echo "Make database migrations"
python manage.py makemigrations

echo "Apply database migrations"
python manage.py migrate

echo "Migrations for celery"
python manage.py migrate django_celery_results

echo "Creating super user"
echo "from django.contrib.auth import get_user_model; from config import DB_ADMIN_PASSWORD; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', DB_ADMIN_PASSWORD)" | python manage.py shell

echo "Start gunicorn"
gunicorn -c gunicorn.py article_aggregator.wsgi