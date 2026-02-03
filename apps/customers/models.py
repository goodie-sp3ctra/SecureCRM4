from django.db import models
from django.db.models import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.utils import timezone
from django.conf import settings
import re
from django.core.exceptions import ValidationError

FIELD_TYPE_CHOICES = [
    ('text',   'Text'),
    ('number', 'Number'),
    ('date',   'Date'),
    # …add more types as you build them…
]

APPLIES_TO_CHOICES = [
    ('client', 'Client'),
    ('job', 'Job'), 
]

def validate_phone_number(value):
    """
    Stub validator for phone numbers. Django migrations need to be
    able to import this function, even if you don’t use it anymore.
    """
    pattern = re.compile(r'^\+?[0-9\- ]{7,20}$')
    if not pattern.match(value):
        raise ValidationError("Enter a valid phone number.")

class Client(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile',
        null=True,    # you made it nullable so existing rows can be blank
        blank=True,
    )
    company_name   = models.CharField(max_length=255)
    contact_name   = models.CharField(max_length=255, blank=True)
    contact_email  = models.EmailField(blank=True)
    phone          = models.CharField(max_length=20, blank=True)
    address        = models.TextField(blank=True)

    STATUS_CHOICES = [
        ('Active',   'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Active',
    )

    # ← NEW: your JSONB blob of custom fields
    custom_fields = JSONField(
      default=dict,
      blank=True,
      help_text="Arbitrary key/value pairs for any client-specific custom fields",
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

    class Meta:
        ordering = ['company_name']
        indexes = [
            # gin index for fast lookups on JSONB keys
            GinIndex(fields=['custom_fields']),
        ]


