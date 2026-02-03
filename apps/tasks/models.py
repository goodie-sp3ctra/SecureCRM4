from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.customers.models import Client, Job
from apps.customers.models import Client
class Task(models.Model):
    # Core
    title        = models.CharField(max_length=255)
    description  = models.TextField(blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    # Ownership / linkage
    created_by   = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='tasks_created', null=True, blank=True)
    assigned_to  = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='tasks_assigned')
    client       = models.ForeignKey(Client, on_delete=models.SET_NULL,
                                     null=True, blank=True)
    job          = models.ForeignKey(Job, on_delete=models.SET_NULL,
                                     null=True, blank=True)

    # State
    due          = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    PRIORITIES   = (
        ('low', 'Low'), ('normal', 'Normal'),
        ('high', 'High'), ('critical', 'Critical'))
    priority     = models.CharField(max_length=10, choices=PRIORITIES,
                                    default='normal')

    # Repetition (optional)
    REPEAT_CHOICES = (
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'))
    repeat       = models.CharField(max_length=10, choices=REPEAT_CHOICES,
                                    default='none')

    def mark_done(self):
        self.completed_at = timezone.now()
        self.save()

    @property
    def is_overdue(self):
        return not self.completed_at and timezone.now() > self.due

    def __str__(self):
        return self.title


class Reminder(models.Model):
    task        = models.ForeignKey(Task, on_delete=models.CASCADE,
                                    related_name='reminders')
    notify_at   = models.DateTimeField()
    delivered   = models.BooleanField(default=False)

    CHANNELS    = (('popup', 'Web pop-up'), ('email', 'Email'))
    channel     = models.CharField(max_length=10, choices=CHANNELS,
                                   default='popup')

    def __str__(self):
        return f'Reminder for {self.task} at {self.notify_at}'

class Meta:
        permissions = [
            ("can_reassign_task", "Can re-assign task to other users"),
        ]
