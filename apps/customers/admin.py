# apps/customers/admin.py
from django.contrib import admin
from .models import Client
from crm_project.custom_admin import securecrm_admin_site

@admin.register(Client, site=securecrm_admin_site)
class ClientAdmin(admin.ModelAdmin):
    list_display  = ("company_name", "contact_name", "status")
    search_fields = ("company_name", "contact_name", "contact_email")
