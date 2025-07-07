from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_templated_email(
    to: str,
    subject_template: str,
    html_template: str,
    context: dict,
    reply_to: str | None = None,
):
    subject = render_to_string(subject_template, context).strip()
    html_body = render_to_string(html_template, context)
    msg = EmailMultiAlternatives(
        subject=subject,
        body=html_body,                 # fallback (we'll attach HTML too)
        from_email=None,                # uses DEFAULT_FROM_EMAIL
        to=[to],
        reply_to=[reply_to] if reply_to else None,
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send()
