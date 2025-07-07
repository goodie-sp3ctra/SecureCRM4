# apps/invoices/models.py
from django.db import models
from django.utils import timezone
from apps.customers.models import Client          # existing app
from apps.customers.models import Job                  # existing app


class Invoice(models.Model):
    """
    A bill that can be linked to either a job or directly to a client.
    """

    # ---------- core identifiers ----------
    invoice_number       = models.CharField(
        max_length=30,
        unique=True,
        help_text="Human-readable invoice number shown to the customer.",
    )
    client       = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="invoices",
    )
    job          = models.ForeignKey(               # optional link
        Job,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invoices",
    )

    # ---------- money / dates ----------
    issue_date   = models.DateField(default=timezone.now)
    due_date     = models.DateField()
    subtotal     = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total        = models.DecimalField(max_digits=10, decimal_places=2)

    # ---------- status lifecycle ----------
    DRAFT      = "draft"
    SENT       = "sent"
    PAID       = "paid"
    OVERDUE    = "overdue"

    STATUS_CHOICES = [
        (DRAFT,   "Draft"),
        (SENT,    "Sent"),
        (PAID,    "Paid"),
        (OVERDUE, "Overdue"),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
    )

    # ---------- misc ----------
    notes        = models.TextField(blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering            = ["-issue_date", "-invoice_number"]
        unique_together     = ("client", "invoice_number")     # one client can’t see dup numbers
        verbose_name        = "Invoice"
        verbose_name_plural = "Invoices"

    # ---------- helpers ----------
    @property
    def is_overdue(self):
        return self.status in {self.SENT, self.OVERDUE} and timezone.now().date() > self.due_date

    def __str__(self):
        return f"{self.invoice_number} – {self.client}"
