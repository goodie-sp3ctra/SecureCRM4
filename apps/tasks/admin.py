# apps/taks/admin.py
from django.contrib import admin
from .models import Task
from crm_project.custom_admin import securecrm_admin_site
from apps.customers.models import Client
from apps.jobs.models import Job


@admin.register(Task, site=securecrm_admin_site)
class TaskAdmin(admin.ModelAdmin):
    list_display  = ("title", "priority", "client", "due", "is_overdue", "completed_at")
    list_filter   = ("priority", "client")
    search_fields = ("title", "client__company_name")
    list_editable = ("priority", "due")
    autocomplete_fields = ("client", "job")
    readonly_fields = ("created_at",)

@admin.display(boolean=True)
def is_overdue(self, obj):
        return obj.is_overdue()
