from django.conf import settings
from django.db import models
from django.utils import timezone

class Activity(models.Model):
    # which contact this belongs to
    contact = models.ForeignKey(
        "customers.Client",
        on_delete=models.CASCADE,
        related_name="activities",
    )
    # who performed the action
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    # a simple slug or code for the type of event
    EVENT_CHOICES = [
        ("created", "Created record"),
        ("updated", "Updated details"),
        ("emailed",  "Sent email"),
        ("called",   "Phone call"),
        # ...etc
    ]
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    # optional free-form description
    note = models.TextField(blank=True)
    # when it happened
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.timestamp:%Y-%m-%d %H:%M} — {self.event_type}"

    def __str__(self):
        return f"{self.user} {self.verb}"
