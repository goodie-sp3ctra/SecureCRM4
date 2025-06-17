from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings


# Validator function for phone number

import re

def validate_phone_number(value):
    pattern = re.compile(r'^\+?[0-9\- ]{7,20}$')
    if not pattern.match(value):
        raise ValidationError("Enter a valid phone number.")


# customers/models.py
from django.db import models
from django.utils import timezone

class Client(models.Model):
    user           = models.OneToOneField(
                     settings.AUTH_USER_MODEL,
                     on_delete=models.CASCADE,
                     related_name='client_profile',
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

    status         = models.CharField(
                     max_length=50,
                     choices=STATUS_CHOICES,
                     default='Active',
                     )
    created_at     = models.DateTimeField(default=timezone.now)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


    class Meta:
        ordering = ['company_name']

    # Save hashed password automatically
    def save(self, *args, **kwargs):
        # Only hash if the password is not already hashed
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    # Optional: method to check passwords
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
