from django.core.mail import send_mail
from django.conf import settings


def send_notification(user, subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # Use your Brevo sender email
        [user.email],  # Send to the registered user
        fail_silently=False,
    )
