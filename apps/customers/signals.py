from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.customers.models import Client
from crm_project.email_utils import send_templated_email

@receiver(post_save, sender=Client)
def email_when_client_created(sender, instance, created, **kwargs):
    if created:
        ctx = {"client": instance}
        send_templated_email(
            to=instance.email,
            subject_template="email/new_client_subject.txt",
            html_template="email/new_client_body.html",
            context=ctx,
        )
