"""
crm_project/celery.py
Celery configuration & autodiscovery.
Run workers with:  celery -A crm_project worker -l info
Run beat with:     celery -A crm_project beat   -l info
"""

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')

app = Celery('crm_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()