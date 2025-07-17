# crm_project/custom_admin.py
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

class SecureCRMAdminSite(AdminSite):
    site_header  = _("SecureCRM – Admin")
    site_title   = _("SecureCRM Admin")
    index_title  = _("Control Panel")
    login_template = "admin/login.html"

    def each_context(self, request):
        # only import models here to avoid pulling in app admin modules at import-time
        from apps.invoices.models import Invoice
        from apps.tasks.models     import Task

        ctx = super().each_context(request)
        ctx.update({
            "invoices":          Invoice.objects.count(),
            "overdue_invoices":  Invoice.objects.filter(status=Invoice.OVERDUE).count(),
            "tasks_open":        Task.objects.filter(completed_at__isnull=True).count(),
        })
        return ctx

securecrm_admin_site = SecureCRMAdminSite(name="securecrm_admin")