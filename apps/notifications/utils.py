from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_notification(email, subject, message):
    """Sends an email notification to a user and ensures correct sender."""
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # ✅ This ensures noreply@ticketease.com is used
            [email],
            fail_silently=False,
        )
        logger.info(f"✅ Email successfully sent from {settings.DEFAULT_FROM_EMAIL} to {email}")
    except Exception as e:
        logger.error(f"❌ Email sending failed: {e}")
