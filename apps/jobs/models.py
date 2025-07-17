from django.db import models

class Job(models.Model):
    STATUS_NEW        = "NEW"
    STATUS_OPEN       = "OPEN"
    STATUS_IN_PROGRESS= "IN_PROGRESS"
    STATUS_CLOSED     = "CLOSED"
    STATUS_CANCELED   = "CANCELED"
    STATUS_ON_HOLD    = "ON_HOLD"

    STATUS_CHOICES = [
        (STATUS_NEW,         "New"),
        (STATUS_OPEN,        "Open"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_CLOSED,      "Closed"),
        (STATUS_CANCELED,    "Canceled"),
        (STATUS_ON_HOLD,     "On Hold"),
    ]

    client       = models.ForeignKey(
                       'customers.Client',
                       on_delete=models.CASCADE,
                       related_name='jobs'
                   )
    job_number   = models.CharField(max_length=20, unique=True, blank=True)
    title        = models.CharField("Job Title", max_length=255)
    description  = models.TextField("Description", blank=True)
    status       = models.CharField(
                       max_length=15,
                       choices=STATUS_CHOICES,
                       default=STATUS_NEW
                   )
    schedule_date= models.DateField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.job_number or self.id} | {self.title}"