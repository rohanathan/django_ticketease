from django.core.mail import send_mail
from django.conf import settings

def send_notification(user, subject, message):
    """Sends an email notification to a user."""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # Ensure this is set in settings.py
        [user.email],  # Send to the user's registered email
        fail_silently=False,
    )
