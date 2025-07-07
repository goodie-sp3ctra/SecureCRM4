# Imports the Celery application so that Django automatically
# starts it whenever any manage.py command, shell, or gunicorn
# worker boots.

from .celery import app as celery_app   # noqa: F401

__all__ = ("celery_app",)