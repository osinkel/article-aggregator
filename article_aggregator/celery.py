from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE','article_aggregator.settings')
app = Celery('article_aggregator', include=['aggregator.tasks'])
app.conf.timezone = 'UTC'
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()