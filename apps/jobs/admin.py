# apps/jobs/admin.py
from django.contrib import admin
from .models import Job
from crm_project.custom_admin import securecrm_admin_site

@admin.register(Job, site=securecrm_admin_site)
class JobAdmin(admin.ModelAdmin):
    list_display       = ("job_number", "title", "status", "client")
    search_fields      = ("job_number", "title")
    autocomplete_fields= ("client",)