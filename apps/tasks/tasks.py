from celery import shared_task
from django.utils import timezone
from django.conf import settings
from apps.tasks.models import Reminder
from crm_project.email_utils import send_templated_email

@shared_task
def send_due_reminders():
    now = timezone.now()
    qs = Reminder.objects.filter(delivered=False, notify_at__lte=now)
    for r in qs.select_related("task", "task__assigned_to"):
        ctx = {"reminder": r, "task": r.task}
        send_templated_email(
            to=r.task.assigned_to.email or settings.DEFAULT_FROM_EMAIL,
            subject_template="email/reminder_subject.txt",
            html_template="email/reminder_body.html",
            context=ctx,
        )
        r.delivered = True
        r.save(update_fields=["delivered"])
         