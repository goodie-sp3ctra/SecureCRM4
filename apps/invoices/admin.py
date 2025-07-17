# apps/invoices/admin.py
from django.contrib import admin
from .models import Invoice
from django.utils import timezone
from django.utils.html import format_html
from crm_project.custom_admin import securecrm_admin_site

@admin.register(Invoice, site=securecrm_admin_site)
class InvoiceAdmin(admin.ModelAdmin):
    list_display    =   ("invoice_number", "client", "issue_date", "due_date", "total", "status")
    list_filter     =   ("status", "issue_date", "due_date")
    search_fields   =   ("invoice_number", "client__name")
    date_hierarchy  =   "issue_date"
    ordering        =   ("invoice_number",)

    readonly_fields =   ("created_at", "updated_at", "paid_at")

# colourise status
def status_colored(self, obj):
    color_map = {"draft":"#999","sent":"#1e90ff","paid":"#22bb33","overdue":"#e74c3c"}
    return format_html('<b style="color:{}">{}</b>', color_map[obj.status], obj.get_status_display())
status_colored.short_description = "Status"

# quick actions
actions = ["mark_paid", "resend_invoice", "export_pdf"]

@admin.action(description="Mark selected invoices PAID")
def mark_paid(self, request, queryset):
    updated = queryset.update(status=Invoice.PAID, paid_at=timezone.now())
    self.message_user(request, f"{updated} invoice(s) marked paid")

@admin.action(description="E-mail PDF again")
def resend_invoice(self, request, qs):
    for inv in qs:  inv.send_email()
    self.message_user(request, f"Queued {qs.count()} e-mails")