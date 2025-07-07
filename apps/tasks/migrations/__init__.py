# apps/tasks/__init__.py
"""
Expose the project-wide Celery application as ``tasks.celery_app`` so
`@shared_task` and autodiscovery work anywhere this app is imported.
"""

from crm_project.celery import app as celery_app  # noqa: F401
__all__ = ("celery_app",)