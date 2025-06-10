from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

# Validator function for phone number
def validate_phone_number(value):
    if not value.isdigit():
        raise ValidationError('Phone number must contain only digits.')
    if len(value) != 10:
        raise ValidationError('Phone number must be exactly 10 digits.')

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[validate_phone_number],
        help_text="Enter a 10-digit phone number without spaces or symbols."
    )
    address = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=128, help_text="Password will be stored in a hashed format.")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.email})'

    class Meta:
        ordering = ['name']

    # Save hashed password automatically
    def save(self, *args, **kwargs):
        # Only hash if the password is not already hashed
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    # Optional: method to check passwords
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
