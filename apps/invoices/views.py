# apps/invoices/views.py
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from crm_project.email_utils import send_templated_email
from .models import Invoice
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

class InvoiceResendView(View):
    model = Invoice
    http_method_names = ["post"]  # only allow POST
    def post(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        send_templated_email(
            to=invoice.client.email,
            subject_template="email/invoice_subject.txt",
            html_template="email/invoice_body.html",
            context={"invoice": invoice},
            reply_to=request.user.email,
        )
        messages.success(request, "Invoice e-mailed again!")
        return redirect("invoices:detail", pk=pk)

class InvoiceListView(LoginRequiredMixin, ListView):
    """Table of invoices belonging to the current user’s clients."""
    model               = Invoice
    template_name       = "invoices/invoice_list.html"     # make this template
    context_object_name = "invoices"
    paginate_by         = 25

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("client").order_by("-issue_date")


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model         = Invoice
    template_name = "invoices/invoice_detail.html"         # make this template
    context_object_name = "invoice"


class InvoiceSendView(LoginRequiredMixin, DetailView):
    """
    Re-send an existing invoice by e-mail and return to the detail page.
    Called by a POST form/button in invoice_detail.html
    """
    model = Invoice
    http_method_names = ["post"]  # only allow POST

    def post(self, request, *args, **kwargs):
        invoice = self.get_object()

        send_templated_email(
            to=invoice.client.email,                       # adjust to your client model
            subject_template="email/invoice_subject.txt",
            html_template="email/invoice_body.html",
            context={"invoice": invoice},
            reply_to=invoice.created_by.email              # or whatever makes sense
        )

        messages.success(request, "Invoice e-mailed again!")
        return redirect("invoices:detail", pk=invoice.pk)

