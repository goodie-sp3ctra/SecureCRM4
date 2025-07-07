# apps/invoices/admin.py
from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display    =   ("invoice_number", "client", "issue_date", "due_date", "total", "status")
    list_filter     =   ("status", "issue_date", "due_date")
    search_fields   =   ("invoice_number", "client__name")
    ordering        =   ("invoice_number",)