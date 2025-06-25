# apps/activity/apps.py
from django.apps import AppConfig

class ActivityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.activity'            # <-- must match your folder structure
    verbose_name = "Activity Feed"

    def ready(self):
        import apps.activity.signals  # noqa
