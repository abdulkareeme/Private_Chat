from celery import shared_task
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_email_confirmation(confirm_url , email):
    subject = 'Confirm your email'
    html_message = render_to_string('core/email_confirmation.html', {'confirm_url': confirm_url})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)